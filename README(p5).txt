CFG input file are urmatorul format:

# comentariu
# comentariu  (skip)
# comentariu

Variables:
var1
var2
 ...
End

# comentariu
# comentariu  (skip)
# comentariu

Terminals:
t1
t2
#
...
End

# comentariu
# comentariu  (skip)
# comentariu

Rules:
var1, t1var1t2|var2
var2, #
...
End

# comentariu
# comentariu  (skip)
# comentariu

Prin conventie, prima variabila gasita in setul de reguli (in partea stanga) este punctul de start, iar la variabilele cu mai multe reguli, regulile sunt despartite prin "|".
Eps este Epsilon


