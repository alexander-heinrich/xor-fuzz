from pythonfuzz.main import PythonFuzz
from time import time
from html.parser import HTMLParser
import signal


@PythonFuzz
def fuzz(buf):
    try:
        string = buf.decode("ascii")
        parser = HTMLParser()
        parser.feed(string)
    except UnicodeDecodeError:
        pass


class TimeoutException(Exception):
    pass


def raise_timeout(signum, frame):
    raise TimeoutException


MINUTES = 60

if __name__ == '__main__':
    duration = 30 * MINUTES
    start = time()
    found_exceptions = []
    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(duration)
    try:
        while True:
            pre_fuzz = time()
            fuzz()
            post_fuzz = time()
            found_exceptions.append(post_fuzz - pre_fuzz)
    except TimeoutException:
        print(f"Found {len(found_exceptions)} exceptions in {duration} seconds.")
    signal.alarm(0)
