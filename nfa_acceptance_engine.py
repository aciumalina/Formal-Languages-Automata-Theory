with open('nfa_config_file.in', 'r') as f:
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

# print(transitions)
# {'q0': [('a', 'q1'), ('a', 'q0'), ('b', 'q0')], 'q1': [('b', 'q2')]}
# lista de liste ex: lista1=[[q0,q0],[q0,q1]] q0->(a)->q0 si q0->(a)->q1 acum verific daca ma pot duce cu starea q0 si starea q1 cu litera a in alta stare
# alt exemplu: lista1=[[q0,q0,q0,q0,q0],[q0,q0,q0,q0,q1]] ma uit la prima lista din lista1: [q0,q0,q0,q0,q0]
# q0->(a)->q0->(a)->q0->(b)->q0->(a)->q0
# iau ultima stare care e q0 si vad daca cu litera b se duce intr-o stare (am gasit starea q0)
# bag in lista_noua=[[q0,q0,q0,q0,q0,q0]]
# ma uit in a doua lista din lista1:  [q0,q0,q0,q0,q1]
#  # q0->(a)->q0->(a)->q0->(b)->q0->(b)->q1
# iau ultima stare care e q1 si vad daca cu litera b se duce intr-o stare (am gasit starea q2)
# bag in lista_noua=[[q0,q0,q0,q0,q0,q0], [q0,q0,q0,q0,q1,q2]]
s = input('s=')
lista1 = [[pct_st]]
lista_noua = list()
# for value in transitions[prima_stare]:
#     print(prima_stare,value[0],value[1],sep=',')

for i in range(len(s)):
    ok = 0
    lista_noua = list()
    for element in lista1:
        # exemplu q0->(a)->q0->(a)->q1->(b)-q2 lista1=[[q0,q0,q1,q2]]
        # verific daca ultima stare din lista din lista1 are vreo stare in care sa se duca (q2 nu are muchie cu nimeni)- deci nu mai are rost sa mai generez
        if element[-1] in stari_plecare:
            for value in transitions[element[-1]]:
                if value[0] == s[i]:
                    j = element.copy()
                    j.append(value[1])
                    # print(j)
                    lista_noua.append(j)
                    ok = 1
    # print(lista_noua)
    if ok == 0:
        break
    lista1.clear()
    lista1 = lista_noua.copy()
valid_cuvant = 0
if ok == 1:
    for element in lista1:
        if element[-1] in z:
            valid_cuvant = 1
            break
if valid_cuvant == 1:
    print("Cuvant acceptat")
else:
    print("Cuvantul nu a fost acceptat")