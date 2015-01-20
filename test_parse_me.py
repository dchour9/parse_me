from io import StringIO
import unittest

from parse_me import real_parser

class test_parse_me(unittest.TestCase):
    maxDiff = None

    sample1 = unicode("""              SALE RECEIPT
Store #11476       eat 01/07/10 16:01:48
Subway Sandwiches & Salads
609 N  MILPAS  ST
MILPAS                    CA 93103
805-966-3001
Trans# 137 Clerk 3     RAJVINDERPAL
Dwr1 TRDT 010710 Reg-ID REG-MAIN
                    Receipt # 0000103913
--- ITEM --- QTY       PRICE MEMO  PLU
HAM&CHEESEfr  1  T $    5.00Add$2FV10225
DRK-21oz      1  TD$    1.20Add$2FV10002
CHIPS         1  TD$    0.80Add$2FV10020
 SOUP         1  T $    1.00       22300
                    --------
        SUBTOTAL $      8.00
       Sales Tx  $      0.70
                    --------
EAT-IN   **TOTAL $      8.70
Cash    AMT TEND $      9.00
                    --------
       CHANGE DUE$      0.30

WE THANK YOU AND APPRECIATE YOUR BUSINES
""")

    def test_store_number(self):
        s = StringIO(test_parse_me.sample1)
        r = real_parser(s)
        self.assertEqual(11476, r.get("store_number", "no store_number"))

    def test_date(self):
        s = StringIO(test_parse_me.sample1)
        r = real_parser(s)
        self.assertEqual("2010-01-07 16:01:48", r.get("date", "no date"))

    def test_address(self):
        s = StringIO(test_parse_me.sample1)
        r = real_parser(s)
        self.assertEqual("609 N  MILPAS  ST", r.get("address", "no address"))

    def test_zipcode(self):
        s = StringIO(test_parse_me.sample1)
        r = real_parser(s)
        self.assertEqual("93103", r.get("zipcode", "no zipcode"))

    def test_phone_number(self):
        s = StringIO(test_parse_me.sample1)
        r = real_parser(s)
        self.assertEqual("805-966-3001", r.get("phone_number", "no phone_number"))


