import copy
with open("tm_config_file.txt") as fin:
    ok = 0
    ok1 = 0
    ok2 = 0
    ok3 = 0
    states = []
    tape_alphabet = []
    sigma = []
    states_aux = []  # pe masura ce citim din fisier ne vom introduce in listele auxiliare variabilele si terminalele intalnite
    tape_alphabet_aux = []

    delta = {}

    for linie in fin:
        linie = linie.rstrip('\n')
        linie = "".join(linie.split())

        if linie == 'Sigma:':
            ok = 1
        if ok == 1 and linie != 'Sigma:' and linie != 'End':
            sigma.append(linie)
        if linie == 'End':
            ok = 0

        if linie == 'TapeAlph:':
            ok1 = 1
        if ok1 == 1 and linie != 'TapeAlph:' and linie != 'End':
            tape_alphabet.append(linie)
        if linie == 'End':
            ok1 = 0

        if linie == 'States:':
            ok2 = 1
        if ok2 == 1 and linie != 'States:' and linie != 'End':
            if ',' in linie:
                k = list(linie.split(','))
                if k[1] == 'S':
                    stare_start = k[0]
                elif k[1] == 'accept':
                    stare_accept = k[0]
                else:
                    stare_reject = k[0]
                states.append(k[0])
            else:
                states.append(linie)
        if linie == 'End':
            ok2 = 0

        if linie == 'Delta:':
            ok3 = 1
        if ok3 == 1 and linie != 'Delta:' and linie != 'End':
            lista = linie.split('=')
            tuplu = []
            ls = []
            if lista[0].split(',')[0] not in states_aux:
                states_aux.append(lista[0].split(',')[0])
            if lista[0].split(',')[1] not in tape_alphabet_aux:
                tape_alphabet_aux.append(lista[0].split(',')[1])
            if lista[1].split(',')[1] not in tape_alphabet_aux:
                tape_alphabet_aux.append(lista[1].split(',')[1])
            for item in lista[0].split(','):
                tuplu.append(item)
            tuplu = tuple(tuplu)

            for item in lista[1].split(','):
                ls.append(item)
            delta[tuplu] = ls

        if linie == 'End':
            ok3 = 0

    if(states_aux.sort() == states.sort() and tape_alphabet_aux.sort() == tape_alphabet.sort()):
        print("TM Valid")
    else:
        print("TM Invalid")


s = "0000"
lista = [stare_start]
for i in s:
    lista.append(i)

stare = lista[0]
lista_prev = lista

def functie(delta, stare, lista, lista_prev):
    stare_initiala = stare
    tuplu = (stare_initiala, lista[lista.index(stare)+1])
    stare = delta[tuplu][0]
    #stanga sau dreapta
    directie = delta[tuplu][2]
    lista_curenta = copy.deepcopy(lista)

    if(tuplu[1] != delta[tuplu][1] and directie == "R"):
            idx = lista.index(stare_initiala)
            lista[lista.index(stare_initiala)] = delta[tuplu][1]
            lista[idx+1] = stare
            if(lista.index(stare) == len(lista)-1):
                lista.append("SPACE")
                lista_curenta = copy.deepcopy(lista)

    elif (tuplu[1] == delta[tuplu][1] and directie == "R"):
        idx = lista.index(stare_initiala)
        lista[idx] = lista[idx+1]
        lista[idx + 1] = stare
        lista_curenta = copy.deepcopy(lista)


    elif (tuplu[1] == delta[tuplu][1] and directie == "L"):
        idx = lista.index(stare_initiala)
        lista[lista.index(stare_initiala)] = lista_prev[lista.index(stare_initiala)-1]
        lista[idx - 1] = stare
        lista_curenta = copy.deepcopy(lista)

    if (stare == stare_accept):
        print(" ".join(str(el) for el in lista))
        print("input acceptat")

    elif (stare == stare_reject):
        print(" ".join(str(el) for el in lista))
        print("input respins")

    else:
        lista_prev = lista_curenta
        print(" ".join(str(el) for el in lista))
        functie(delta, stare, lista, lista_prev)

functie(delta,stare, lista, lista_prev)


