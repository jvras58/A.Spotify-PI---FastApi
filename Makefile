SHEll := /bin/zsh
.PHONY: venv

venv:
	poetry run poetry install

start:
	poetry run python app/startup.py
