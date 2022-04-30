#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 17:41:36 2022

@author: elie
"""

from satsolveur import *
import sys

if __name__ == '__main__':
    
    if len(sys.argv) < 4:
        print("Usage : python3 " + sys.argv[0] + " fichier nb_tests nb_max_pas")
        sys.exit(1)
    
    # Constantes
    fichier = sys.argv[1]
    nb = int(sys.argv[2])
    max_pas = int(sys.argv[3])
    probas = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] # valeur à tester
    
    # Creation du solveur
    solv = SatSolveur()
    solv.lireClausesFichier(fichier)
    
    # Affichage des paramètres
    print("Fichier de test : " + fichier)
    print("Nombre de tests par valeur de P : " + str(nb))
    print("Nombre de pas maximum de l'algorithme : " + str(max_pas) + "\n")
    
    # Affichage des résultats (entete)
    print("P\t\tSUCCES\t\tPAS MOY\t\tPAS MOY TOT")
    
    # Execution de tous les tests
    for p in probas:
        somme = 0
        somme_reu = 0
        reu = 0
        for _ in range(nb):
            res = solv.lancerSolveur(p, max_pas)
            if res < max_pas:
                reu += 1
                somme_reu += res
            somme += res
        
        # affichage des données
        pas_moy_reu = -1
        if reu != 0:
            pas_moy_reu = somme_reu/reu
        
        print(str(p)
              + "\t\t" + str(round(reu*100/nb, 2))
              + "\t\t" + str(round(pas_moy_reu, 2))
              + "\t\t" + str(round(somme/nb, 2)))