# Projet d'INF402 - Takuzu

Projet d'INF402 - resolution d'une grille de Takuzu avec un SAT-solveur. Python.

## Rapport de projet


Le rapport sur lequel se base ce programme est disponible à l'adresse suivante :

[https://fr.overleaf.com/read/pkyjqgcshzjd](https://fr.overleaf.com/read/pkyjqgcshzjd)


## Execution du programme

### Avertissement

Le programme n'a pas été conçu pour gérer les erreurs de saisies.
Si l'utilisateur entre n'importe quoi le non bon fonctionnement du programme
est de sa responsabilité.

### Utilisation principale

Vous avez deux possibilités pour résoudre une grille de Takuzu :
1. Ecrire les données du problème dans un fichier (.tkz) respectant la structure suivante

```
largeur_de_la_grille(n)
n lignes comportant n symboles qui sont, soit '0' soit '1' soit '.'
le point représente l'absence de contraintes
```

Pour des exemples voir le dossier tests.

2. Au clavier (peu pratique) : on demande le nombre de zeros et de uns puis les coordoonées de tous les zeros puis ceux de tous les uns.

Pour éxécuter il faut ensuite entrer :
```
python3 main.py [fichier.tkz] [-s] [-i] [-h]
```

* L'option `-h` __(Help)__ permet d'avoir quelques éléments d'inforamtions.
* L'option `-s`_(avec Sortie)_ permet d'écrire les resultat de chaque operation dans des fichiers ;
* L'option `-i`_(Interne)_ permet d'utiliser le solveur 
	
  **Attention** : pour pouvoir utiliser le programme correctement, il faut que le programme `rsat` ce trouve dans le 'PATH'. Merci de l'installer.

* Enfin, il faut mettre les options après le nom du fichier (optionnel) et avec un `-` devant chaque.

## Organisation des fichiers

### Modules principaux

Il y  a dans ce projet 6 modules principaux :
1. La classe `Grille` qui définit une grille de jeu plus ou moins remplies
2. La librairie `es_dimacs` qui contient les fonctions d'entrée/sortie dans des fichiers dimacs.
3. Le module `pbmodele` permet à partir d'une grille de modéliser un problème sous forme de clauses qu'on peut écrire dans un fichier dimacs.
4. Le module `satsolveur` qui permet de trouver un modele d'un ensemble de 3-clauses.
5. Un programme principal qui permet de trouver la solution (si possible) d'un problème saisi par l'utilisateur (cf ci-dessus).

### Modules de test

Ce projet comporte 2 programmes qui testent séparement chaque fonction des modules `pbmodele`, `satsolveur`.
