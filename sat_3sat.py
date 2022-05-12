#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:10:32 2022

@authors: E. Carrot, L. De Mathan, A. Koshbas 
"""

import es_dimacs

class Sat3SAT:
    "Programme de conversion d'un fichier dimacs sat en dimacs 3-sat"
    
    
    """
        Constructeur naïf
    """
    def __init__(self, clauses = [], nb_variables = 0):
        self.nb_variables = nb_variables
        self.clauses = clauses
        self.clauses_simplifiees = []
    
    
    """
        Affecte à l'objet courant l'ensemble de clauses non simplifiée
            qui se trouvent dans un fichier dimacs
    """
    def lireClausesFichier(self, nom_fichier):
        # On utilise le module es_dimacs
        u = es_dimacs.lireCNFDimacs(nom_fichier)
        self.nb_variables = u[0]
        self.clauses = u[1]
        
        
    """
        Fonction principale qui convertit l'ensmeble de clauses de l'objet
            en un ensemble de clauses à trois littéraux
    """
    def conversion(self):
        # On effectue la conversion sur chaque clause
        for clause in self.clauses:
            # longeur de la clause
            k = len(clause)
            
            # Clause de taille 1
            if k == 1:
                # on ajoute deux variables
                y1 = self.nb_variables + 1
                y2 = y1 + 1
                
                self.nb_variables += 2
                
                # on ajoute les quatre clauses équivalentes (cf exo 51)
                self.clauses_simplifiees.append([clause[0], y1, y2])
                self.clauses_simplifiees.append([clause[0], y1, -y2])
                self.clauses_simplifiees.append([clause[0], -y1, y2])
                self.clauses_simplifiees.append([clause[0], -y1, -y2])
                
            # Clause de taille 2
            elif k == 2:
                # on ajoute une variable
                y1 = self.nb_variables + 1
                self.nb_variables += 1
                
                # on ajoute les deux clauses équivalentes (cf exo 51)
                self.clauses_simplifiees.append([clause[0], clause[1], y1])
                self.clauses_simplifiees.append([clause[0], clause[1], -y1])
                
            # Clause de taille 3
            elif k == 3:
                # rien à faire (cf exo 51)
                self.clauses_simplifiees.append(clause)
            
            # Clause de taille supérieure à 3 : aïe !
            else:
                # premiere variable suplementaire
                yi = self.nb_variables + 1
                
                # premiere 3-clause : z1 + z2 + -y1 (cf exo 51) 
                self.clauses_simplifiees.append([clause[0], clause[1], yi])
                
                # Pour toutes les clauses "au milieu"
                for i in range(1, k-3):
                    # (i+1)-eme 3-clause : -yi + z(i+2) + -yi (cf exo 51) 
                    self.clauses_simplifiees.append(
                        [-yi, clause[i+1], yi + 1]
                    )
                    yi += 1
                
                # derniere 3-clause : y(k-3) + z(k-1) + zk (cf exo 51) 
                self.clauses_simplifiees.append(
                    [-yi, clause[k-2], clause[k-1]]
                )
                
                self.nb_variables += k-3     # on a k-3 variables de plus
                
        
        
    """
        Ecrit le contenu l'objet courant dans un fichier en utilisant
            le format dimacs
    """
    def sortieDimacs(self, nom_fichier):
        # On appelle le module es_dimacs simplement
        es_dimacs.ecrireCNFDimacs(
            self.nb_variables,
            self.clauses_simplifiees,
            nom_fichier
        )
    
