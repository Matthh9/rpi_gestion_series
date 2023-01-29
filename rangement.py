# -*- coding: utf-8 -*-
"""
Created on Tue Feb 8 05:34:05 2022

@author: matth

lancement manuel : python3 /home/pi/telechargement_1fichier/rangement.py /media/pi/cloud/Films/telechargement/
"""
import sys
import os
import re
from pathlib import Path

if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        cheminTelechargement=sys.argv[1]
        cheminRangement=cheminTelechargement.rsplit('/',2)[0]+'/TV Shows/'
        cheminRangementFilm=cheminTelechargement.rsplit('/',2)[0]+'/Movies/'
        
        files = [_ for _ in os.listdir(cheminTelechargement) if _.endswith((".avi", ".mkv", ".mp4"))]
        for name in files:
                # try car s'il y a une erreur on considère que c'est un film et pas une série 
            try:
                #print(name)
                [newName,extension]=name.rsplit('.',1)
                
                #permet de retirer l'année du titre de la série
                newName=re.sub("20[0-9]{2}.", "", newName) 
                
                #recherche la chaine : commençant par S puis au moins 1 nombre puis un point ou non puis E puis au moins 1 nombre
                resultatSearch=re.search("[Ss][0-9]+[\.]?[Ee][0-9]+", newName)
                #recupère la chaine précédemment recherché, retire le . s'il est présent et force la majuscule pour les lettres
                saisonEpisode=resultatSearch.group().replace('.','').upper()
                
                #on récupère uniquement le titre de la série
                newName=newName[:resultatSearch.span()[0]-1].upper()
                
                saison=re.search("S[0-9]+", saisonEpisode).group()
                
                #creation des dossiers pour le rangement
                Path(cheminRangement+newName+'/'+saison).mkdir(parents=True, exist_ok=True)
                
                #deplacer le fichier
                os.rename(cheminTelechargement+name, cheminRangement+newName+'/'+saison+'/'+newName+'.'+saisonEpisode+'.'+extension)
            except:
                os.rename(cheminTelechargement+name, cheminRangementFilm+name)
                pass
