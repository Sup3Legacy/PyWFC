# PyWFC
Utilisation de l'algorithme WFC dans des problèmes de résolution ou de génération

## Motivation
J'ai appris récemment l'existence de l'[algorithme WFC (Wave function collapse)](https://github.com/mxgmn/WaveFunctionCollapse) et dans ce projet, je souhaite exploiter les différentes possibilités qu'il offre.

Pour commencer, je l'ai utilisé dans le cadre de la recherche d'une solution bien définie, ie. la résolution d'un Sudoku.

## PySudoku
Le principe de l'algorithme, appliqué au Sudoku est let suivant : On se done une grille de départ. Toutes les cases qui ne sont pas remplies seront potentiellement remplies par plusieurs ```états``` (les états sont les nombres 1-9). Ces cases sont alors en **superposition d'états** (terme emprunté à la physique quantique). On appelle **entropie** d'une case le nomrbe d'états possibles à un certains moment sur cette case (lrosque qu'on **réduit** une case, ie. on lui assigne un nombre, on fixe son entropie à 0, par convention). Le but de l'algorithme est de **réduire entièrement la fonction d'onde**, c'est à dire d'assigner à chaque case un unique état, donc d'amener l'entropie totale à son minimum.

### Fonctionnement de l'algorithme

On se donne une grille de départ. On en déduit tous les états possibles sur chaque case non encore attribuée.
* Tant qu'il existe une case d'entropie non nulle, faire :
  * Prendre une case, **C**, d'entropie non nulle minimale (possible, l'entropie étant un entier naturel)
  * La réduire, c'est-à-dire prendre parmis ses états possibles un état au hasard et le lui attribuer, faisant tomber son entropie à 0.
  * En déduire des réduction partielles d'autres cases. En effet, ayant réduit **C**, toutes les cases de la même colonne/ligne/carré ne peuvent avoir le même état. Donc chacune de ces cases qui avait comme état possible l'état attribué à **C** voit son entropie diminuer de 1.

La terminaison de cet algorithme est immédiate, étant donné qu'à chaque itération, on fait baisser l'entropie totale d'au moins 1 (l'**entropie étant ici une valeur naturelle**).
Pourtant, sa correction n'est pas assurée. En effet, le choix aléatoire de l'état à attribuer à la case au moment de sa réduction peut mener dans une impase : une ou plusieurs cases peuvent se vori retirer tous leurs états possibles. Alors, la résolution ne peut plus continuer.

Pour résoudre ce problème, il existe une solution : le **back-tracking**. Il s'agit de garder une trace de toutes les actions faites et de, lorsqu'un blocage est détecté, remonter l'arbre des décisions (donc faire artificiellement augmenter l'entropie) jusqu'à la décision blocante, la changer et réessayer. Il s'agit alors ni plus ni moins d'**explorer l'arbre entier des possibilités de la grille**, jusqu'à trouver une solution satisfaisante. On passe alors d'un algorithme non-déterministe à un algorithme déterministe.

Pourtant, j'ai pris le parti de rester sur mon implémentation initiale et ne ne pas utiliser de **back-tracking**, étant donné qu'il est possible de faire la chose suivant : lorsqu'un blocage est détecté, réinitialiser la grille et recommencer du début. Cette solution, peu élégante, a l'avantage d'être tout de même rapide (moins d'**1s** pour une grille "facile" et **10-20s** pour une grilel "expert").
De plus, le code (uploadé ici) est très court, à peine 120 lignes, ce qui en fait un solveur de Sudoku très rapide et simple à implémenter!
