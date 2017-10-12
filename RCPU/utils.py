import contextlib
import os
import sys
import termios
import tty
# Taken from https://stackoverflow.com/a/45266694
# TODO: make this cross-platform

_MAX_CHARACTER_BYTE_LENGTH = 4


@contextlib.contextmanager
def _tty_reset(file_descriptor):  # pragma: no cover
    """
    A context manager that saves the tty flags of a file descriptor upon
    entering and restores them upon exiting.
    """
    old_settings = termios.tcgetattr(file_descriptor)
    try:
        yield
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)


def get_character(file=sys.stdin):
    """
    Read a single character from the given input stream (defaults to sys.stdin).
    """
    try:  # pragma: no cover
        file_descriptor = file.fileno()
        with _tty_reset(file_descriptor):
            tty.setcbreak(file_descriptor)
            return os.read(file_descriptor, _MAX_CHARACTER_BYTE_LENGTH)
    except IOError:
        return file.read(1)
