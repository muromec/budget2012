from consoleargs import command
from parser import Parser
from tags import Tags

@command(argv=False)
def do_differ(budget, last_budget):
    print budget, last_budget
    tagger = Tags()
    for_diff = {}
    for code in tagger.codes:
        for_diff[code] = []

    for path in [budget, last_budget]:
        parser = Parser(path)
        for row, typ in parser:
            ct = for_diff.get(row.idx1.value)
            if not (ct is None):
                ct.append([row,typ])

        print parser, path

    for code, entries in for_diff.items():
        origin, typ = entries[0]
        for other, otyp in entries[1:]:
            
            if origin.title.value != other.title.value:
                print code
                print origin.title.value
                print other.title.value
                print '=='
