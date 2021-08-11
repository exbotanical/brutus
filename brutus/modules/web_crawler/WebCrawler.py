"""This module exposes a public API for web crawling
"""
import asyncio
import cgi
import re
import time
import typing
import urllib.parse
from asyncio import Queue
from collections import namedtuple

import aiohttp

from brutus.models.BaseBrutusModule import BaseBrutusModule
from brutus.utils.logger import LOGGER

UrlStatistic = namedtuple(
    'UrlStatistic',
    [
        'url',
        'next_url',
        'status',
        'exception',
        'size',
        'content_type',
        'encoding',
        'num_urls',
        'num_new_urls',
    ],
)


class WebCrawler(BaseBrutusModule):  # pylint: disable=R0902
    """Implements a crawler that parses a given set of root URLs,
    and builds a report of statistics collected on discovered hyperlinks

    Inherits:
        BaseBrutusModule
    """

    def __init__(
        self,
        root_urls: set,
        exclude: str = None,
        strict: bool = True,
        max_redirect: int = 10,
        max_tries: int = 4,
        max_tasks: int = 10,
    ):

        BaseBrutusModule.__init__(self)

        # event loop impl
        self.ev = asyncio.get_event_loop()

        # root URLs from which to crawl
        self.root_urls = root_urls

        # a regex pattern to exclude from crawling
        self.exclude = exclude

        # only crawl literal host matches?
        self.strict = strict

        # max no. of redirects to follow
        self.max_redirect = max_redirect

        # max attempts to establish a connection
        self.max_tries = max_tries

        # max concurrent tasks
        self.max_tasks = max_tasks

        # synchronized, evented queue
        self.queue = Queue(loop=self.ev)  # type: ignore

        # URLs that have been crawled
        self.crawled_urls: typing.Set = set()

        # statistics on crawling results
        self.statistics: list = []

        # base HTTP session manager
        self.session = aiohttp.ClientSession(loop=self.ev)

        self.root_domains = set()

        self.stats: dict = {}
        self.t0: float = 0
        self.t1: float = 0

        for root in root_urls:
            parts = urllib.parse.urlparse(root)
            host, _ = urllib.parse.splitport(parts.netloc)  # type: ignore

            if not host:
                continue
            if re.match(r'\A[\d\.]*\Z', host):
                self.root_domains.add(host)
            else:
                host = host.lower()

                if self.strict:
                    self.root_domains.add(host)
                else:
                    self.root_domains.add(WebCrawler.resolve_domain(host))

        for root in root_urls:
            self.produce_work_unit(root)

        self.t0 = time.time()
        self.t1 = 0

    @staticmethod
    def resolve_domain(host: str) -> str:
        """Resolve the host to just the domain

        Args:
            host (str)

        Returns:
            str
        """
        parts = host.split('.')[-2:]
        return ''.join(parts)

    @staticmethod
    def is_redirect(response: aiohttp.ClientResponse) -> bool:
        """Is the HTTP response code indicative of a redirect?

        Args:
            response (aiohttp.ClientResponse)

        Returns:
            bool
        """
        return response.status in (300, 301, 302, 303, 307)

    async def close(self) -> None:
        """Close all resources"""
        await self.session.close()

    def host_okay(self, host: str) -> bool:
        """Evaluate whether a host should be crawled. Literal matches
        are always considered viable. Approximate matches are crawled if
        strict mode is OFF.

        Args:
            host (str)

        Returns:
            bool
        """
        host = host.lower()
        if host in self.root_domains:
            return True

        if re.match(r'\A[\d\.]*\Z', host):
            return False

        if self.strict:
            return self.host_valid_strict(host)

        return self.host_valid_lenient(host)

    def host_valid_strict(self, host: str) -> bool:
        """Evaluate whether a host should be crawled

        Args:
            host (str)

        Returns:
            bool
        """
        host = host[4:] if host.startswith('www.') else 'www.' + host
        return host in self.root_domains

    def host_valid_lenient(self, host: str) -> bool:
        """Evaluate whether a host should be crawled, lenient mode

        Args:
            host (str)

        Returns:
            bool
        """
        return WebCrawler.resolve_domain(host) in self.root_domains

    def record_statistic(self, stats: 'UrlStatistic'):
        """Record a UrlStatistic"""
        self.statistics.append(stats)

    async def parse_links(
        self, response: aiohttp.ClientResponse
    ) -> typing.Tuple[UrlStatistic, set]:
        """Parse discovered URLs / hyperlinks

        Args:
            response (aiohttp.ClientResponse)

        Returns:
            tuple[UrlStatistic, set]: a tuple of the statistic
            and associated URLs / hyperlinks
        """
        links = set()
        content_type = None
        encoding = None
        body = await response.read()

        if response.status == 200:
            content_type = response.headers.get('content-type')
            enc: typing.Dict[str, str] = {}

            if content_type:
                content_type, enc = cgi.parse_header(content_type)

            encoding = enc.get('charset', 'utf-8')

            if content_type in ('text/html', 'application/xml'):
                text = await response.text()

                # replace href with (?:href|src) to follow image links
                urls = set(re.findall(r'''(?i)href=["']([^\s"'<>]+)''', text))
                if urls:
                    LOGGER.info(
                        'found %r distinct urls via %r',
                        len(urls),
                        response.url.human_repr(),
                    )

                for url in urls:
                    normalized = urllib.parse.urljoin(str(response.url), url)

                    defragmented, _ = urllib.parse.urldefrag(normalized)

                    if self.is_url_valid(defragmented):
                        links.add(defragmented)

        stat = UrlStatistic(
            url=response.url,
            next_url=None,
            status=response.status,
            exception=None,
            size=len(body),
            content_type=content_type,
            encoding=encoding,
            num_urls=len(links),
            num_new_urls=len(links - self.crawled_urls),
        )

        return stat, links

    async def fetch(self, url: str, max_redirect: int) -> None:
        """Fetch a single URL

        Args:
            url (str)
            max_redirect (int)
        """
        tries = 0
        exception = None

        while tries < self.max_tries:
            try:
                response = await self.session.get(url, allow_redirects=False)

                if tries > 1:
                    LOGGER.debug('fetch attempt %r for %r succeeded', tries, url)

                break

            except aiohttp.ClientError as client_error:
                LOGGER.error('fetch attempt %r for %r: %r', tries, url, client_error)
                exception = client_error

            tries += 1

        else:
            LOGGER.error(
                'attempt to fetch %r failed after %r tries', url, self.max_tries
            )

            self.record_statistic(
                UrlStatistic(
                    url=url,
                    next_url=None,
                    status=None,
                    exception=exception,
                    size=0,
                    content_type=None,
                    encoding=None,
                    num_urls=0,
                    num_new_urls=0,
                )
            )

            return

        try:
            if WebCrawler.is_redirect(response):
                location = response.headers['location']
                next_url = urllib.parse.urljoin(url, location)

                self.record_statistic(
                    UrlStatistic(
                        url=url,
                        next_url=next_url,
                        status=response.status,
                        exception=None,
                        size=0,
                        content_type=None,
                        encoding=None,
                        num_urls=0,
                        num_new_urls=0,
                    )
                )

                if next_url in self.crawled_urls:
                    return

                if max_redirect > 0:
                    LOGGER.info('found redirect: from %r to %r', url, next_url)
                    self.produce_work_unit(next_url, max_redirect - 1)

                else:
                    LOGGER.error('redirect limit reached: from %r to %r', url, next_url)
            else:
                stat, links = await self.parse_links(response)

                self.record_statistic(stat)

                for link in links.difference(self.crawled_urls):
                    self.queue.put_nowait((link, self.max_redirect))

                self.crawled_urls.update(links)

        finally:
            await response.release()

    async def queued_coroutine(self) -> None:
        """Process the queue indefinitely"""
        try:
            while True:
                url, max_redirect = await self.queue.get()

                assert url in self.crawled_urls

                await self.fetch(url, max_redirect)

                self.queue.task_done()

        except asyncio.CancelledError:
            pass

    def is_url_valid(self, url: str) -> bool:
        """Is the given URL valid i.e. http/s scheme?

        Args:
            url (str)

        Returns:
            bool
        """
        if self.exclude and re.search(self.exclude, url):
            return False

        parts = urllib.parse.urlparse(url)

        if parts.scheme not in ('http', 'https'):
            LOGGER.debug('skipping non-http scheme in found at %r', url)
            return False

        host, _ = urllib.parse.splitport(parts.netloc)  # type: ignore

        if not self.host_okay(host):
            LOGGER.debug('skipping non-root host found at %r', url)
            return False

        return True

    def produce_work_unit(self, url: str, max_redirect: int = None) -> None:
        """Add a unit of work to the synchronized queue

        Args:
            url (str)
            max_redirect (int, optional): Defaults to None.
        """
        if max_redirect is None:
            max_redirect = self.max_redirect

        LOGGER.debug('adding %r %r', url, max_redirect)

        self.crawled_urls.add(url)
        self.queue.put_nowait((url, max_redirect))

    async def crawl(self) -> None:
        """Run the primary crawling routine"""
        workers = [
            asyncio.Task(self.queued_coroutine(), loop=self.ev)
            for _ in range(self.max_tasks)
        ]

        self.t0 = time.time()

        await self.queue.join()

        self.t1 = time.time()

        for w in workers:
            w.cancel()

    def add_statistic(self, key: str, count: int = 1) -> None:
        """Add a statistic record

        Args:
            key (str)
            count (int, optional). Defaults to 1.
        """
        self.stats[key] = self.stats.get(key, 0) + count

    def log_statistic(self) -> None:
        """Log a statistic record to the logger instance"""
        for key, count in sorted(self.stats.items()):
            LOGGER.info('%10d' % count, key)

    def run_report(self) -> None:
        """Run (print) a full session report"""
        t1 = self.t1 or time.time()

        dt = t1 - self.t0

        if dt and self.max_tasks:
            speed = len(self.statistics) / dt / self.max_tasks
        else:
            speed = 0

        LOGGER.info('CRAWLER STATISTICS REPORT')

        try:
            show = list(self.statistics)
            show.sort(key=lambda stat: str(stat.url))

            for stat in show:
                self.log_url_metadata(stat)

        except KeyboardInterrupt:
            LOGGER.info('SIGINT received')

        LOGGER.info(
            'Completed parsing',
            len(self.statistics),
            'urls in %.3f secs' % dt,
            '(max_tasks=%d)' % self.max_tasks,
            '(%.3f urls per second per task)' % speed,
        )

        self.log_statistic()

        LOGGER.info('Remaining:', self.queue.qsize())
        LOGGER.info('Total Statistics:', len(self.statistics))
        LOGGER.info('Datetime:', time.ctime(), 'local time')

    def log_url_metadata(self, stat: 'UrlStatistic') -> None:
        """Run (print) log URL metadata, add statistics

        Args:
            stat (UrlStatistic)
        """
        if stat.exception:
            self.add_statistic('fail')
            self.add_statistic('fail_' + str(stat.exception.__class__.__name__))

            LOGGER.info(stat.url, 'error', stat.exception)

        elif stat.next_url:
            self.add_statistic('redirect')
            LOGGER.info(stat.url, stat.status, 'redirect', stat.next_url)

        elif stat.content_type == 'text/html':
            self.add_statistic('html')
            self.add_statistic('html bytes', stat.size)
            LOGGER.info(
                stat.url,
                stat.status,
                stat.content_type,
                stat.encoding,
                stat.size,
                '%d/%d' % (stat.num_new_urls, stat.num_urls),
            )

        else:
            if stat.status == 200:
                self.add_statistic('other')
                self.add_statistic('other bytes', stat.size)
            else:
                self.add_statistic('error')
                self.add_statistic('error bytes', stat.size)
                self.add_statistic('status_%s' % stat.status)

            LOGGER.info(
                stat.url, stat.status, stat.content_type, stat.encoding, stat.size
            )
