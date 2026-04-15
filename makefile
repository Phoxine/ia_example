create-venv:
	python3 -m venv .venv
.PHONY: create-venv

install:
	.venv/bin/pip install -r requirements.txt
.PHONY: install

run:
	.venv/bin/python main.py
.PHONY: run
