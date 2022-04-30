#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 22:15:49 2022

@authors: E. Carrot, L. De Mathan, A. Koshbas
"""

import es_dimacs
import random
import math


MAX_ITERATION = 600
P = 0.4


"""
    SAT SOLVEUR DU TYPE WALKSAT
    ATTENTION POUR LE BON FONCTIONNEMENT, 
    NE PAS MODIFIER L'ASSIGNATION DIRECTEMENT
"""
class SatSolveur:
    "Programme naif de Sat Solveur"
    
    
    """
        Constructeur naïf
    """
    def __init__(self, clauses = [], nb_variables = 0):
        # On initialise les attributs
        self.nb_variables = nb_variables        # Le nombre de variables
        self.clauses = clauses                  # L'ensemble de clauses
        self.assignation = [0] * nb_variables   # Une assignation
        self.clauses_insatisfaites = []         # Des clauses non satisfaites
        self.trouveClausesInsatisfiable()            #   par l'assignation
    
    
    """
        Affecte à l'objet courant l'ensemble de clauses non simplifiée
            qui se trouvent dans un fichier dimacs
    """
    def lireClausesFichier(self, nom_fichier):
        # On utilise le module es_dimacs
        u = es_dimacs.lireCNFDimacs(nom_fichier)
        self.nb_variables = u[0]
        self.clauses = u[1]
        self.assignation = [0] * self.nb_variables
        self.trouveClausesInsatisfiable()      # !! on a modifié l'assignation
        
        
    """
        Fonction principale trouve (ou essaie) un modele à un ensemble de
            clauses
    """
    def lancerSolveur(self, p, max_it):
        # On determine une assignation aleatoire
        v = self.assignationAleatoire()
        
        # On cherche un modele, tant que ce n'est pas le cas
        i = 0
        while not self.estModele() and i < max_it:
            # On prend une clause insatisfaite
            c = self.choixClauseInsatisfaiteAleatoire()
            # On prend une variable aleatoire
            x = random.random()
            # Suivant si x est ordonne par rapport à la probabilite
            if x <= p:
                # Choix aleatoire d'une variable à modifier
                y = self.choixVariableAleatoire(c)
            else:
                # Choix stratégique d'une variable à modifier
                y = self.choixVariableDeterministe(c)
            # On change l'assignation en consequence
            self.changeValeurAssignation(y)
            i += 1 # Et on recommence
        
        # On retourne le nombre de pas
        return i
            
        
    """
        Retourn vrai ssi l'assignation est un modèle de l'ensemble de clauses
    """
    def estModele(self):
        # On est modele si toutes les clauses sont satisfaites
        return len(self.clauses_insatisfaites) == 0
    
    
    """
        Génère une assignation aleatoirement
    """
    def assignationAleatoire(self):
        # Pour chaque variable
        for i in range(self.nb_variables):
            # On choisit aleatoirement sa valeur de verite
            self.assignation[i] = random.randint(0, 1)
        self.trouveClausesInsatisfiable()    # !! on a modifié l'assignation
        
    
    """
        Inverse la valeur d'une variable de l'assignation
    """
    def changeValeurAssignation(self, var):
        self.assignation[var-1] = 1 - self.assignation[var-1]
        self.trouveClausesInsatisfiable()    # !! on a modifié l'assignation
    
    
    """
        Determine si un littéral est vrai ou faux dans l'assignation
            courante
    """
    def estLitteralVrai(self, litt):
        var = abs(litt)   # la variable (numero) sans négation (-)
        val = self.assignation[var-1]  # on regarde la valeur dans l'assignation
        # On traite les deux cas non a et v(a) = 0 ou a et v(a) = 1
        #   avec a la variable et v l'assignation
        return (litt < 0 and val == 0) or (litt > 0 and val == 1)
    
    
    """
        Reference dans l'attribut clauses_insatisfaites l'index de toutes
            les clauses qui ne sont pas satisfaites par l'assignation        
    """
    def trouveClausesInsatisfiable(self):
        # On efface l'ensemble non satisfait
        self.clauses_insatisfaites.clear()
        
        # Pour toutes les clauses
        for i in range(len(self.clauses)):
            nb_lit = len(self.clauses[i])
            
            # On cherche un litérral qui soit vrai
            j = 0
            while j < nb_lit and not self.estLitteralVrai(self.clauses[i][j]):
                j += 1
            
            # S'il n'y en a pas on met la clause insatisfaisable
            if j == nb_lit:
                self.clauses_insatisfaites.append(i)
    
    
    """
        Retourne aléatoirement l'index d'une clause dans l'attribut clause_
            insatisfaites
    """
    def choixClauseInsatisfaiteAleatoire(self):
        # Il s'agit d'un tirage au sort...
        alea = random.randint(0, len(self.clauses_insatisfaites)-1)
        return self.clauses_insatisfaites[alea]
    
    
    """
        Retourne un entier (correspondant à une variable) choisi au hasard
        Dans la clause dont l'index est donné en paramètre
    """
    def choixVariableAleatoire(self, index_clause): 
         # Il encore s'agit d'un tirage au sort...
        alea = random.randint(0, len(self.clauses[index_clause])-1)
        return abs(self.clauses[index_clause][alea])
    
    
    """
        Retourne la variable de score maximal dans la clause dont l'index
            est donné en paramètre
    """
    def choixVariableDeterministe(self, index_clause):
        # On calcule le score de chaque variable
        l_temp = list(map(
            lambda x : self.score_naif(abs(x)),
            self.clauses[index_clause]
        ))
        # On cherche le max
        smax = max(l_temp)
        # On retourne la variable dans la clause d'index celui du max.
        return abs(self.clauses[index_clause][l_temp.index(smax)])
    
    
    """
        Determine un score de satisfiabilité pour la variable donnée
    """
    def score_naif(self, var):
        score = 0
        
        if self.assignation[var-1] == 1:
            for clause in self.clauses:
                if clause.count(-var) != 0:
                    score += 1
                if clause.count(var) != 0:
                    score -= 1
        else:
            for clause in self.clauses:
                if clause.count(-var) != 0:
                    score -= 1
                elif clause.count(var) != 0:
                    score += 1
        return score
    
    
    """
        Ecrit la dans un fichier en utilisant le format dimacs
    """
    def ecrireSolution(self, nom_fichier):
        # Si on n'a pas de solution
        if not self.estModele():
            return
        
        # On appelle le module es_dimacs simplement
        litt = []
        for i in range(self.nb_variables):
            if self.assignation[i] == 0:
                litt.append(-i-1)
            else:
                litt.append(i+1)
        es_dimacs.ecrireSAT(nom_fichier, litt)
            