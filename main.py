#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:21:44 2022

@author: E. CARROT

POUR UTILISER CE FICHIER, SVP veuillez mettre le programme rsat dans le PATH
en l'installant par exemple ou en le téléchargeant et ajoutant le fichier rsat dans /bin ou tout autre répertoire du PATH

http://reasoning.cs.ucla.edu/rsat/download.php
"""

import sys
import os
from pbmodele import *
from satsolveur import *
from grille import *


"""
    Programme qui tâche de trouver une solution à un problème de Takuzu
"""


if __name__ == '__main__':
    if sys.argv.count("-h") != 0:
        print("Usage : python3 main.py [fichier.tkz] [-s] [-i]")
        print("Avec  :\n" + 
              "        -s : permet d'écrire les resultat de chaque operation dans des fichiers\n" +
              "        -i : permet d'utiliser le solveur du projet. Sinon veuillez à ce que rsat soit dans le path.")
        sys.exit(0)
    
    ECRIRE_SORTIE = False
    # Ecrire dans des fichiers
    if sys.argv.count("-s") != 0:
        ECRIRE_SORTIE = True
    
    # Initialisation de la grille initiale depuis le fichier donné en argument
    g = Grille()

    # Nom de fichier par defaut    
    doc_name = "probleme"
    
    # On construit la grille soit par argument soit par ligne de console
    if (len(sys.argv) > 1 and sys.argv[1] != "-s"
        and sys.argv[1] != "-i"):
        g.construireGrilleFichier(sys.argv[1])
        doc_name = sys.argv[1]
        doc_name = doc_name.replace(".tkz", "")
    else:
        g.construireGrilleClavier()
        
        # s'il y a une demande de sortie fichiers alors on demande un nom
        if ECRIRE_SORTIE:
            doc_name = input("Entrer le nom des fichiers (sans extension) : ")
        
        print("\n--------------------------------\n")
    
    #######################################################################
    #######################################################################
    
    # PARTIE AUTOMATIQUE
    
    print("Grille de jeu initiale :")
    g.ecrireGrille()
    
    
    ##############################
    #                            #
    #    PARTIE FORMALISATION    #
    #         DU PROBLEME        #
    #                            #
    ##############################
    print("\nFormalisation du problème       --> ", doc_name, ".dmcs", sep="")
    
    # on instancie le problème
    pb = ProblemeModele(g)
    pb.determinerClauses()
    
    # Vérifiaction du nombre de clauses obtenu
    nb_reel = len(pb.clauses)
    nb_theo = pb.nombreClauses()
    print("Nombre théorique de clauses : ", nb_theo)
    print("Nombre obtenu de clauses    : ", nb_reel)
    
    # Erreur : pas le bon nombre de clauses
    if nb_theo != nb_reel:
        print("Erreur lors de la formalisation :" +
              " pas le nombre attendu de clauses")
        sys.exit(2)
    
    # Ecrit l'ensemble des clauses dans un fichier dimacs
    if ECRIRE_SORTIE:
        pb.sortieDimacs(doc_name + ".dmcs")
    
    
    ##############################
    #                            #
    #     PARTIE RESOLUTION      #
    #                            #
    ##############################
    
    
    print("\nResolution du problème          --> ", doc_name, ".sol", sep="")
    
    ##############################
    #        SAT SOLVEUR         #
    #         DU PROJET          #
    ##############################
    if sys.argv.count("-i") != 0:
        
        solveur = SatSolveur(pb.clauses, pb.nb_variables)
        
        # On lance la resolution au plus 20 fois
        i = 0
        res = MAX_ITERATION
        while i != 20 and not solveur.estModele():
            res = solveur.lancerSolveur(P, MAX_ITERATION)
            i += 1
        
        # On ecrit le nb de tentatives
        print("Nombre de tentatives : ", i)
        
        # On regarde si c'est modele ou pas
        if solveur.estModele():  # Si oui on affiche le résultat

            print("Nombre de pas : ", res)
            l_grille = []
            
            # on transforme l'assignation en contraintes pour la grille
            for i in range(solveur.nb_variables):
                if solveur.assignation[i] == 1:
                    l_grille.append(i+1)
                else:
                    l_grille.append(-i-1)
            
            # on écrit la grille
            gs = Grille(g.taille, l_grille)
            gs.ecrireGrille()
            
            # On ecrit un fichier si demande
            if ECRIRE_SORTIE:
                solveur.ecrireSolution(doc_name + ".sol")
        
        else:
            print("Echec du solveur Sat")
    
    
    
    ##############################
    #       SAT SOLVEUR          #
    #       EXTERNE : RSAT       #
    ##############################
    else:
        # On écrit le fichier dans un fichier temp
        pb.sortieDimacs("temp")
        
        # On lance le solveur et on écrit la solution dans temp2
        os.system("rsat temp -s > temp2")
        
        # On recupère la conjonction des littéraux
        lit = es_dimacs.lireSAT("temp2")
        
        # si il n'y a aucun littéral pas de solution (à priori)
        if len(lit) == 0:
            print("Echec du solveur Sat")
            
        # sinon on affiche la grille solution
        else:
            gs = Grille(g.taille, lit)
            gs.ecrireGrille()
        
        # Suppression des fichiers
        os.system("rm temp temp2")
        
        # On sauvegarde si demandé
        if ECRIRE_SORTIE:
            es_dimacs.ecrireSAT(doc_name + ".sol", gs.cases)
        