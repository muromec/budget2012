# encoding: utf8

import xlrd
import re
import collections

Money = collections.namedtuple("Money", 
        ["wtf1", "idx1", "idx2", "title", "money"]
)

book = xlrd.open_workbook('data/doc_210369.xls', formatting_info=True)
sht = book.sheets()[0]

def human_money(value):
    assert isinstance(value, (float, int)), "wrong typ %r - %r" % (value, type(value))

    BB = 1000000000
    if value > BB:
        return '%4.2f B' % round(value / BB, 2)

    MM = 1000000
    if value > MM:
        return '%d M' % round(value / MM)

    if value > 1000:
        return '%d T' % round(value / 1000)

    return value


batch = []
codes = dict([
    line.split(' ', 1)
    for line in open('tag/tags')
])
regexps = dict([
    line.split(':', 1)
    for line in open('tag/regexps')
])
last_c = None
last_s = None
sum_out = {}
all_sum = 0
marked = 0
for row_n in range(sht.nrows):
    row = Money._make(sht.row(row_n)[:5])
    row_d = sht.row(row_n)
 
    if not row.idx1.value:
        continue

    inf_idx = sht.cell_xf_index(row_n, 1)
    inf = book.xf_list[inf_idx]
    font = book.font_list[inf.font_index]
   
    if font.italic:
        typ = 'subcategory'
        assert last_c
    elif font.bold:
        typ = 'category'
        last_c = row.idx1.value

        all_sum += (row.money.value * 1000)
    else:
        typ = 'ordinary'

    if isinstance(row.money.value, basestring):
        continue

    if typ != 'ordinary':
        continue

    title = codes.get(row.idx1.value, 0)
    if title:
        sum_out[title] = sum_out.get(title, 0) + (row.money.value * 1000)
        marked += (row.money.value * 1000)
        continue

    for reg, title in regexps.items():
        if not re.match(reg.decode('utf8'), row.title.value, re.U):
            continue

        sum_out[title] = sum_out.get(title, 0) + (row.money.value * 1000)
        marked += (row.money.value * 1000)
        break



for title, val in sum_out.items():
    print 'marked', human_money(val), val, title.strip()

print 'unmarked', human_money(all_sum - marked), '%4.2f' %(all_sum - marked), 'UNSP'
