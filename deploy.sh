#!/bin/bash

set -e

echo $GITHUB_AUTH_SECRET > ~/.git-credentials && chmod 0600 ~/.git-credentials
git config --global credential.helper store
git config --global user.email "vigilo-wrbsite-bot>@users.noreply.github.com"
git config --global user.name "Vigilo website bot"
git config --global push.default simple

rm -rf deployment
git clone -b master https://github.com/jesuisundesdeux/vigilo-website.git deployment
rsync -av --delete --exclude ".git" public/ deployment

cd deployment

# Generate preview - 1
curl -Lo preview.png "https://manet.herokuapp.com/?url=vigilo.city%2Ffr%2Fvilles%2Fmontpellier&clipRect=0%2C0%2C1024%2C1200"
cp ../README.md . 

ls -alh 

git add -A
# we need the || true, as sometimes you do not have any content changes
# and git woundn't commit and you don't want to break the CI because of that
git commit -m "Regeneration du site. Commit ${TRAVIS_COMMIT} le $(date)" || true
git push

cd ..
rm -rf deployment