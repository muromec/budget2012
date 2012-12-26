import re

from consoleargs import command
from utils import human_money
from parser import Parser
from tags import Tags

def print_unmarked(names, sum_unmarked):
    for idx, val in sum_unmarked.items():
        if not val:
            continue

        print 'unmarked', human_money(val), val, names[idx].strip().encode('utf8')

def print_unmarked_sum(all_sum, marked):
    print 'unmarked', human_money(all_sum - marked), '%4.2f' %(all_sum - marked), 'Untagged'


class RawMarker(object):
    def __init__(self):
        self.tagger = Tags()

        self.sum_out = {}
        self.sum_unmarked = {}

        self.names = {}
        self.all_sum = 0
        self.marked = 0

    def __call__(self, row, typ):
        self.last(typ, row.idx1.value)

        handle = getattr(self, 'handle_%s' % typ, None)
        if callable(handle):
            handle(row)

        self.names[row.idx1.value] = row.title.value

    def last(self, typ, val):
        setattr(self, 'last_%s' % typ, val)

    def handle_category(self, row):
        self.all_sum += (row.money.value * 1000)
        self.sum_unmarked[row.idx1.value] = (row.money.value * 1000)

class Marker(RawMarker):

    def handle_ordinary(self, row):
        title = self.tagger.codes.get(row.idx1.value, 0)

        if title:
            self.mark_money(title, row.money.value * 1000)
            return

        for reg, title in self.tagger.regexps.items():
            if not re.match(reg.decode('utf8'), row.title.value, re.U):
                continue

            self.mark_money(title, row.money.value * 1000)
            return

    def mark_money(self, title, money):
        self.sum_out[title] = self.sum_out.get(title, 0) + money
        self.marked += money
        self.sum_unmarked[self.last_category] -= money


@command(argv=False)
def do_marker(budget, unmarked=False, raw=False):
    parser = Parser(budget)
    parser.go()

    marker = RawMarker() if raw else Marker()

    for row, typ in parser:
        marker(row, typ)

    for title in marker.tagger.codes_titles:
        val = marker.sum_out.get(title)
        if not val:
            continue

        print 'marked', human_money(val), val, title.strip()

    if unmarked or raw:
        print_unmarked(marker.names, marker.sum_unmarked)
    else:
        print_unmarked_sum(marker.all_sum, marker.marked)
