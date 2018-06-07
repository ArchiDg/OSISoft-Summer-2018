import logging

class Log(object):
    def __init__(self, log_file_name):
        self.logging.basicConfig(filename=log_file_name, level=logging.INFO)

