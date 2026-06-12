APP ?= apps/sample_tool
APPID ?=
NAME ?=
CATEGORY ?= Tools
AUTHOR ?= Unknown
DESCRIPTION ?= Generated Flipper Zero app
VERSION ?= 0.1

.PHONY: help scaffold validate lint build launch catalog

help:
	@printf '%s\n' \
		'Targets:' \
		'  make scaffold APPID=my_tool NAME="My Tool" CATEGORY=Tools AUTHOR="Your Name" DESCRIPTION="Short description"' \
		'  make validate APP=apps/my_tool' \
		'  make lint APP=apps/my_tool' \
		'  make build APP=apps/my_tool' \
		'  make launch APP=apps/my_tool   # human-approved hardware run only' \
		'  make catalog APP=apps/my_tool ORIGIN=https://github.com/owner/repo.git COMMIT_SHA=<sha>'

scaffold:
	@test -n "$(APPID)" || (echo 'APPID is required' && exit 2)
	@test -n "$(NAME)" || (echo 'NAME is required' && exit 2)
	python3 scripts/new_app.py --appid "$(APPID)" --name "$(NAME)" --category "$(CATEGORY)" --author "$(AUTHOR)" --short-description "$(DESCRIPTION)" --version "$(VERSION)"

validate:
	python3 scripts/validate_app.py "$(APP)"

lint:
	cd "$(APP)" && ufbt lint

build:
	cd "$(APP)" && ufbt

launch:
	@printf '%s\n' 'Hardware launch requested. Review generated code first; this target runs ufbt launch against a connected Flipper.'
	cd "$(APP)" && ufbt launch

catalog:
	@test -n "$(ORIGIN)" || (echo 'ORIGIN is required' && exit 2)
	@test -n "$(COMMIT_SHA)" || (echo 'COMMIT_SHA is required' && exit 2)
	python3 scripts/catalog_manifest.py "$(APP)" --origin "$(ORIGIN)" --commit-sha "$(COMMIT_SHA)"
