import xlrd
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
        return '%d B' % round(value / BB)

    MM = 1000000
    if value > MM:
        return '%d M' % round(value / MM)

    if value > 1000:
        return '%d T' % round(value / 1000)

    return value


batch = []
for row_n in range(sht.nrows):
    row = Money._make(sht.row(row_n)[:5])
    row_d = sht.row(row_n)

    inf_idx = sht.cell_xf_index(row_n, 1)
    inf = book.xf_list[inf_idx]
    font = book.font_list[inf.font_index]
    
    if font.italic:
        typ = 'subcategory'
    elif font.bold:
        typ = 'category'
    else:
        typ = 'ordinary'

    if not row.idx1.value:
        continue

    if isinstance(row.money.value, unicode):
        continue

    batch.append((typ,row))

batch = sorted(batch, key=lambda (t,x): x.money.value)
for typ, row in reversed(batch):
    money = human_money(row.money.value * 1000)
    print typ, row.title.value.encode('utf8'), money

all_b = sum([
        row.money.value
        for typ, row in batch
        if typ == 'category' and \
                row.money.value < 1000000
])
print human_money(all_b * 1000)
