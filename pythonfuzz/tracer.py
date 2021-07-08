import collections
import sys

prev_line = 0
prev_filename = ''
data = collections.defaultdict(set)


def trace(frame, event, arg):
    if event != 'line':
        return trace

    global prev_line
    global prev_filename

    func_filename = frame.f_code.co_filename
    func_line_no = frame.f_lineno

    if func_filename != prev_filename:
        # We need a way to keep track of inter-files transfers,
        # and since we don't really care about the details of the coverage,
        # concatenating the two filenames is enough.
        data[func_filename + prev_filename].add((prev_line, func_line_no))
    else:
        data[func_filename].add((prev_line, func_line_no))

    prev_line = func_line_no
    prev_filename = func_filename

    return trace


def get_coverage():
    return sum(map(len, data.values()))


class Tracer(object):
    def traceit(self, frame, event, arg):
        if self.original_trace_function is not None:
            self.original_trace_function(frame, event, arg)

        if event == "line":
            function_name = frame.f_code.co_name
            lineno = frame.f_lineno
            self._trace.append((function_name, lineno))

        return self.traceit

    def __init__(self):
        self._trace = []

    # Executes at start of `with` block
    def __enter__(self):
        self.original_trace_function = sys.gettrace()
        sys.settrace(self.traceit)
        return self

    # Executes at end of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        sys.settrace(self.original_trace_function)

    # List of (function_name, line_number) for executed lines
    def coverage_list(self):
        return self._trace

    # Set of (function_name, line_number) for executed lines
    def coverage_set(self):
        return frozenset(self.coverage_list())

    def num_lines_covered(self):
        return len(self._trace)
