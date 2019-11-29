#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
log_utils.py - wraps python loggging facility for simple usage
"""
import unittest
import logging.handlers
import os.path
from datetime import datetime
from file_utils import ReverseFileIterator

DEFAULT_LOG_LEVEL = "DEBUG"

# anything going wrong in this module
class LogUtilsError(Exception):
    """
    exception for anything going wrong in this module
    """
    def __init__(self, value):
        """
        This is the exception constructor method
        """
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        """
        Convert error object to a string
        """
        return repr(self.value)

# Logger class, features:
# 1) the caller's file path and line number are printed with each message
# 2) multiple instantiations of this object are possible in the same program
#    wherever you need to log, instantiate a Logger object and call its
#    debug() or info() or warning() or critical() function with a string
#
# Example usage:
#    >>> my_log_utils = Logger("log_filename", "DEBUG")
#    >>> my_log_utils.debug("oh no, what have i done!")
# or
#    >>> my_log_utils.info("oh no, what have i done!")
# and so on..
#
# 1st argument to Logger(): the filename to which logging occurs
# 2nd argument to Logger: the log level above which we do not log

class Logger():
    """
    Analyze video text to find entities (cards from the cards table)
    in it and return a list of entities per video as well as a score
    for each entity, reflecting the confidence that the entity
    corresponds to entities depicted in the video.  The main function
    to use from this class is analyzeVideoEntities() but it has other
    useful text analysis tools embedded.
    """

    def __init__(self, s_log_filename, s_log_level=os.environ.get('LOG_LEVEL')):
        """
        Constructor: initializes logging
        1st argument: the filename to which logging occurs
        2nd argument: the log level above which we do not log
        (hierarchy is debug->info->warning->error->critical)
        """
        if not s_log_level:
            s_log_level = DEFAULT_LOG_LEVEL

        self._log = self._init_logging(s_log_filename, s_log_level)


    @staticmethod
    def _init_logging(s_log_filename, s_log_level):
        """
        Set up the member variable self._log for logging use.
        """
        # NB: using the log filename as the log_utils name
        log_utils = logging.getLogger(s_log_filename)

        # this is how we tell if we have already set-up the handlers for
        # the log_utils instantiated in this class, if yes, don't do it again..
        if log_utils.handlers:
            # we have a handler already, we do need to set up its formatter
            # to the
            return log_utils

        # max size of log file before it gets rotated, not relevant to html
        # logging
        max_log_file_size = 9000000

        # number of backups we keep of log files when they get recycled when
        # they reach MAX_LOG_FILE_SIZE number of bytes, not relevant to html
        # logging
        max_log_file_backups = 9

        log_utils.propagate = False

        log_level_dict = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        log_utils.setLevel(log_level_dict[s_log_level.upper()])

        handler = logging.handlers.RotatingFileHandler(
            s_log_filename,
            maxBytes=max_log_file_size,
            backupCount=max_log_file_backups)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        handler.setFormatter(formatter)
        log_utils.addHandler(handler)

        return log_utils

    # NOTE: the functions below have repeated code - it has to remain
    # this way, because when the repeated code (first four lines of
    # each of the functions below) is put in its own function, it
    # messes up the value returned by self._log.findCaller() such that
    # instead of returning the file which called this module, it returns
    # this module's file.

    def debug(self, s_message):
        """
        write debug message
        """
        self._log.debug(s_message)

    def info(self, s_message):
        """
        write info message
        """
        self._log.info(s_message)

    def warning(self, s_message):
        """
        write warning message
        """
        self._log.warning(s_message)

    def error(self, s_message):
        """
        write error message
        """
        self._log.error(s_message)


    def critical(self, s_message):
        """
        write critical message
        """
        self._log.critical(s_message)

def log_warning(log_obj, s_phrase):
    """
    helper function to know if to log to a file or stdout based on 'log_obj'
    being None or not
    """
    if log_obj is None:
        print(s_phrase)
    else:
        log_obj.warning(s_phrase)

def log_info(log_obj, s_phrase):
    """
    helper function to know if to log to a file or stdout based on 'log_obj'
    being None or not
    """
    if log_obj is None:
        print(s_phrase)
    else:
        log_obj.info(s_phrase)

def log_critical(log_obj, s_phrase):
    """
    helper function to know if to log to a file or stdout based on 'log_obj'
    being None or not
    """
    if log_obj is None:
        print(s_phrase)
    else:
        log_obj.critical(s_phrase)

def log_error(log_obj, s_phrase):
    """
    helper function to know if to log to a file or stdout based on 'log_obj'
    being None or not
    """
    if log_obj is None:
        print(s_phrase)
    else:
        log_obj.error(s_phrase)

def log_debug(log_obj, s_phrase):
    """
    helper function to know if to log to a file or stdout based on 'log_obj'
    being None or not
    """
    if log_obj is None:
        print(s_phrase)
    else:
        log_obj.debug(s_phrase)

def init_logging(log_obj, s_name="unnamed"):
    """
    generic initializer from log obj 'log_obj' - returns None (i.e. does
    nothing) if 'log_obj' is False; returns 'log_obj' if it is not None
    and if it is None, returns a newly created default log object whose
    file is in the directory os.environ["LOG_DIR"] and filename is 's_name'
    """
    if log_obj is False:
        return None

    if log_obj is not None:
        return log_obj

    s_log_dir = os.environ.get("LOG_DIR")
    if s_log_dir is None:
        s_log_dir = "."
    s_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

    return Logger(os.path.join(s_log_dir, s_date+"_"+s_name+".log"))

def get_log_line_components(s_line):
    """
    given a log line, returns its datetime as a datetime object
    and its log level as a string and the message itself as another
    string - those three are returned as a tuple.  the log level
    is returned as a single character (first character of the level's
    name, capitalized).
    """
    try:
        dtime = datetime.strptime(s_line[0:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise LogUtilsError("Not a proper date/time at start of log line!")

    if dtime is None:
        raise LogUtilsError("Not a proper date/time at start of log line!")

    log_level = s_line[24]

    if log_level == "D":
        s_line = s_line[30:]
    elif log_level == "I":
        s_line = s_line[29:]
    elif log_level == "W":
        s_line = s_line[32:]
    elif log_level == "E":
        s_line = s_line[30:]
    elif log_level == "C":
        s_line = s_line[33:]
    else:
        raise LogUtilsError("log-level not in log line!")

    return s_line, dtime, log_level


class ReverseLogFileIterator():
    """
    class to iterate through a log file from end to start, verifying
    that the last line is a warning line has an "END" in it and
    iterating through lines only until the first encounter of a line
    with "START" in it (if no such START warning line is found an
    error is thrown, same for case when no END line is found).
    """

    def __init__(self, s_log_filename):
        """
        do some checking right off the bat
        """
        self._s_log_filename = s_log_filename
        self._iterator = ReverseFileIterator(s_log_filename)
        self._b_started = False
        self._b_ended = False

    def __iter__(self):
        """
        part of allowing this class's objects to also be used as iterators
        """
        return self

    def __next__(self):
        """
        next..
        """
        if self._b_ended is True:
            raise StopIteration

        try:
            s_line = self._iterator.__next__()
        except StopIteration:
            if not self._b_started:
                raise LogUtilsError("log file %s has no START directive!" %
                                    (self._s_log_filename,))
            if not self._b_ended:
                raise LogUtilsError("log file %s has no END directive!" %
                                    (self._s_log_filename,))

        s_message, dtime, log_level = get_log_line_components(s_line)

        if self._b_started is False:
            # only on 1st iteration do we get here
            if len(s_message) < 3 or s_message[0:3] != "END":
                raise LogUtilsError("Last line has no 'END'; file: %s" %
                                    (self._s_log_filename,))

            self._b_started = True
            return s_message, dtime, log_level

        # only on non 1st iteration do we get here, you should never find an
        # 'END' in the line again!
        if len(s_message) >= 3 and s_message[0:3] == "END":
            raise LogUtilsError("2nd 'END' found before any 'START'!")
        if len(s_message) >= 5 and s_message[0:5] == "START":
            # on the next iteration we'll raise a StopIteration
            self._b_ended = True

        return s_message, dtime, log_level

    def all(self):
        """
        runs next() over and over until the end
        """
        return [i for i in self]

def verify_last_log_session(s_log_filename, log_obj=None):
    """
    verify some basic things about last log session, returns the
    duration of the entire session if successful, or None, if
    verification failed
    """
    # s_short_filename = os.path.split(s_log_filename)[-1]
    end_dtime = None
    n_errors = 0
    n_criticals = 0
    n_warnings = 0
    n_lines = 0
    dtime = None
    for s_line, dtime, s_log_type in ReverseLogFileIterator(s_log_filename):
        s_line_len = len(s_line) > 0
        assert s_line_len > 0
        if s_log_type == "E":
            n_errors += 1
        elif s_log_type == "C":
            n_criticals += 1
        elif s_log_type == "W":
            n_warnings += 1

        if not end_dtime:
            end_dtime = dtime

        n_lines += 1

    # start_time = dtime
    # delta_time = end_dtime-start_time
    assert dtime is not None
    delta_time = end_dtime-dtime

    if log_obj:
        # log_obj.info("session duration (seconds): %d" % delta_time.seconds)
        if n_warnings > 0:
            log_obj.warning("# of warnings: %d" % n_warnings)
        if n_errors > 0:
            log_obj.error("# of errors: %d" % n_errors)
        if n_criticals > 0:
            log_obj.critical("# of criticals: %d" % n_criticals)

    return delta_time, n_lines, n_warnings, n_errors, n_criticals

def get_last_session_query(s_log_filename):
    """
    returns first query line it encounters while traversing the
    last session in a log file backwards
    """
    # s_short_filename = os.path.split(s_log_filename)[-1]
    for s_line, dtime, s_log_type in ReverseLogFileIterator(s_log_filename):
        del dtime
        del s_log_type
        if s_line[0:6] == 'query:':
            return s_line[6:].strip()

    return None

class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test01():
        """
        a very basic test
        """
        log = Logger("log_utils.log", "DEBUG")
        log.debug("-->debug<--:hello world!")
        log.info("-->info<--:hello world!")
        log.warning("-->warning<--:hello world!")
        log.error("-->error<--:hello world!")
        log.critical("-->critical<--:hello world!")


if __name__ == "__main__":
    unittest.main()
