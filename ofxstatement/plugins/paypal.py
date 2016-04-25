# -*- coding: utf-8 -*-

import locale
import itertools
import csv

from datetime import datetime

from contextlib import contextmanager
from ofxstatement.parser import StatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import Statement, StatementLine, generate_transaction_id


def take(iterable, n):
    """Return first n items of the iterable as a list."""
    return list(itertools.islice(iterable, n))


def drop(iterable, n):
    """Drop first n items of the iterable and return result as a list."""
    return list(itertools.islice(iterable, n, None))


def head(iterable):
    """Return first element of the iterable."""
    return take(iterable, 1)[0]


@contextmanager
def scoped_setlocale(category, loc=None):
    """Scoped version of locale.setlocale()"""
    orig = locale.getlocale(category)
    try:
        yield locale.setlocale(category, loc)
    finally:
        locale.setlocale(category, orig)


def atof(string, loc=None):
    """Locale aware atof function for our parser."""
    with scoped_setlocale(locale.LC_NUMERIC, loc):
        return locale.atof(string)


class PayPalStatementParser(StatementParser):
    bank_id = 'PayPal'
    date_format = '%Y/%m/%d'
    valid_header = [
        u"Date",
        u"Time",
        u"Time Zone",
        u"Name",
        u"Type",
        u"Status",
        u"Currency",
        u"Gross",
        u"Fee",
        u"Net",
        u"From Email Address",
        u"To Email Address",
        u"Transaction ID",
        u"Counterparty Status",
        u"Address Status",
        u"Item Title",
        u"Item ID",
        u"Shipping and Handling Amount",
        u"Insurance Amount",
        u"Sales Tax",
        u"Option 1 Name",
        u"Option 1 Value",
        u"Option 2 Name",
        u"Option 2 Value",
        u"Auction Site",
        u"Buyer ID",
        u"Item URL",
        u"Closing Date",
        u"Escrow Id",
        u"Invoice Id",
        u"Reference Txn ID",
        u"Invoice Number",
        u"Custom Number",
        u"Receipt ID",
        u"Balance",
        u"Address Line 1",
        u"Address Line 2/District/Neighborhood",
        u"Town/City",
        u"State/Province/Region/County/Territory/Prefecture/Republic",
        u"Zip/Postal Code",
        u"Country",
        u"Contact Phone Number",
        u"",
    ]

    def __init__(self, fin, account_id, currency, encoding=None, locale=None, analyze=False):
        self.account_id = account_id
        self.currency = currency
        self.locale = locale
        self.encoding = encoding
        self.analyze = analyze

        with open(fin, 'r', encoding=self.encoding) as f:
            self.lines = f.readlines()

        self.validate()
        self.statement = Statement(
            bank_id=self.bank_id,
            account_id=self.account_id,
            currency=self.currency
        )

    @property
    def reader(self):
        return csv.reader(self.lines, delimiter=',')

    @property
    def header(self):
        return [c.strip() for c in head(self.reader)]

    @property
    def rows(self):
        rs = drop(self.reader, 1)
        currency_idx = self.valid_header.index("Currency")
        return [r for r in rs if r[currency_idx] == self.currency]

    def validate(self):
        """
        Validate to ensure csv has the same header we expect.
        """

        expected = self.valid_header
        actual = self.header
        if expected != actual:
            msg = "\n".join([
                "Header template doesn't match:",
                "expected: %s" % expected,
                "actual  : %s" % actual
            ])
            raise ValueError(msg)

    def split_records(self):
        for row in self.rows:
            yield row

    def parse_record(self, row):

        id_idx = self.valid_header.index("Transaction ID")
        date_idx = self.valid_header.index("Date")
        memo_idx = self.valid_header.index("Name")
        refnum_idx = self.valid_header.index("Reference Txn ID")
        amount_idx = self.valid_header.index("Gross")
        payee_idx = self.valid_header.index("To Email Address")

        stmt_line = StatementLine()
        stmt_line.id = row[id_idx]
        stmt_line.date = datetime.strptime(row[date_idx], self.date_format)
        stmt_line.payee = row[payee_idx]
        stmt_line.memo = row[memo_idx]
        if self.analyze:
            if stmt_line.payee.lower() == 'steamgameseu@steampowered.com':
                idx = self.valid_header.index("Item Title")
                stmt_line.memo = '{0} / {1}'.format(stmt_line.memo, row[idx])

        stmt_line.refnum = row[refnum_idx]
        stmt_line.amount = atof(row[amount_idx].replace(" ", ""), self.locale)

        return stmt_line


def parse_bool(value):
    if value in ('True', 'true', '1'):
        return True
    if value in ('False', 'false', '0'):
        return False
    raise ValueError("Can't parse boolean value: %s" % value)


class PayPalPlugin(Plugin):
    def get_parser(self, fin):
        kwargs = {
            'encoding': 'iso8859-1',
        }
        if self.settings:
            if 'account_id' in self.settings:
                kwargs['account_id'] = self.settings.get('account_id')
            if 'currency' in self.settings:
                kwargs['currency'] = self.settings.get('currency')
            if 'locale' in self.settings:
                kwargs['locale'] = self.settings.get('locale')
            if 'encoding' in self.settings:
                kwargs['encoding'] = self.settings.get('encoding')
            if 'analyze' in self.settings:
                kwargs['analyze'] = parse_bool(self.settings.get('analyze'))
        return PayPalStatementParser(fin, **kwargs)
