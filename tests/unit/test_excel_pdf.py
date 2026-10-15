"""Editype excel (.xlsx with openpyxl, .xls with xlrd) and preprocessing extractpdf (pdfminer.six).

`data/orders.xls` has the same content as the .xlsx made in the test; it was written once with xlwt.
"""
import datetime
import os

import pytest

from helpers import parse, records, write_grammar

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

EXCEL_GRAMMAR = '''
    from bots.botsconfig import *
    syntax = {'field_sep': ';', 'quote_char': '"', 'charset': 'utf-8', 'skip_firstline': True, 'noBOTSID': True}
    structure = [{ID: 'LIN', MIN: 1, MAX: 9999}]
    recorddefs = {'LIN': [
        ['BOTSID', 'M', 3, 'A'], ['ORDER', 'C', 35, 'AN'], ['DATE', 'C', 35, 'AN'], ['QTY', 'C', 16, 'R'],
        ['PRICE', 'C', 16.4, 'R'], ['NAME', 'C', 70, 'AN'], ['FLAG', 'C', 5, 'AN'], ['TIME', 'C', 35, 'AN'],
    ]}
'''
HEADER = ['order', 'date', 'qty', 'price', 'name', 'flag', 'time']
ROWS = [
    ['PO-1', datetime.date(2026, 1, 31), 12, 1.25, 'bolt; "M8"', True, datetime.datetime(2026, 1, 31, 13, 45, 0)],
    ['PO-2', datetime.date(2026, 2, 1), 3.5, 100, 'café €', False, datetime.time(7, 5, 9)],
]
EXPECTED = [
    {'BOTSID': 'LIN', 'ORDER': 'PO-1', 'DATE': '2026-01-31', 'QTY': '12', 'PRICE': '1.25', 'NAME': 'bolt; "M8"',
     'FLAG': '1', 'TIME': '2026-01-31T13:45:00'},
    {'BOTSID': 'LIN', 'ORDER': 'PO-2', 'DATE': '2026-02-01', 'QTY': '3.5', 'PRICE': '100', 'NAME': 'café €',
     'FLAG': '0', 'TIME': 'T07:05:09'},
]


@pytest.fixture(scope='module', autouse=True)
def grammars(botsenv):
    write_grammar('excel', 'ut_orders', EXCEL_GRAMMAR)


def parse_file(tmp_path, content):
    edi = parse(tmp_path, 'excel', 'ut_orders', content)
    assert not edi.errorfatal and not edi.errorlist, edi.errorlist
    return records(edi)


def test_excel_xlsx(tmp_path):
    openpyxl = pytest.importorskip('openpyxl')
    book = openpyxl.Workbook()
    sheet = book.active
    for row in [HEADER] + ROWS:
        sheet.append(row)
    sheet.append([None, None, None])            # an empty row at the end is not a record
    book.create_sheet('second').append(['only the first sheet is read'])
    path = tmp_path / 'orders.xlsx'
    book.save(path)
    assert parse_file(tmp_path, path.read_bytes()) == EXPECTED


def test_excel_xls(tmp_path):
    pytest.importorskip('xlrd')
    with open(os.path.join(DATA, 'orders.xls'), 'rb') as f:
        assert parse_file(tmp_path, f.read()) == EXPECTED


def test_excel_file_that_is_not_excel(tmp_path):
    pytest.importorskip('xlrd')
    edi = parse(tmp_path, 'excel', 'ut_orders', b'this is not an excel file')
    assert edi.errorfatal and 'Excel extraction failed' in ''.join(edi.errorlist)


# ---------------------------------------------------------------- pdf

def make_pdf(pages):
    """A pdf with text in Helvetica 10. pages: list of pages; a page is a list of (x, y, text)."""
    objects = ['<< /Type /Catalog /Pages 2 0 R >>', None, '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
    kids = []
    for texts in pages:
        stream = 'BT /F1 10 Tf ' + ' '.join(
            '1 0 0 1 %s %s Tm (%s) Tj' % (x, y, text.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)'))
            for x, y, text in texts) + ' ET'
        objects.append('<< /Length %d >>\nstream\n%s\nendstream' % (len(stream), stream))
        objects.append('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents %d 0 R '
                       '/Resources << /Font << /F1 3 0 R >> >> >>' % len(objects))
        kids.append('%d 0 R' % len(objects))
    objects[1] = '<< /Type /Pages /Kids [%s] /Count %d >>' % (' '.join(kids), len(kids))
    out = b'%PDF-1.4\n'
    offsets = []
    for nr, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out += ('%d 0 obj\n%s\nendobj\n' % (nr, obj)).encode('latin-1')
    xref = len(out)
    out += ('xref\n0 %d\n0000000000 65535 f \n' % (len(objects) + 1)).encode('ascii')
    out += b''.join(('%010d 00000 n \n' % offset).encode('ascii') for offset in offsets)
    out += ('trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objects) + 1, xref)).encode('ascii')
    return out


def extract(pdf, **parameters):
    """run preprocessing function extractpdf on pdf (bytes); returns the csv as written (bytes)"""
    from bots import botslib, preprocess
    from bots.botsconfig import FILEIN, OK
    name = 'pdf%s' % len(pdf)
    with botslib.opendata_bin(name, 'wb') as f:
        f.write(pdf)
    ta_from = botslib.NewTransaction(status=FILEIN, statust=OK, filename=name, idroute='utpdf', charset='utf-8')
    ta_from.filename = name
    before = max(row['idta'] for row in botslib.query('SELECT idta FROM ta'))
    preprocess.extractpdf(ta_from, FILEIN, **parameters)
    rows = list(botslib.query('SELECT idta, filename, statust FROM ta WHERE idta>%(idta)s', {'idta': before}))
    assert len(rows) == 1 and rows[0]['statust'] == OK
    with botslib.opendata_bin(rows[0]['filename'], 'rb') as f:
        return f.read()


def test_extractpdf(botsenv):
    pytest.importorskip('pdfminer')
    pdf = make_pdf([
        [(50, 800, 'Order'), (200, 800, 'PO-1'), (50, 780, 'Item'), (200, 780, 'bolt, M8'), (400, 780, '12')],
        [(50, 800, 'Total'), (200, 800, '15.00')],
    ])
    # page number, line number on the page, then the fields; text that is close together is one field
    assert extract(pdf).decode('utf-8') == (
        '1,1,Order,PO-1\r\n'
        '1,2,Item,"bolt, M8",12\r\n'
        '2,1,Total,15.00\r\n')
    assert extract(pdf + b' ', field_sep=';').decode('utf-8').splitlines()[1] == '1;2;Item;bolt, M8;12'


def test_extractpdf_file_that_is_not_pdf(botsenv):
    pytest.importorskip('pdfminer')
    from bots.exceptions import InMessageError
    with pytest.raises(InMessageError, match='PDF extraction failed'):
        extract(b'this is not a pdf file')
