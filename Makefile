
URL = 'http://w1.c1.rada.gov.ua/pls/zweb2/webproc34?id=&pf3511=41157&pf35401=210369'

URL_2013_OUT = 'http://w1.c1.rada.gov.ua/pls/zweb_n/webproc34?id=&pf3511=44897&pf35401=238679'

all: data/doc_210369.xls data/b2013_out.xls env/bin/python
	env/bin/rada mark -r $<

env/bin/python:
	python -m virtualenv env
	env/bin/pip install -r requirements.txt
	env/bin/pip install .

data/doc_210369.xls:
	[ -d data ] || mkdir data
	wget $(URL) -O $@

data/b2013_out.xls:
	[ -d data ] || mkdir data
	wget $(URL_2013_OUT) -O $@


clean:
	rm -rf env data

mark: data/doc_210369.xls env/bin/python
	env/bin/rada $<
