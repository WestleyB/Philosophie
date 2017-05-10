#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode
from pprint import pprint
from urllib.parse import unquote
from urllib.parse import urldefrag
import re

#  globale cache
cache = {}

# Si vous écrivez des fonctions en plus, faites-le ici


def getJSON(page):
    params = urlencode({
      'format': 'json',
      'action': 'parse',
      'prop': 'text',
      'redirects': True,
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"
    response = urlopen(API + "?" + params)
    return response.read().decode('utf-8')


def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']
        content = parsed['parse']['text']
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None


def getPage(page):
    try:
        title, content = getRawPage(page)
        if title is not None or content is not None:
            title = title.replace("_"," ")
            soup = BeautifulSoup(content['*'], 'html.parser')
            list_href = []
            # Recherche des liens dans la page
            for link in soup.find_all("p", recursive=False):
                for sublink in link.find_all("a"):
                    if re.search("^\/wiki\/\w*", sublink.get('href')):
                        # filtrer les pages hors de l’espace de noms principal de Wikipédia
                        if re.search("/w*:/w*", sublink.get('href')) is None and re.search("API_", sublink.get('href')) is None:
                            clean_link = unquote(urldefrag(sublink.get('href'))[0])[6:]
                            if clean_link != '':
                                clean_link = clean_link.replace('_', ' ')
                                if clean_link not in list_href:
                                    list_href.append(clean_link)
            return title, list_href[:10]
        else:
            return None, []
    except TypeError:
        return None, []




if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")

    # Voici des idées pour tester vos fonctions :
    #pprint(getJSON("Utilisateur:A3nm/INF344"))
    #pprint(getJSON("philosophique"))
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Histoire"))
