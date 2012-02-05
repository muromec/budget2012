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


