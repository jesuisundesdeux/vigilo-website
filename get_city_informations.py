#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import urllib.request

CITYLIST="https://vigilo-bf7f2.firebaseio.com/citylist.json"

def downloadFile(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')

    return text

if __name__ == "__main__":
    data = downloadFile(CITYLIST)
    jcontent = json.loads(data)
    
    for k in jcontent:
        print(k)
