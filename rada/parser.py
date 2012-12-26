import xlrd
import collections
Money = collections.namedtuple("Money", 
        ["wtf1", "idx1", "idx2", "title", "money"]
)

class Parser(object):
    def __init__(self, fname):
        self.book = xlrd.open_workbook(fname, formatting_info=True)
        self.sht = self.book.sheets()[0]

    def go(self):
        pass

    def __iter__(self):
        for row_n in range(self.sht.nrows):
            row_d = self.sht.row(row_n)
            row = Money._make(row_d[:5])

            if not row.idx1.value:
                continue

            inf_idx = self.sht.cell_xf_index(row_n, 1)
            inf = self.book.xf_list[inf_idx]
            font = self.book.font_list[inf.font_index]
           
            if font.italic:
                typ = 'subcategory'
            elif font.bold:
                typ = 'category'
            else:
                typ = 'ordinary'

            if isinstance(row.money.value, basestring):
                continue

            yield row, typ

