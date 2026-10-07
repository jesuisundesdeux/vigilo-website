HUGO ?= hugo

all: help

help: ## Show this help
	@grep -E "^[a-z-]+:.*##" Makefile | sed 's/:.*##/\t/'

node_modules: package.json
	npm install
	@touch node_modules

data: ## Fetch the instances from vigilo-conf (and their API)
	python3 scripts/fetch_instances.py

doc-backend: ## Update the upgrade documentation from vigilo-backend
	curl -sSfL https://raw.githubusercontent.com/jesuisundesdeux/vigilo-backend/master/doc/UPGRADE.md -o /tmp/UPGRADE.md
	cat content/documentation/upgrade/_index.fr.tpl /tmp/UPGRADE.md > content/documentation/upgrade/_index.fr.md

generate: node_modules data ## Build the site in public/
	$(HUGO) --gc --minify --cleanDestinationDir

serve: node_modules data ## Local server with live reload (http://localhost:1313)
	$(HUGO) server

.PHONY: all help data doc-backend generate serve
