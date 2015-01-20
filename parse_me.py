#!/usr/bin/env python

from datetime import datetime
from inspect import stack as inspect_stack
from logging import getLogger
import re

def parse(filename):
    with open(filename, "r") as f:
        return real_parser(f)

def real_parser(iostream):
    """Receipt parser. This could use a little work.
    """
    l = getLogger("{}".format(inspect_stack()[1][3]))
    r = dict()
    line = iostream.readline()
    while line:
        l.debug("read: %r", line)
        m = re.match(r"Store #(?P<store>\d+) +(?:eat|tko|tkc) +(?P<month>\d\d)/(?P<day>\d\d)/(?P<year>\d+) (?P<hour>\d\d):(?P<minute>\d\d):(?P<second>\d\d) *\n", line)
        address = re.match(r"(?P<stnum>\d+) +(?P<stname>\D+) *\n", line)
        zipcode = re.match(r"(?P<city>\D+) +(?P<state>\D\D) +(?P<zipcode>\d+) *\n", line)
        number = re.match(r"Phone (?P<areacode>\d\d\d)-(?P<local>\d\d\d)-(?P<pin>\d\d\d\d) *\n", line)
        phonenum = re.match(r"(?!Fax)(?P<areacode>\d\d\d)-(?P<local>\d\d\d)-(?P<pin>\d\d\d\d) *\n", line)
        #card = re.match(r"(?P<blank>\.+) +(?:Card|Account No:) +(?#************) +(?P<pin>\d\d\d\d) *\n", line)
        card = re.match(r"Card (?P<blank>\D+)(?P<pin>\d\d\d\d) *\n", line)
        account = re.match(r"(?P<blank2>\s+)Account No: (?P<blank>\D+)(?P<pin>\d\d\d\d) *\n", line)
        if card:
            l.debug("match: %r", card.groups())
            cardNum = card.groups()[1]
            r["last_card_used"] = cardNum
            line = iostream.readline()
            continue
        if account:
            l.debug("match: %r", account.groups())
            accountNum = account.groups()[2]
            r["last_account_used"] = accountNum
            line = iostream.readline()
            continue
        if m:
            l.debug("match: %r", m.groups())
            store, month, day, year, hour, minute, second  = [int(x) for x in m.groups()]
            r["store_number"] = store
            r["date"] = datetime(2000 + year, month, day, hour, minute, second).isoformat(sep=" ")
            line = iostream.readline()
            continue
        if address:
            l.debug("match: %r", address.groups())
            stnum = address.groups()[0]
            stname = address.groups()[1]
            r["address"] = stnum + " " + stname
            line = iostream.readline()
            continue
        if zipcode:
            l.debug("match: %r", zipcode.groups())
            zips = zipcode.groups()[2]
            r["zipcode"] = zips
            line = iostream.readline()
            continue
        if number:
            l.debug("match: %r", number.groups())
            area, local, pin = [int(x) for x in number.groups()]
            r["phone_number"] = str(area) + "-" + str(local) + "-" + str(pin)
            line = iostream.readline()
            continue
        if phonenum:
            l.debug("match : %r", phonenum.groups())
            area, local, pin = [int(x) for x in phonenum.groups()]
            r["phone_number"] = str(area) + "-" + str(local) + "-" + str(pin)
            line = iostream.readline()
            continue
        else:
            l.debug("no match")
        line = iostream.readline()
    # I should probably parse a little more of the receipt...
    return r

if "__main__" == __name__:
    from argparse import ArgumentParser
    from logging import basicConfig, CRITICAL, ERROR, WARNING, INFO, DEBUG

    parser = ArgumentParser(description="Parse a receipt file.")
    parser.add_argument("-v", "--verbose", action="count")
    parser.add_argument("-q", "--quiet", action="count")
    parser.add_argument("file_name", metavar="file_name")

    arguments = parser.parse_args()

    raw_log_level = 2 + (arguments.verbose or 0) - (arguments.quiet or 0)
    if   raw_log_level <= 0: log_level = CRITICAL
    elif raw_log_level == 1: log_level = ERROR
    elif raw_log_level == 2: log_level = WARNING    # default
    elif raw_log_level == 3: log_level = INFO
    else:                    log_level = DEBUG
    basicConfig(level=log_level)

    l = getLogger("{}".format(__name__))
    l.debug("Parsing file: %s", arguments.file_name)

    from pprint import pprint
    pprint(parse(arguments.file_name))
