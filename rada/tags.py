class Tags(object):
    def __init__(self, dirname='tag'):
        codes_order = [
            line.split(' ', 1)
            for line in open('tag/tags')
        ]

        self.codes_titles = []
        for idx, title in codes_order:
            if title not in self.codes_titles:
                self.codes_titles.append(title)

        self.codes = dict(codes_order)
        self.regexps = dict([
            line.split(':', 1)
            for line in open('tag/regexps')
        ])
