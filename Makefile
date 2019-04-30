VERSION := 0.55.4
IGNOREURL := "/getgrav.org/"
makefile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
pwd := $(dir $(makefile_path))

HUGO := docker run --rm -it -v $(pwd):/src -v $(pwd)/docs:/target -p 1313:1313 klakegg/hugo:${VERSION}

all: help

help:
	@grep "##" Makefile | grep -v "@grep"

themes/hugo-theme-learn:
	git clone git@github.com:matcornic/hugo-theme-learn.git

version: ## Show hugo version
	docker run --rm -it klakegg/hugo:${VERSION} version

generate: themes/hugo-theme-learn ## Generate pages content
	${HUGO} --debug --cleanDestinationDir

serve: ## Emulate web server
	${HUGO} server --buildDrafts --buildExpired --buildFuture --disableFastRender

test: generate ## Test generated webpage
	docker run -v $(pwd)/docs:/site 18fgsa/html-proofer /site --allow_hash_href --url-ignore "${IGNOREURL}"