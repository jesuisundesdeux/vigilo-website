VERSION := 0.55.4
IGNOREURL := "/getgrav.org/,/vigilo.jesuisundesdeux.org/"
makefile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
pwd := $(dir $(makefile_path))

HUGO := docker run --rm -it -v $(pwd):/src -v $(pwd)/public:/target -p 1313:1313 klakegg/hugo:${VERSION}
CMD := docker run --rm -it -v $(pwd):/src -v $(pwd)/public:/target alpine

all: help

help:
	@grep "##" Makefile | grep -v "@grep"

themes/hugo-theme-learn:
	git clone https://github.com/badele/hugo-theme-learn.git themes/hugo-theme-learn

version: ## Show hugo version
	docker run --rm -it klakegg/hugo:${VERSION} version

generate: clean themes/hugo-theme-learn ## Generate pages content
	${HUGO} --debug --cleanDestinationDir

serve: themes/hugo-theme-learn ## Emulate web server
	${HUGO} server --buildDrafts --buildExpired --buildFuture --disableFastRender

test: generate ## Test generated webpage
	docker run -v $(pwd)/public:/site 18fgsa/html-proofer /site --allow_hash_href --url-ignore "${IGNOREURL}"

clean:
	${CMD} rm -rf /target/*