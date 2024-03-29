#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import shutil
import urllib.request

CITYLIST="https://raw.githubusercontent.com/jesuisundesdeux/vigilo-conf/main/main/citylist.json"

countries = {
    "France": "fr",
    "Belgique": "be"
}

REMOVE_SYMBOLS_ACCENTS = {
    'a':[u'â',u'à'],
    'c':[u'ç'],
    'e':[u'è',u'ê',u'é',u'ë'],
    'i':[u'ï',u'î'],
    'o':[u'ö',u'ô'],
    'u':[u'û',u'ü'],
    '-': ['-','\'','"','/','.']
    }

MAKEFILE_ACTION="make generate-cities-content"

def normalize(text):
    text = text.lower()

    # Remove accent
    for c in iter(REMOVE_SYMBOLS_ACCENTS):
        for r in REMOVE_SYMBOLS_ACCENTS[c]:
            text = text.replace(r,c)

    # Remove multiple spaces
    text = "-".join(text.split())

    text = re.sub(r'<BR.*?>', ' ', text,flags=re.MULTILINE)
    text = text.replace('PAS DE SAISIE','')

    text = text.strip()

    return text

def protectEmail(email):
    email = email.replace("@"," ✉ ")
    email = email.replace("."," ⊙ ")

    return email

def downloadFile(url):

    try:
      response = urllib.request.urlopen(url, timeout=10)
      data = response.read()
      text = data.decode('utf-8')
      return text
    except Exception as err:
      print('skip')
      return False;


def createContentForCity(key, city_info, scope_info):
    foldername = normalize("%s-%s" % (scope_info['display_name'],countries[city_info['country']]))

    version = 'Beta'
    if city_info['prod']:
        version = 'inconnue'
        if 'backend_version' in scope_info:
            version = scope_info['backend_version']

    contact_info = ""
    if 'contact_email' in scope_info and scope_info['contact_email']!='':
        contact_info = "- **Contact:** %s" % protectEmail(scope_info['contact_email'])

    carte_info = ""
    if 'map_url' in scope_info and scope_info['map_url']!='':
        carte_info = "- **Carte:** %s" % scope_info['map_url']

    api_scope = "- **Scope info:** %s/get_scope.php?scope=%s" % (city_info['api_path'],city_info['scope'])

    opendata = '- **Données ouvertes:** <a href="%s/get_issues.php?scope=%s&format=json">JSON</a> - <a href="%s/get_issues.php?scope=%s&format=geojson">GeoJSON</a> - <a href="%s/get_issues.php?scope=%s&format=csv">CSV</a>' % (city_info['api_path'],city_info['scope'],city_info['api_path'],city_info['scope'],city_info['api_path'],city_info['scope'])
    content = """---
title: %s (%s)
---
{{%% vigilo-map-url "%s" %%}}

{{%% vigilo-stats "%s" %%}}

{{%% get_issues "%s" "&scope=%s" %%}}


## Informations complémentaires

%s
%s
%s
%s
""" % (
    scope_info['display_name'],
    version,
    scope_info['map_url'],
    key,
    city_info['api_path'],
    city_info['scope'],
    contact_info,
    carte_info,
    api_scope,
    opendata
    )


    # Write content
    foldercontent = "content/villes/%s" % foldername
    os.makedirs(foldercontent,exist_ok=True)
    with open("%s/_index.fr.md" % foldercontent, 'w') as f:
        f.write(content)

    # Add folder to gitignore
    with open(".gitignore", 'a+') as f:
        gitignoreline = "# Add from %s\n%s\n\n" % (MAKEFILE_ACTION,foldercontent)
        f.write(gitignoreline)


if __name__ == "__main__":
    data = downloadFile(CITYLIST)
    jcity = json.loads(data)

    # Init .gitignore
    shutil.copyfile(".gitignore.tpl", ".gitignore")

    # Get cities informations
    for k in jcity:
        city_info = jcity[k]
        city_info['api_path'] = city_info['api_path'].replace('%3A%2F%2F','://')

        if city_info['prod']:
            print(k)
            # Get scope information
            data = downloadFile("%s/get_scope.php?scope=%s" % (city_info['api_path'],city_info['scope']))
            if data:
              scope_info = json.loads(data)
              createContentForCity(k, city_info,scope_info)
           
