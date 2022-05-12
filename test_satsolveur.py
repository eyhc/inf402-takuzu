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
        [2, 3, 4],
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

print("-------- TEST SATISFIABILITE -----------")
solv.assignation = [0, 0, 1, 1, 0]
print(solv.assignation)
solv.trouveClausesInsatisfiable()
print(solv.clauses_insatisfaites)
print(solv.estModele())

print("-------- CLAUSE ALEATOIRE --------------")
i = solv.choixClauseInsatisfaiteAleatoire()
print(i)

print("-------- VARIABLE ALEATOIRE cl 3 -------")
i = solv.choixVariableAleatoire(3)
print(i)

print("-------- VARIABLE DETERMINISTE clause 3 ")
print(solv.assignation)
for i in range(1,4):
    print("Max score " + str(i+1) + " : " + str(solv.score_naif(i+1)))
i = solv.choixVariableDeterministe(3)
print(i)

solv.assignation[3] = 0
solv.assignation[4] = 1
print(solv.assignation)
for i in range(1,4):
    print("Max score " + str(i+1) + " : " + str(solv.score_naif(i+1)))
i = solv.choixVariableDeterministe(3)
print(i)

print("-------- TEST SOLVEUR ------------------")
res = solv.lancerSolveur(P, MAX_ITERATION)
print(res)
print(solv.assignation)