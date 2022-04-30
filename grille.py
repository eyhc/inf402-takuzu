#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:42:19 2022

@author: Elie
"""

import re

"""
    Classe pour représenter une grille de Takuzu
"""
class Grille:
    
    """
        Constructeur naïf
    """
    def __init__(self, taille = 0, liste_cases = []):
        # On initialise les attributs
        self.taille = taille
        self.cases = liste_cases
    
    
    """
        Construit une grille avec saisie clavier
    """
    def construireGrilleClavier(self):
        # On lit la taille de la grille, le nombre de zero puis de un
        self.taille = int(input("Taille de la grille : "))
        nz = int(input("Entrer le nombre de 0 : "))
        nu = int(input("Entrer le nombre de 1 : "))
        
        # On lit ensuite toutes les cases déjà remplies
        if nu+nz != 0:
            print("Veuillez entrer", nu+nz ,"lignes en commmencant"+ 
              " par les zeros qui soient de la forme : x,y")
        for i in range(nu+nz):
            # On récupère les deux coordonnées et on ajoute
            cp = input()
            self.ajouterCase(cp, i < nz)
    
    
    """
        Construit une grille qui lit toute les entrées dans le fichier fournies
        Le format à respecter est expliqué dans le fichier ci-dessous:
            - Première ligne la taille du jeu (n)
            - Deuxième ligne le nombre de 0 (nz)
            - Troisième ligne le nombre de 1 (nu)
            - Il a y ici nz+nu lignes de la forme i,j
                où i entre 1 et n represente l'abscisse de la case
                et j entre 1 et n represente l'ordonnee de la case'
    """
    def construireGrilleFichier(self, fichier_entree):
        # Ouverture du fichier
        f = open(fichier_entree)
        
        # Taille de la grille
        self.taille = int(f.readline())
        
        # On recupère nz et nu
        nz = int(f.readline())
        nu = int(f.readline())
        
        # On traite chaque case
        for i in range(nz+nu):
            # On lit et on ajoute la case
            cp = f.readline()
            self.ajouterCase(cp, i < nz)
        
        # On 
        f.close()

    """
        Ecrit à l'écran la grille de jeu
    """
    def ecrireGrille(self):
        # une ligne horizontal
        ligne = "-"
        for _ in range(self.taille):
            ligne += "----"
        print(ligne)
        
        # on parcours le tableau
        for i in range(1, self.taille+1):
            for j in range(1, self.taille+1):
                # Cas d'une case remplie par un 1
                if self.cases.count(self.numeroCase(i, j)) != 0:
                    print('| 1 ', end="")
                # Cas d'une case remplie par un 0
                elif self.cases.count(-self.numeroCase(i, j)) != 0:
                    print('| 0 ', end="")
                # Cas d'une case non remplie
                else:
                    print('|   ', end="")
            print('|')
            print(ligne)
    
    
    """
        Ajoute un un ou un zero dans la case représenté par la chaine "i,j"
    """
    def ajouterCase(self, chaine, zero):
        # on recupère les deux morceaux avec une expression regulière
        cp = re.findall("[0-9]+", chaine)
        # On traite les cas des zeros et uns
        v = self.numeroCase(int(cp[0]), int(cp[1]))
        if v <= self.taille * self.taille:
            if zero:
                self.cases.append(-v)
            else:
                self.cases.append(v)
    
    
    """
        Méthode qui donne le numero de la variable associé à la case (x,y)
    """
    def numeroCase(self, x, y):
        # pour que les cases soient numéroté de 1 à n*n
        return (x-1) * self.taille + y
    
