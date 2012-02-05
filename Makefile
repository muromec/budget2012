
URL = 'http://w1.c1.rada.gov.ua/pls/zweb2/webproc34?id=&pf3511=41157&pf35401=210369'

all: data/doc_210369.xls bin/python
	bin/python rada.py

bin/python:
	python -m virtualenv .
	bin/pip install -r requirements.txt

data/doc_210369.xls:
	[ -d data ] || mkdir data
	wget $(URL) -O $@


clean:
	rm -rf bin lib include share data

mark: data/doc_210369.xls bin/python
	bin/python rada_explain.py
