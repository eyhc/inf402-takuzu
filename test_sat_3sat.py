#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 21:24:04 2022

@author: elie
"""

from sat_3sat import *

sat3 = Sat3SAT([
        [1],
        [-3, 2],
        [-4,6,-5],
        [1,2,3,4,5,6,7,8,9,10,11,-12,-14,13,15,-1,-2,-3,-4,-5,-6],
        [12,-5],
        [-4,5,4]
    ], 15)


sat3.conversion()

print("-------- CLAUSES INITIALES ----------------------")
print(sat3.clauses)

print("\n-------- CLAUSES CONVERTIES ---------------------")
print(sat3.clauses_simplifiees)

print("\n-------- NOMBRE DE VARIABLES --------------------")
print(sat3.nb_variables)