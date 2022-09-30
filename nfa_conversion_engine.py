with open('dfa_nfa.in', 'r') as f:
    ok = 0
    ok1 = 0  # contorizam paragraful unde se gaseste Sigma
    ok2 = 0  # contorizam unde incepe si se termina Transitions
    # numarul starilor start
    punct_start = 0
    # numarul starilor finale
    punct_finish = 0
    # valid se ocupa cu verificarea starilor din segmentul States si starile din segmentul Transitions
    valid = 1
    letters = []  # alfabetul
    states = []  # starile
    z = []

    # dictionar care are ca si chei nod start si ca valori: litera si nod stop
    transitions = {}

    # states_transitions - se ocupa cu starile din tranzitie
    states_transitions = []
    # stari_plecare - are toate starile de unde se pleaca (Exemplu q0 se duce in q1 deci o sa am in stari_plecare=[q0])
    stari_plecare = []
    for linie in f:
        # linie contine \n
        linie = linie.rstrip('\n')
        linie = "".join(linie.split())

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
            t = linie.count(',')  # numara cate virgule avem pe linie
            if ',' in linie:
                k = list(linie.split(','))
                if t == 1:
                    if k[1] == 'S':
                        # y-punct de start
                        pct_st = k[0]
                        punct_start += 1
                    if k[1] == 'F':
                        # z-punct de final
                        z.append(k[0])
                        punct_finish += 1
                if t == 2:
                    pct_st = k[0]
                    z.append(k[0])
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
            stari_plecare.append(k[0])
            if k[1] not in letters:
                valid = 0
            states_transitions.append(k[0])
            states_transitions.append(k[2])
            if k[0] in transitions:
                transitions[k[0]].append((k[1], k[2]))
            else:
                transitions[k[0]] = []
                transitions[k[0]].append((k[1], k[2]))
        if linie == 'End':
            ok2 = 0

    # verificam daca avem aceleasi stari din segmentul States si in segmentul Transitions (daca nu, atunci nu e corect acest DFA)
    for x in states_transitions:
        if x not in states:
            valid = 0

    if punct_start != 1 or punct_finish == 0 or valid == 0:
        print('NFA nu e corect')
    else:
        print('NFA e corect')



def sortare(tuplu):
    for i in range(len(tuplu)):
        for j in range(i, len(tuplu)):
            if tuplu[i] > tuplu[j]:
                aux = tuplu[i]
                tuplu[i] = tuplu[j]
                tuplu[j] = aux
    return tuplu


stari_comasate = []
stari_comasate_individuale = set()
nou = {}

litere_intalnite = []
frecv = [0 for i in range(len(letters))]
letters = sorted(letters)

stari_noi_introduse = {pct_st}

for tuplu in transitions[pct_st]:
    frecv[letters.index(tuplu[0])] += 1

for tuplu in transitions[pct_st]:
    if (tuplu[0] not in litere_intalnite):
        litere_intalnite.append(tuplu[0])
        litere_intalnite.append(tuplu[1])
    else:
        stari_noi_introduse.add(sortare((litere_intalnite[litere_intalnite.index(tuplu[0]) + 1], tuplu[1])))
        nou[pct_st] = [(tuplu[0], (litere_intalnite[litere_intalnite.index(tuplu[0]) + 1], tuplu[1]))]
        stari_comasate_individuale.add(litere_intalnite[litere_intalnite.index(tuplu[0]) + 1])
        stari_comasate_individuale.add(tuplu[1])
print(stari_comasate_individuale)
for i in frecv:
    if i == 1:
        for tuplu in transitions[pct_st]:
            if tuplu[0] == letters[frecv.index(i)]:
                nou[pct_st].append(tuple(sorted(list(tuplu))))

frecv2 = [set() for i in range(len(letters))]

for tuplu in nou[pct_st]:
    if type(tuplu[1]) == tuple:
        nod_nou = tuplu[1]
        for stare in tuplu[1]:
            for tuplu1 in transitions[stare]:
                frecv2[letters.index(tuplu1[0])].add(tuplu1[1])

        nou[nod_nou] = []
        for multime in frecv2:
            nou[nod_nou].append((letters[frecv2.index(multime)], tuple(sorted(list(multime)))))
            stari_noi_introduse.add(tuple(sorted(list(multime))))

aux = {}
frecv3 = [set() for i in range(len(letters))]

for cheie in nou:
    for tuplu in nou[cheie]:
        if type(tuplu[1]) == tuple:
            if tuplu[1] in stari_noi_introduse and tuplu[1] not in nou.keys():
                nod_nou = tuplu[1]
                for stare in tuplu[1]:
                    for tuplu1 in transitions[stare]:
                        frecv3[letters.index(tuplu1[0])].add(tuplu1[1])
                aux[nod_nou] = []
                for multime in frecv3:
                    if len(multime) > 2:
                        continue
                    elif len(multime) != 1:
                        aux[nod_nou].append((letters[frecv3.index(multime)], tuple(sorted(list(multime)))))
                        stari_noi_introduse.add(tuple(sorted(list(multime))))
                    else:
                        aux[nod_nou].append((letters[frecv3.index(multime)], list(multime)[0]))
                        stari_noi_introduse.add(list(multime)[0])
        else:
            h = tuplu[1]
            frecv = [0 for i in range(len(letters))]
            litere_intalnite = []
            stari_comasate_individuale = set()
            for element in transitions[h]:
                frecv[letters.index(element[0])] += 1
                aux[h] = []
                if (element[0] not in litere_intalnite):
                    litere_intalnite.append(element[0])
                    litere_intalnite.append(element[1])
                else:
                    stari_noi_introduse.add(
                        sortare((litere_intalnite[litere_intalnite.index(element[0]) + 1], element[1])))
                    aux[h] = [(element[0], (litere_intalnite[litere_intalnite.index(element[0]) + 1], element[1]))]
                    stari_comasate_individuale.add(litere_intalnite[litere_intalnite.index(element[0]) + 1])
                    stari_comasate_individuale.add(element[1])
            for i in frecv:
                if i == 1:
                    for tuplu in transitions[h]:
                        if tuplu[0] == letters[frecv.index(i)]:
                            aux[h].append(tuple(sorted(list(tuplu))))

for nod in aux:
    ls = sorted(list(nod))
    if tuple(ls) not in nou.keys():
        nou[nod] = aux[nod]
print(nou)



#AFISARE IN FISIER
with open('outfile.in','w') as fout:
    print("Sigma: ", file=fout)
    for litera in letters:
        print(litera, file=fout)
    print("End", file=fout)

    print("States: ", file = fout)
    for cheie in nou:
        if cheie == pct_st:
            print(f"{cheie}, S", file = fout)
        elif type(cheie) == tuple:
            ok = 0
            for stare in cheie:
                if stare in z:
                    ok = 1

            if ok == 0:
                print(cheie, file=fout)
            else:
                print(f"{cheie}, F", file=fout)

        elif cheie in z:
            print(f"{cheie}, F", file = fout)

        elif cheie == pct_st and cheie in z:
            print(f"{cheie}, S, F",file = fout)

        else:
            print(cheie, file = fout)
    print("End", file = fout)

    print("Transitions: ", file = fout)
    for cheie in nou:
        for valoare in nou[cheie]:
            print(f"{cheie}, {valoare[0]}, {valoare[1]}", file=fout)
    print("End", file=fout)







