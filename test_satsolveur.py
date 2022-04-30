#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 11:50:11 2022

@author: elie
"""

from satsolveur import *

solv = SatSolveur([
        [1, 4],
        [1, -4],
        [-1, 4],
        [3, 2, 5],
        [-3, -5],
        [-3, 5],
        [3, -5]
    ], 5)

print("-------- CLAUSES -----------------------")
print(solv.clauses)

print("-------- ASSIGNATION ALEATOIRE ---------")
solv.assignationAleatoire()
print(solv.assignation)
solv.assignationAleatoire()
print(solv.assignation)
solv.assignationAleatoire()
print(solv.assignation)
solv.assignation = [0, 0, 1, 1, 0]

print("-------- TEST SATISFIABILITE -----------")
solv.trouveClausesInsatisfiable()
print(solv.clauses_insatisfaites)
print(solv.estModele())

print("-------- CLAUSE ALEATOIRE --------------")
i = solv.choixClauseInsatisfaiteAleatoire()
print(i)

print("-------- VARIABLE ALEATOIRE ------------")
i = solv.choixVariableAleatoire(3)
print(i)

print("-------- VARIABLE DETERMINISTE ---------")
print(solv.assignation)
for i in range(solv.nb_variables):
    print("Max score " + str(i+1) + " : " + str(solv.score_naif(i+1)))
i = solv.choixVariableDeterministe(4)
print(i)

solv.assignation[3] = 0
print(solv.assignation)
for i in range(solv.nb_variables):
    print("Max score " + str(i+1) + " : " + str(solv.score_naif(i+1)))
i = solv.choixVariableDeterministe(4)
print(i)

print("-------- TEST SOLVEUR ------------------")
res = solv.lancerSolveur(P, MAX_ITERATION)
print(res)
print(solv.assignation)