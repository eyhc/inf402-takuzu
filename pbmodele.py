#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:10:29 2022

@authors: E. Carrot, L. De Mathan, A. Koshbas
"""

import math
import itertools
import es_dimacs


"""
    Classe modélisant un problème c'est à dire une grille et 
      une fnc correspondante
"""
class ProblemeModele:
    "Programme de conversion d'un probleme de takuzu en fichier dimacs"
    
    """
       Pour transformer un probleme au format dimac, il faut une grille
       La determination des clauses et faites également.
    """
    def __init__(self, grille):
        self.grille = grille    # on initialise la grille du problème
        self.clauses = []       # on définit un ensemble de clauses
        # nombre de variables d'un pb
        self.nb_variables = self.grille.taille * self.grille.taille
    
    
    """
        Determine le nombre théorique de clauses du problème
        Permet de faire un contrôle lorsqu'on a déterminé toutes les clauses
    """
    def nombreClauses(self):
        k = int(self.grille.taille / 2)
        r1 = 16 * k * (k - 1)                      # Nb clauses regle 1
        r2 = 8 * k * math.comb(2*k, k+1)           # Nb clauses regle 2
        r3 = k * (2*k-1) * int(math.pow(2, 2*k+1)) # Nb clauses regle 3
        return r1 + r2 + r3 + len(self.grille.cases)    # le total
    
    
    """
        Determiner l'ensemble des clauses du problème
    """
    def determinerClauses(self):
        # on vide
        self.clauses.clear()
        # On détermine les clauses de chaque règle
        self.determinerPremiereRegle()   # suivant la 1re regle
        self.determinerDeuxiemeRegle()   # suivant la 2e regle
        self.determinerTroisiemeRegle()  # suivant la 3e regle
        
        # On ajoute les clauses unitaires des cases de la grille deja remplies
        self.clauses += list(map(lambda x: [x], self.grille.cases))
    
    
    """
        Méthode qui calcule les clauses de la première règle :
            Il ne peut pas y avoir trois symboles identiques consecutifs
    """
    def determinerPremiereRegle(self):
        n = self.grille.taille
        g = self.grille
        
        for i in range(1, n+1):         # conjonction sur i de 1 à n
            for j in range (1, n-1):    # conjonction sur j de 1 à n-2
                # Cas des lignes
                self.clauses.append([   # des clauses U(i,j)+U(i,j+1)+U(i,j+2);
                    g.numeroCase(i, j),
                    g.numeroCase(i, j+1),
                    g.numeroCase(i, j+2)
                ])
                self.clauses.append([  # -U(i,j) + -U(i,j+1) + -U(i,j+2);
                    -g.numeroCase(i, j),
                    -g.numeroCase(i, j+1),
                    -g.numeroCase(i, j+2)
                ])
                # Cas des colonnes
                self.clauses.append([  # U(j,i) + U(j+1,i) + U(j+2,i)
                    g.numeroCase(j, i),
                    g.numeroCase(j+1, i),
                    g.numeroCase(j+2, i)
                ])
                self.clauses.append([  # et -U(j,i) + -U(j+1,i) + -U(j+2,i).
                    -g.numeroCase(j, i),
                    -g.numeroCase(j+1, i),
                    -g.numeroCase(j+2, i)
                ])
    
    
    """
        Méthode qui calcule les clauses de la deuxième règle :
            Il y a autant de 1 que de 0 sur chaque ligne et colonne
    """
    def determinerDeuxiemeRegle(self): 
        # On dertermine P(n,k)
        n = self.grille.taille
        k = int(n/2)
        P = list(itertools.combinations(range(1, n+1), k+1))
        
        # On dertermine les clauses
        g = self.grille
        for i in range(1, n+1):   # conjonction sur i de 1 à n
            for J in P:           # conjonction sur chaque combinaison
                c1 = []
                c2 = []
                c3 = []
                c4 = []
                for j in J:      # de la disjonction sur chaque elt de la comb.
                    # Cas des lignes
                    c1.append(g.numeroCase(i, j))   # des U(i,j)
                    c2.append(-g.numeroCase(i, j))  # des non U(i,j)
                    # Cas des colonnes
                    c3.append(g.numeroCase(j, i))   # des U(j,i)
                    c4.append(-g.numeroCase(j, i))  # des non U(j,i)
                
                # On ajoute ces clauses au problème
                self.clauses.append(c1)
                self.clauses.append(c2)
                self.clauses.append(c3)
                self.clauses.append(c4)
    
    
    """
        Méthode qui calcule les clauses de la troisième règle :
            Toutes les lignes et colonnes sont différentes
    """
    def determinerTroisiemeRegle(self):
        n = self.grille.taille
        g = self.grille
        
        for i in range(1, n+1):          # conjonction sur i de 1 à n
            for i2 in range(i+1, n+1):   # conjonction sur i2 de i+1 à n
                c1 = []
                c2 = []
                for j in range(1, n+1):  # disjonction des j de 1 à n
                    # Cas des lignes
                    c1.append([                # de la conjonction
                        [                          # de U(i,j) + U(i2,j)
                            g.numeroCase(i, j),
                            g.numeroCase(i2, j)
                        ],
                        [                         # et de -U(i,j) + -U(i2,j)
                            -g.numeroCase(i, j),
                            -g.numeroCase(i2, j)
                        ]
                    ])
                    # Cas des colonnes
                    c2.append([[                   # idem que ci-dessus mais
                            g.numeroCase(j, i),        # en sens inverse
                            g.numeroCase(j, i2)
                        ],
                        [
                            -g.numeroCase(j, i),
                            -g.numeroCase(j, i2)
                        ]
                    ])
                
                # On ajoute les clauses prealablement developpées
                self.clauses += self.developper(c1)
                self.clauses += self.developper(c2)
    
    
    """
        Developpe pour la regle 4
    """
    def developper(self, l):
        # On peut voir le developpement de X facteur comme le produit
        #  Cartesien sur les emsenbles des éléments de chaque facteur
        cart =  list(itertools.product(*l))
        
        # En effectuant le produit cartesien on a des tuples de liste d'entiers
        # On simplifie ça en listes
        simp = []               # ensemble des clauses simplifiée
        
        # pour chaque tuple representant une clause
        for clause in cart:
            c_simp = []         # la clause simplifiée
            
            # pour toutes les listes du tuple
            for lst in clause:
                # on ajoute les éléments de la liste dans c_simp
                c_simp += lst 
            
            # on ajoute la clause à l'ensemble (de clauses simplifiées)
            simp.append(c_simp)
        
        # et on retourne l'ensemble de clauses simplifiée
        return simp
    
    
    """
        Sortie dimacs
    """
    def sortieDimacs(self, nom_fichier):        
        # appel au module d'entrees/sorties dimacs
        es_dimacs.ecrireCNFDimacs(
            self.nb_variables,
            self.clauses,
            nom_fichier
        )
        