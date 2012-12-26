# encoding: utf8

import sys

from consoleargs import command
from marker import do_marker
from diff import do_differ

@command
def main(cmd, *a):
    do = {
        "mark": do_marker,
        "diff": do_differ,
    }
    if cmd not in do:
        print 'unknown command %r, commads: %s' % (
                cmd, str.join(", ", do.keys())
        )
        return sys.exit(1)

    handle = do.get(cmd)
    handle(*a)


