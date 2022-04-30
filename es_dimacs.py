#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 12:10:29 2022

@author: Elie
"""

import re

##############################################
#                                            #
#  Module d'entrées sortie au format dimacs  #
#                                            #
##############################################

"""
    Méthode qui lit un fichier dimacs contenant une CNF l'ensemble des clauses
    Renvoie un couple dont
          le premier élément est le nombre de variables distinctes
          le deuxième élément est une liste de clauses
"""
def lireCNFDimacs(nom_fichier):
    # Ouverture du fichier
    f = open(nom_fichier, 'r')
    
    # on saute les lignes de commentaires
    line = f.readline()
    while line[0] == 'c':
        line = f.readline()
    
    # On lit la déclaration du formalise
    expr = re.search("p cnf ([0-9]*) ([0-9]*)", line)
    nb_variables = int(expr.group(1))
    nb_clauses   = int(expr.group(2))
    
    # lectures des clauses
    clauses = []
    
    # Pour chaque ligne représentant une clause
    for _ in range(nb_clauses):
        line = f.readline()                       # On lit la ligne
        clause = re.findall("(-?[0-9]+) ", line)  # On recupère tous les entiers
        clause = list(map(lambda x: int(x), clause)) # STR -> INT
        clauses.append(clause)                    # On ajoute la clause
    
    # Fermeture du fichier
    f.close()
    
    # le retour
    return (nb_variables, clauses)


"""
    Méthode qui lit un fichier dimacs contenant une solution SAT
    Renvoie un couple dont
          le premier élément est le nombre de variables distinctes
          le deuxième élément est une liste de de littéraux
"""
def lireSAT(nom_fichier):
    # Ouverture du fichier
    f = open(nom_fichier, 'r')
    
    # on saute les lignes de commentaires
    line = f.readline()
    while line[0] != 'v':
        line = f.readline()
    
    # on recupère les littéraux et on convertit
    litteraux = re.findall("(-?[0-9]+) ", line)
    litteraux = list(map(lambda x: int(x), litteraux))
    
    # Fermeture du fichier
    f.close()
    
    # le retour
    return litteraux


"""
    Méthode qui écrit dans le fichier indiqué l'ensemble des clauses fournies
    au format DICMACS (CNF)
"""
def ecrireCNFDimacs(nb_var, clauses, nom_fichier):
    # Ouverture du fichier
    f = open(nom_fichier, 'w')
    
    # ENTETE COMMENTAIRES
    f.write("c \n")
    f.write("c TAKUZU PB\n")
    f.write("c E.C. L.D.M. A.K\n")
    f.write("c " + nom_fichier + "\n")
    f.write("c \n")
    
    # DECLARATION DU FORMALISME
    nb_clauses = len(clauses)  # nb de clauses
    f.write("p cnf " + str(nb_var) + " " + str(nb_clauses) + "\n")
    
    # ECRITURE DES CLAUSES MODELISANTS LES REGLES
    for clause in clauses:       # Pour chaque clause
        for lit in clause:
            f.write(str(lit) + " ")   # On écrit chaque littéral
        f.write("0\n")                # Et on ferme la clause
    
    # Fermeture du fichier
    f.close()


"""
    Méthode qui écrit les nb_litt premiers littéraux de l'ensemble fournis
    dans le fichier indiqué
"""
def ecrireSAT(nom_fichier, litteraux, nb_litt = -1):
    # Ouverture du fichier
    f = open(nom_fichier, 'w')
    
    # ENTETE COMMENTAIRES
    f.write("c \n")
    f.write("c TAKUZU SOL\n")
    f.write("c E.C. L.D.M. A.K\n")
    f.write("c " + nom_fichier + "\n")
    f.write("c \n")
    
    # declaration du fichier
    f.write("s SATISFIABLE\n")
    f.write("v ")
    
    # On affiche tous les littéraux
    if nb_litt == -1:
        nb_litt = len(litteraux)
    
    # On ecrit chaque littéral
    for i in range(nb_litt):
        f.write(str(litteraux[i]) + " ")
    
    # Et on ferme la solution
    f.write("0\n")
    
    # Fermeture du fichier
    f.close()