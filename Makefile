VERSION := 0.55.4
FILEIGNORE := "/site/fr/api/index.html/"
makefile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
pwd := $(dir $(makefile_path))

HUGO := docker run --rm -it -v $(pwd):/src -v $(pwd)/public:/target -p 1313:1313 klakegg/hugo:${VERSION}
HTMLPROOFER := docker run -v $(pwd)/public:/site 18fgsa/html-proofer /site --allow_hash_href --disable-external true --file-ignore "${FILEIGNORE}"
CMD := docker run --rm -it -v $(pwd):/src -v $(pwd)/public:/target alpine

all: help

help:
	@grep "##" Makefile | grep -v "@grep"

themes/hugo-theme-learn:
	git clone https://github.com/badele/hugo-theme-learn.git themes/hugo-theme-learn

version: ## Show hugo version
	docker run --rm -it klakegg/hugo:${VERSION} version

doc-backend:
	rm -rf /tmp/vigilo-backend
	git clone https://github.com/jesuisundesdeux/vigilo-backend.git /tmp/vigilo-backend
	cp content/api/_index.fr.tpl content/api/_index.fr.md
	cat /tmp/vigilo-backend/doc/REST_API.md >> content/api/_index.fr.md


generate-cities-content: ## generate-cities-content
	python3 get_city_informations.py

generate: clean themes/hugo-theme-learn doc-backend generate-cities-content ## Generate pages content
	${HUGO} --debug --cleanDestinationDir

serve: themes/hugo-theme-learn doc-backend generate-cities-content ## Emulate web server
	${HUGO} server --buildDrafts --buildExpired --buildFuture --disableFastRender

test: generate ## Test generated webpage
	${HTMLPROOFER}

clean:
	${CMD} rm -rf /target/*
