with open('dfa_config_file.in', 'r') as f:
    ok = 0
    ok1 = 0
    ok2 = 0
    # numarul starilor start
    punct_start = 0
    # numarul starilor finale
    punct_finish = 0
    # valid se ocupa cu verificarea starilor din segmentul States si starile din segmentul Transitions
    valid = 1
    letters = []        #alfabetul
    states = []         #starile
    multimea_stari_finale = []
    # dictionar care are ca si chei nod start si ca valori: litera si nod stop
    transitions = {}
    # states_transitions - se ocupa cu starile din tranzitie
    states_transitions = []
    for linie in f:
        # linie contine \n
        linie = linie.rstrip('\n')
        linie = "".join(linie.split())
        # print(linie)
        # litere start
        # luam toate literele din segmentul Sigma pana la End
        if linie == 'Sigma:':
            ok = 1
        if ok == 1 and linie != 'Sigma:' and linie != 'End':
            letters.append(linie)
        if linie == 'End':
            ok = 0
        # litere finish
        # luam toate starile din segmentul States pana la End
        # de asemenea daca avem un S sau un F dupa stare inseamna ca avem o stare start sau stare finala si numaram starile de start si cele de final
        if linie == 'States:':
            ok1 = 1
        if ok1 == 1 and linie != 'States:' and linie != 'End':
            t = linie.count(',')
            h = linie.split(',', 1)
            if ',' in linie:
                k = list(linie.split(','))
                if t == 1:
                    if k[1] == 'S':
                        # y-punct de start
                        pct_st = k[0]
                        punct_start += 1
                    if k[1] == 'F':
                        # z-punct de final
                        multimea_stari_finale.append(k[0])
                        punct_finish += 1
                if t == 2:
                    pct_st = k[0]
                    multimea_stari_finale.append(k[0])
                    punct_start += 1
                    punct_finish += 1
                states.append(k[0])
            else:
                states.append(linie)
        if linie == 'End':
            ok1 = 0
        # luam toate literele din segmentul Transitions pana la End
        # ex: stare1:[(litera2,stare2),(litera3,stare3)] practic am avea muchia stare1->stare2 (ducem din starea1 litera2 in starea2) si muchia stare1->stare3(ducem din starea1 litera3 in starea3)
        if linie == 'Transitions:':
            ok2 = 1
        if ok2 == 1 and linie != 'Transitions:' and linie != 'End':
            k = list(linie.split(',', 2))
            k[0] = k[0].rstrip(' ')
            if k[1] not in letters:
                valid = 0
            states_transitions.append(k[0])
            states_transitions.append(k[2])
            if k[0] in transitions:
                transitions[k[0]].append([k[1], k[2]])
            else:
                transitions[k[0]] = []
                transitions[k[0]].append([k[1], k[2]])
        if linie == 'End':
            ok2 = 0
    # verificam daca avem aceleasi stari din segmentul States si in segmentul Transitions (daca nu, atunci nu e corect acest DFA)
    for x in states_transitions:
        if x not in states:
            valid = 0

    # verificam daca exista doua muchii care pleaca dintr-o stare cu aceeasi litera in stari diferite (daca da, atunci nu mai e un automat determinist)
    for st in transitions:
        for i in transitions[st]:
            for j in transitions[st]:
                if (i[0] == j[0] and i[1] != j[1]) or (j[0] not in letters):
                    valid = 0
                    break

    if punct_start != 1 or punct_finish == 0 or valid == 0:
        print('DFA nu e corect')
    else:
        print('DFA e corect')

matrice = [[None for i in range(len(states))] for j in range(len(states))]              #am alocat matricea
for i in range(1,len(states)):
    for j in range(0,i):
        if(states[i] in multimea_stari_finale and states[j] in multimea_stari_finale) or (states[i] not in multimea_stari_finale and states[j] not in multimea_stari_finale):
            matrice[i][j] = 0
            matrice[j][i] = 0
        else:
            matrice[i][j] = 1
            matrice[j][i] = 1

for i in range(len(states)):                #luam elementele de sub diagonala principala, cele care ne intereseaza (PRIMA ITERATIE)
    for j in range(i):
        if matrice[i][j] == 0:
            k = 0
            n = len(transitions[states[i]])
            while k < n:
                if matrice[states.index(transitions[states[i]][k][1])][states.index(transitions[states[j]][k][1])] == 1:
                    matrice[i][j] = 1
                    matrice[j][i] = 1
                k+=1

for i in range(len(states)):                #luam elementele de sub diagonala principala, cele care ne intereseaza(A DOUA ITERATIE)
    for j in range(i):
        k = 0
        if matrice[i][j] == 0:
            k = 0
            for k in range(len(states[i])):
             if matrice[states.index(transitions[states[i]][k][1])][states.index(transitions[states[j]][k][1])] == 1:
                    matrice[i][j] = 1
                    matrice[j][i] = 1
for linie in matrice:
     print(linie)


stari_finale = list()
for i in range(len(states)):
    for j in range(i):
        if matrice[i][j] == 0:
            if (states[i] in multimea_stari_finale or states[j] in multimea_stari_finale):                          #verificam starile finale din tuplu. daca o stare finala este comasata cu alta stare, o vom sterge din lista, dupa care adaugam tuplul(starea nou formata)
                try:
                    multimea_stari_finale.remove(states[i])
                except:
                    pass
                try:
                    multimea_stari_finale.remove(states[j])
                except:
                    pass
                multimea_stari_finale.append((states[i], states[j]))
            if (states[i] == pct_st or states[j] == pct_st):
                pct_st = (states[i], states[j])
            stari_finale.append(((states[i], states[j])))

multime_stari = set()

for tuplu in stari_finale:                         #in multime_stari punem toate starile care au fost comasate cu altele
    multime_stari.add(tuplu[0])
    multime_stari.add(tuplu[1])

stari_necomasate = []

for st in states:
    if st not in multime_stari:
        stari_necomasate.append(st)

for stare in stari_necomasate:
    stari_finale.append(stare)


dictionar_final = {}                    #am parcurs dictionarul cu starile initiale si am modificat functia delta, in functie de starile care au fost comasate si nu mai exista de sine statatoare
for cheie in transitions:
    i = 0
    for ls in transitions[cheie]:
        if ls[1] in multime_stari:
            for stare in stari_finale:
                if type(stare) == tuple:
                    if ls[1] in stare:
                        transitions[cheie][i][1] = stare
        i += 1
print(transitions)

for cheie in transitions:
    if cheie in multime_stari:
        for stare in stari_finale:
            if type(stare) == tuple:
                if cheie in stare:
                    dictionar_final[stare] = transitions[cheie]
    else:
        dictionar_final[cheie] = transitions[cheie]
print(dictionar_final)                                          #contine functia delta actualizata

#PRINTARE IN FISIER
with open('output.in', 'w') as fout:
    print("Sigma: ", file = fout)
    for litera in letters:
        print(litera, file = fout)
    print("End", file = fout)

    print("States: ", file = fout)

    for cheie in dictionar_final:
        if cheie == pct_st:
            print(f"{cheie}, S", file = fout)
        elif cheie in multimea_stari_finale:
            print(f"{cheie}, F", file = fout)
        elif cheie == pct_st and cheie in multimea_stari_finale:
            print(f"{cheie}, S, F", file = fout)
        else:
            print(cheie, file = fout)

    print("End", file = fout)

    print("Transitions:", file = fout)
    for cheie in dictionar_final:
        for valoare in dictionar_final[cheie]:
            print(f"{cheie}, {valoare[0]}, {valoare[1]}", file = fout)
    print("End", file = fout)

































