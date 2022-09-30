TM input file are urmatorul format:

# comentariu
# comentariu  (skip)
# comentariu

States:
q1, S
q2
q3
...
qa, accept
qr, reject
End

# comentariu
# comentariu  (skip)
# comentariu

Sigma:
0
End

# comentariu
# comentariu  (skip)
# comentariu

TapeAlph:
0
x
SPACE
...
End

# comentariu
# comentariu  (skip)
# comentariu

Delta:
q1, 0 = q2, SPACE, R
q2, SPACE = qr, SPACE, L
...
End

# comentariu
# comentariu  (skip)
# comentariu

In states, starea care contine "S" este punctul de start, iar qa si qr reprezinta starile de accept, respectiv reject. Am notat cu SPACE spatiul liber.
De asemenea, R si L reprezinta directia de deplasare spre dreapta, respectiv stanga.
States determina starile, Sigma este alfabetul inputului, TapeAlph determina alfabetul benzii, Delta este functia de tranzitie.
De exemplu, scrierea q1, 0 = q2, SPACE, R arata ca din starea q1, la citirea caracterului 0 ne mutam in starea q2, pe banda scriem SPACE si ne deplasam in dreapta.





