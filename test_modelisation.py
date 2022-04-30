#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:10:29 2022

@author: elie
"""

import sys
from pbmodele import *
from grille import *
import es_dimacs


if __name__ == '__main__':
    g = Grille()
    g.construireGrilleFichier("tests/grille_4.tkz")
    
    print("Grille de jeu initiale :")
    g.ecrireGrille()
    
    pb = ProblemeModele(g)
    
    print("Nombre de clauses à obtenir : ", pb.nombreClauses())
    pb.nombreClauses()
    
    print("---------------------------------------------------------------")
    pb.determinerPremiereRegle()
    print("Cinquieme clause (ligne) première règle" + 
          " [u(2,1) + u(2,2) + u(2,3)] :\n", pb.clauses[8])
    print("Cinquieme clause (colonne) première règle" + 
          " [u(1,2) + u(2,2) + u(3,2)] : \n", pb.clauses[10])
    
    print("---------------------------------------------------------------")
    pb.clauses.clear()
    pb.determinerDeuxiemeRegle()
    print("Troisième clause (ligne) deuxieme règle" + 
          " [u(1,1) + u(1,2) + u(1,4)] :\n", pb.clauses[4])
    print("Troisième clause (colonne) deuxieme règle" + 
          " [u(1,1) + u(2,1) + u(4,1)] : \n", pb.clauses[6])
    

    print("---------------------------------------------------------------")
    r = pb.developper([
        [ [1, 5], [-1, -5] ],
        [ [2, 6], [-2, -6] ]    
    ])
    
    print("---------------------------------------------------------------")
    pb.clauses.clear()
    print("developpement de [(u11 + u21 ).(-u11 + -u21 )] + " +
          "[(u12 + u22 ).(-u12 + -u22 )] : \n", r)
    pb.determinerTroisiemeRegle()
    print("Première clause (ligne) troisième règle" + 
          " [u(1,1) + u(1,2) + u(1,4)] :\n", pb.clauses[0])
    print("Deuxième clause (ligne) troisième règle" + 
          " [u(1,1) + u(2,1) + u(4,1)] : \n", pb.clauses[1])
    print("Cinquième clause (ligne) troisième règle" + 
          " [u(1,1) + u(2,1) + u(4,1)] : \n", pb.clauses[4])
    
    print("---------------------------------------------------------------")
    pb.determinerClauses()
    
    print("Nombre de clauses réel : ", len(pb.clauses))
    
    print("---------------------------------------------------------------")
    pb.sortieDimacs("toto.dmcs")
    u = es_dimacs.lireCNFDimacs("toto.dmcs")
    print(u[0])
    print(u[1][8])
    print(u[1][10])   # 32 clauses pour la première
    print(u[1][36])
    print(u[1][38])   # 64 pour la seconde
    print(u[1][96])
    print(u[1][97])
    print(u[1][100])  # 192 pour la derniere
    print(u[1][288])  # et les 5 contraintes initiales



