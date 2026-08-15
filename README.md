# XOR-Fuzz: coverage-guided fuzz testing for python based on PythonFuzz.

PythonFuzz is coverage-guided [fuzzer](https://developer.mozilla.org/en-US/docs/Glossary/Fuzzing) for testing python packages.
XOR-Fuzz is based on PythonFuzz and modifies it in the following way:
It collects four inputs, creates a mutation mask by xor-ing them to determine commonalities and then directs its mutations towards the differences in the inputs.

Fuzzing for safe languages like python is a powerful strategy for finding bugs like unhandled exceptions, logic bugs,
security bugs that arise from both logic bugs and Denial-of-Service caused by hangs and excessive memory usage.

Fuzzing can be seen as a powerful and efficient strategy in real-world software in addition to classic unit-tests.

## Usage

### Installing XOR-Fuzz as an editable package
To use XOR-Fuzz it is easiest to install it as an editable package. Run the following:

```
git clone git@gitlab.com:alexanderheinrich/pythonfuzz.git xor-fuzz
cd xor-fuzz
pip install -e .
```

### Running Examples

To run one of our examples clone the repository and do the following:
```
python examples/benchmarks/fuzzing.py
```
```
python examples/benchmarks/etree.py
```
```
python examples/benchmarks/htmlparser.py
```

### Fuzz Target

To run XOR-Fuzz on your own code, the first step is to implement the following function (also called a fuzz
target). Here is an example of a simple fuzz function for the built-in `html` module

```python
from html.parser import HTMLParser
from pythonfuzz.main import PythonFuzz


@PythonFuzz
def fuzz(buf):
    try:
        string = buf.decode("ascii")
        parser = HTMLParser()
        parser.feed(string)
    except UnicodeDecodeError:
        pass


if __name__ == '__main__':
    fuzz()
```

Features of the fuzz target:

* fuzz will call the fuzz target in an infinite loop with random data (according to the coverage guided algorithm) passed to `buf`( in a separate process).
* The function must catch and ignore any expected exceptions that arise when passing invalid input to the tested package.
* The fuzz target must call the test function/library with with the passed buffer or a transformation on the test buffer 
if the structure is different or from different type.
* Fuzz functions can also implement application level checks to catch application/logical bugs - For example: 
decode the buffer with the testable library, encode it again, and check that both results are equal. To communicate the results
the result/bug the function should throw an exception.
* pythonfuzz will report any unhandled exceptions as crashes as well as inputs that hit the memory limit specified to pythonfuzz
or hangs/they run more the the specified timeout limit per testcase.


## Credits & Acknowledgments

The original PythonFuzz can be found here: [PythonFuzz](https://gitlab.com/gitlab-org/security-products/analyzers/fuzzers/pythonfuzz)

PythonFuzz is a port of [fuzzitdev/jsfuzz](https://github.com/fuzzitdev/jsfuzz)

which is in turn heavily based on [go-fuzz](https://github.com/dvyukov/go-fuzz) originally developed by [Dmitry Vyukov's](https://twitter.com/dvyukov).
Which is in turn heavily based on [Michal Zalewski](https://twitter.com/lcamtuf) [AFL](http://lcamtuf.coredump.cx/afl/).
