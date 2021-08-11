"""
Inquirer interface
"""
import asyncio
import sys

import inquirer  # type: ignore

from brutus.interfaces.utils.inquirer_utils import destructure
from brutus.modules.web_crawler.WebCrawler import WebCrawler
from brutus.utils.logger import LOGGER


def prepend_protocol(url: str) -> str:
    """Prefix a URL with a protocol schema if not present

    Args:
        url (str)

    Returns:
        str
    """
    if '://' not in url:
        url = 'https://' + url
    return url


def run() -> None:
    """Run the inquirer interface and module"""

    questions = [
        inquirer.List(
            name='strict', message='Run in strict mode?', choices=[True, False]
        ),
        inquirer.Text(
            name='n_redirects',
            message='Enter maximum allowable redirects',
            default='10',
            validate=lambda _, n: isinstance(int(n), int),
        ),
        inquirer.Text(
            name='n_tries',
            message='Enter maximum connection retries',
            default='4',
            validate=lambda _, n: isinstance(int(n), int),
        ),
        inquirer.Text(
            name='n_tasks',
            message='Enter maximum concurrent connections',
            default='200',
            validate=lambda _, n: isinstance(int(n), int),
        ),
        inquirer.Text(
            name='root_urls', message='Enter root URLs to crawl from (comma-delimited)'
        ),
    ]

    answers = inquirer.prompt(questions)

    strict, n_redirects, n_tries, n_tasks, root_urls = destructure(
        answers, 'strict', 'n_redirects', 'n_tries', 'n_tasks', 'root_urls'
    )

    loop = asyncio.get_event_loop()

    try:
        urls = root_urls.split(',')
        fmt_urls = {prepend_protocol(url) for url in urls}

        crawler = WebCrawler(
            root_urls=fmt_urls,
            exclude=None,
            strict=strict,
            max_redirect=int(n_redirects),
            max_tries=int(n_tries),
            max_tasks=int(n_tasks),
        )

        loop.run_until_complete(crawler.crawl())  # Crawler gonna crawl

    except KeyboardInterrupt:
        sys.stderr.flush()
        LOGGER.info('Interrupted')

    finally:
        crawler.run_report()

        asyncio.run(crawler.close())

        # next two lines are required for actual aiohttp resource cleanup
        loop.stop()
        loop.run_forever()

        loop.close()


if __name__ == '__main__':
    run()
