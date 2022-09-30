with open('dfa_config_file.in', 'r') as f:
    ok = 0
    ok1 = 0                 #contorizam paragraful unde se gaseste Sigma
    ok2 = 0                 #contorizam unde incepe si se termina Transitions
    # numarul starilor start
    punct_start = 0
    # numarul starilor finale
    punct_finish = 0
    # valid se ocupa cu verificarea starilor din segmentul States si starile din segmentul Transitions
    valid = 1
    letters = []        #alfabetul
    states = []         #starile
    z = []

    # dictionar care are ca si chei nod start si ca valori: litera si nod stop
    transitions = {}

    # states_transitions - se ocupa cu starile din tranzitie
    states_transitions = []
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
            t = linie.count(',')                #numara cate virgule avem pe linie
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
    print(transitions)


