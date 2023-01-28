# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 21:11:27 2022

@author: matth
dans la contrab : 30 17 * * * python3 /home/pi/telechargement_1fichier/check_nouvelle_series.py >> /dev/null 2>&1
"""


import requests
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import subprocess

file_path = os.path.dirname(os.path.abspath(__file__))

urlSite="https://www.wawacity.tech/?p=series&s=vostfr-hq"
domaine=urlSite.rsplit('/',1)[0]

urlDiscord='URL webhook discord'

webhook = DiscordWebhook(url=urlDiscord)


def sendMessageDiscord (message, urlDiscord):
    webhook = DiscordWebhook(url=urlDiscord, content=message)
    webhook.execute()


def get_derniere_serie():
    with open(file_path+'/derniere_serie.txt', 'r') as fichier:
        contenu = fichier.read()
    return contenu


def set_derniere_serie(nom):
    with open(file_path+'/derniere_serie.txt', 'w') as fichier:
        fichier.write(nom)


### DEBUT DU SCRIPT ###

derniere_serie=get_derniere_serie()

date = datetime.datetime.now().strftime("%a %d %b %Y")
message=""


try:
    o = requests.get(urlSite)
except:
    webhook = DiscordWebhook(url=urlDiscord, content="Erreur dans l'ouverture de l'url wawacity")
    webhook.execute()
else:
    s = o.text
    s=s.split('<div class="container-fluid" id="main-body">',1)[1]
    s=s.split('<div class="wa-block">',1)[1]
    series=s.split('<div class="wa-sub-block wa-post-detail-item">')[1:]

    compteur=0
    premier = True

    for serie in series:
        nom = serie.split('<div class="wa-sub-block-title">')[1].split('</i>',1)[1].split('<i>')[0][1:]
        
        if premier:
            new_derniere_serie = nom
            premier = False
        
        if (not(nom in derniere_serie)):
            compteur+=1
            image = domaine + serie.split('" class="img-responsive">')[0].rsplit('src="')[1]
            lien = domaine +'/'+ serie.split('<a href="')[1].split('">')[0]

            message+=nom+"  "+image+"   "+lien+"\n"

            embed = DiscordEmbed(
                title=nom, url=lien
            )

            embed.set_image(url=image)

            webhook.add_embed(embed)
        else: break
        
        #un message embed discord peut avoir max 10 élèments permet d'envoyer une partie avant d'overflow
        if compteur >=9:
            compteur=0
            webhook.execute(remove_embeds=True)
              
    webhook.execute(remove_embeds=True)

    set_derniere_serie(new_derniere_serie)
