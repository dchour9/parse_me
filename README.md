parse_me
========

`sample1.txt` through `sample4.txt` are receipts that came out of a subway POS
and were destined for a printer. We want to parse out the contents of these
receipts and store the information in a data structure. You can design any data
structure you like to represent the data. `parse_me.py` contains the very
beginnings of a program to do this. Finish the `real_parse` method of this
program. You'll know you're on the right track if you can get some more of the
unit tests passing (see below for instructions on how to run the unit tests).
Or you can write your own solution in the language of your choice.  If you're
using `parse_me.py`, run it as follows:

```sh
./parse_me.py sample1.txt
```

or

```sh
./parse_me.py -vv sample2.txt
```

Expert Mode
-----------

Demonstrate your awesomeness with unit tests. We have included
`test_parse_me.py` which contains a number of unit tests. You can run these
using

```sh
unit2 discover
```

from the command line. You'll see that two of the tests are already passing.
Maybe more if you've already completed the `real_parse` method. Develop unit
tests to cover the parsing of the entire receipt, and for extra bonus points
show us a commit history that demonstrated test-driven development.

LEGENDARY Mode
--------------

Do something useful with the credit-card info in `sample2.txt` and the two sub-
cards in the footer of `sample4.txt` while still not breaking on any of the
other samples.
