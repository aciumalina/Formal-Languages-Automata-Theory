#ECHIPA:
# Aciu Malina
# Boboc Cristina
# State Antonia
import copy
with open("tm_config_file4.txt") as fin:
    ok = 0
    ok1 = 0
    ok2 = 0
    ok3 = 0
    ok4 = 0
    states = []                 #in states memoram starile
    tape_alphabet = []          #memorarea alfabetului benzii
    sigma = []                  #alfabetul inputului
    states_aux = []             #pe masura ce citim din fisier ne vom introduce in states_aux si tape_alphabet_aux variabilele si terminalele intalnite, pentru a verifica la final daca coincid cu SIGMA si
                                #Tape Alphabet citite anterior
    tape_alphabet_aux = []

    delta = {}                  #in acest dictionar retinem functia de tranzitie

    for linie in fin:           #citim din fisier linie cu linie
        linie = linie.rstrip('\n')
        linie = "".join(linie.split())

        if linie == 'Sigma:':
            ok = 1
        if ok == 1 and linie != 'Sigma:' and linie != 'End':        #prin aceste linii de cod citim si retinem literele din SIGMA
            sigma.append(linie)
        if linie == 'End':
            ok = 0

        if linie == 'TapeAlph:':
            ok1 = 1
        if ok1 == 1 and linie != 'TapeAlph:' and linie != 'End':    #prin aceste linii de cod citim si retinem literele din ALFABETUL BENZII
            tape_alphabet.append(linie)
        if linie == 'End':
            ok1 = 0

        if linie == 'States:':
            ok2 = 1
        if ok2 == 1 and linie != 'States:' and linie != 'End':      #prin aceste linii de cod citim si retinem STARILE
            if ',' in linie:
                k = list(linie.split(','))                          #fie k linia curenta citita. Daca intalnim o virgula pe aceasta linie, o transformam intr-o lista
                                                                    #care ne va indica in functie de elementul de pe pozitia 1 daca starea citita este de start, accept sau reject
                if k[1] == 'S':
                    stare_start = k[0]                              #aici am gasit starea de start
                elif k[1] == 'accept':
                    stare_accept = k[0]                             #aici am gasit starea de accept
                else:
                    stare_reject = k[0]                             #altfel mai ramane starea de reject
                states.append(k[0])                                 #adaugam starea in lista de STATES
            else:
                states.append(linie)                                #altfel, daca nu gasim nicio virgula pe linia curenta, pur si simplu adaugam starea in lista de STATES
        if linie == 'End':
            ok2 = 0

        if linie == 'Delta:':
            ok3 = 1
        if ok3 == 1 and linie != 'Delta:' and linie != 'End':        #citirea functiei delta
            lista = linie.split('=')                                 #separam linia curenta in functie de semnul egal, transformam linia intr-o lista
            tuplu = []
            ls = []
            if lista[0].split(',')[0] not in states_aux:                #lista[0].split(',')[0] reprezinta starea cea mai din stanga, o adaugam in states_aux
                states_aux.append(lista[0].split(',')[0])
            if lista[0].split(',')[1] not in tape_alphabet_aux:         #lista[0].split(',')[1] reprezinta un caracter citit de pe banda, daca nu il gasim in tape_alphabet_aux il adaugam(
                                                                        #(facem verificare not in pentru a evita duplicatele)
                tape_alphabet_aux.append(lista[0].split(',')[1])
            if lista[1].split(',')[1] not in tape_alphabet_aux:          #lista[1].split(',')[1] reprezinta un caracter care va fi scris pe banda, daca nu il gasim in tape_alphabet_aux il adaugam
                tape_alphabet_aux.append(lista[1].split(',')[1])
            for item in lista[0].split(','):                            #separam lista[0] in functie de virgula pentru a crea un tuplu cu starea curenta la care ne aflam
                                                                        #si caracterul citit de pe banda, pentru reprezentarea functiei delta
                tuplu.append(item)
            tuplu = tuple(tuplu)                                        #aici transformam lista denumita "tuplu" intr-un tuplu, pentru a-l face imutabil

            for item in lista[1].split(','):                            #separam lista[1] in functie de virgula si adaugam fiecare item intr-o lista
                ls.append(item)
            delta[tuplu] = ls                                           #prin aceasta linie concretizam functia de tranzitie.
                                                                        #delta(q3; 0) = [q4; 0; R] => in aceast caz, ls este lista [q4; 0; R], iar tuplul "tuplu" mentionat anterior
                                                                        #este (q3; 0).
        if linie == 'End':
            ok3 = 0

        if linie == "Input:":                                   #citirea inputului benzii
            ok4 = 1
        if ok4 == 1 and linie != 'Input:' and linie != 'End':
            cuvant = linie.rstrip('\n')
        if linie == 'End':
            ok4 = 0

    # aici verificam ca starile intalnite pe parcurs in scrierea functiei delta sa fie aceleasi
    # cu starile date anterior, gasite in lista STATES. Facem aceeasi verificare si pentru caracterele din TAPE APLHABET.
    #verificam de asemenea ca starile de accept si reject sa fie diferite
    # verificam ca sigma sa nu contina SPACE
    if(states_aux.sort() == states.sort() and tape_alphabet_aux.sort() == tape_alphabet.sort() and stare_accept != stare_reject and 'SPACE' not in sigma):
        print("TM Valid")
    else:
        print("TM Invalid")

banda1 = ['$']                          #am adaugat suplimentar simbolul $ pentru a marca inceputul inputului

for i in cuvant:                        #pe prima banda, denumita banda1, vom scrie input-ul caracter cu caracter
    banda1.append(i)
banda1.append('SPACE')                  #la finalul input-ului adaugam SPACE pentru a delimita input-ul de restul benzii
banda2 = copy.deepcopy(banda1)          #cea de-a doua banda, denumita banda2, devine copia primei benzi
banda1.insert(1, stare_start)           #prin aceasta inserare aratam ca ne aflam in starea de start si capul benzii arata spre primul simbol

banda = []
banda.append(banda1)
banda.append('$')
banda.append(banda2)                    #am convertit cele doua benzi intr-o singura banda, delimitate prin simbolul '$'

stare1 = banda1[1]                      #in acest moment stare1 este starea initiala a benzii 1
lista_prev1 = banda1


def functie1(delta, banda1, lista_prev1):
    global stare1                                       #folosim stare1 ca variabila globala pentru a retine modificarile facute asupra acesteia indiferent de cate ori apelam functia
    stare_initiala = stare1                             #retinem stare1 in variabila stare_initiala pentru a retine starea curenta.
    tuplu = (stare_initiala, banda1[banda1.index(stare1)+1])                #variabila "tuplu" devine tuplul corespondent din dictionarul cu functia delta (adica starea curenta si urmatorul caracter de citit de pe banda)
    stare1 = delta[tuplu][0]                            #aici stare1 se modifica si ia valoarea starii urmatoare in care voi trece in urma aplicarii lui delta
    directie = delta[tuplu][2]                          #directia stanga sau dreapta
    lista_curenta = copy.deepcopy(banda1)               #imi fac o copie a benzii in variabila "lista_curenta" pentru a memora configuratia benzii inainte de modificari

    if(tuplu[1] != delta[tuplu][1] and directie == "R"):        #daca ne deplasam in dreapta si caracterul curent citit (adica tuplu[1]) este diferit de caracterul care ar trebui scris pe banda in urma tranzitiei
                                                                #delta[tuplu][1], inseamna ca vom scrie pe banda caracterul delta[tuplu][1]
            idx = banda1.index(stare_initiala)                  #retinem index-ul la care se gaseste starea la care ne aflam
            banda1[idx] = delta[tuplu][1]                       #modificam banda, iar starea curenta o inlocuim cu caracterul care trebuie scris conform delta

            banda1[idx+1] = stare1                              #urmatoare pozitie devine starea cea noua in care am ajuns, care fusese retinuta in stare1
            if(banda1.index(stare1) == len(banda1)-1):          #acest "if" trateaza conditia limita cand ne aflam la ultimul caracter din input, moment in care adaugam caracterul "SPACE" in continuare
                                                                #pentru a marca parcurgerea intregului input
                banda1.append("SPACE")
                lista_curenta = copy.deepcopy(banda1)           #reactualizam lista_curenta ca fiind o noua copie a benzii

    elif (tuplu[1] == delta[tuplu][1] and directie == "R"):     #daca caracterul curent citit este acelasi cu caracterul care ar trebui scris, inseamna ca
                                                                #pe banda nu vom scrie nimic, ci doar ne vom deplasa in dreapta cu starea cea noua
        idx = banda1.index(stare_initiala)
        banda1[idx] = banda1[idx+1]
        banda1[idx + 1] = stare1
        lista_curenta = copy.deepcopy(banda1)                   #reactualizam lista_curenta ca fiind o noua copie a benzii


    elif (tuplu[1] == delta[tuplu][1] and directie == "L"):      #acesta este iar un caz in care nu scriem nimic pe banda, dar ne deplasem in stanga.
                                                                 #urmam aceeasi gandire ca la cazul anterior, doar ca vom scrie la index idx-1 in loc de idx+1, pentru a exemplifica deplasarea in stanga
        idx = banda1.index(stare_initiala)
        banda1[idx] = lista_prev1[idx-1]
        banda1[idx - 1] = stare1
        lista_curenta = copy.deepcopy(banda1)


    elif tuplu[1] != delta[tuplu][1] and directie == "L":         #acesta este cazul in care scriem pe banda si ne deplasam in stanga. Am folosit aceeasi gandire ca la deplasarea in dreapta,
                                                                    #doar ca, din nou, am marcat deplasarea la stanga pe banda prin "idx-1".
        idx = banda1.index(stare_initiala)
        banda1[idx+1] = delta[tuplu][1]
        banda1[idx] = banda1[idx-1]
        banda1[idx-1] = stare1

    if (stare1 == stare_accept):            #cand ajungem cu starea1 in stare accept, inseamna ca inputul a fost acceptat pe prima banda
        print("input acceptat pe banda 1")

    elif (stare1 == stare_reject):          #cand ajungem cu starea1 in stare reject, inseamna ca inputul a fost respins de prima banda
        print("input respins pe banda 1")

    else:                                   #aici vom reapela functia atat timp cat inca nu suntem in stare_accept si nici in stare_reject
        lista_prev1 = lista_curenta          #in lista_prev vom retine lista_curenta
                                            #prin aceasta linie vom reflecta la nivelul intregii benzi ce modificari s-au facut la banda 1
        banda[0] = banda1
        for el in banda:
            if type(el) == list:
                for i in el:
                    print(i, end=" ")
            else:
                print(el, end=" ")
        print('\n')                      #prin aceste linii afisam stadiul curent al benzii
        functie1(delta, banda1, lista_prev1)          #reapelare functie

def functie2(delta, stare2, banda2, lista_prev2):
    stare_initiala = stare2
    tuplu = (stare_initiala, banda2[banda2.index(stare2)+1])
    stare2 = delta[tuplu][0]
    directie = delta[tuplu][2]
    lista_curenta = copy.deepcopy(banda2)

    if(tuplu[1] != delta[tuplu][1] and directie == "R"):
            idx = banda2.index(stare_initiala)
            banda2[banda2.index(stare_initiala)] = delta[tuplu][1]
            banda2[idx+1] = stare2
            if(banda2.index(stare2) == len(banda2)-1):
                banda2.append("SPACE")
                lista_curenta = copy.deepcopy(banda2)

    elif (tuplu[1] == delta[tuplu][1] and directie == "R"):
        idx = banda2.index(stare_initiala)
        banda2[idx] = banda2[idx+1]
        banda2[idx + 1] = stare2
        lista_curenta = copy.deepcopy(banda2)


    elif (tuplu[1] == delta[tuplu][1] and directie == "L"):
        idx = banda2.index(stare_initiala)
        banda2[banda2.index(stare_initiala)] = lista_prev2[banda2.index(stare_initiala)-1]
        banda2[idx - 1] = stare2
        lista_curenta = copy.deepcopy(banda2)


    elif tuplu[1] != delta[tuplu][1] and directie == "L":         #acesta este cazul in care scriem pe banda si ne deplasam in stanga. Am folosit aceeasi gandire ca la deplasarea in dreapta,
                                                                    #doar ca, din nou, am marcat deplasarea la stanga pe banda prin "idx-1".
        idx = banda2.index(stare_initiala)
        banda2[idx+1] = delta[tuplu][1]
        banda2[idx] = banda2[idx-1]
        banda2[idx-1] = stare2

    if (stare2 == stare_accept):
        print("input acceptat pe banda 2")

    elif (stare2 == stare_reject):
        print("input respins pe banda 2")

    else:
        lista_prev = lista_curenta
        banda[2] = banda2
        for el in banda:                        #printare configuratia actuala a benzii
            if type(el) == list:
                for i in el:
                    print(i, end = " ")
            else:
                print(el, end = " ")
        print('\n')
        functie2(delta, stare2, banda2, lista_prev)

functie1(delta, banda1, lista_prev1)
tuplu = (stare1, banda[1])              #aici cream tuplul format din stare1(care va fi qa sau qr) si banda[1], adica delimitatorul dintre cele doua benzi
banda2.insert(1, delta[tuplu][0])       #vom insera in banda doi starea in care ajungem prin aplicarea functiei de tranzitie
stare2 = banda2[1]                      #stare2 devine starea de start pentru banda 2
lista_prev2 = banda2
functie2(delta,stare2,banda2,lista_prev2)       #apelam functia pentru cea de-a doua banda

if(banda1 == banda2 and stare1 == stare_accept):                   #daca in urma apelarii celor doua functii, benzile arata identic si stare1 este de accept, inseamna ca inputul a fost acceptat
    print("Input acceptat")
elif(banda1 == banda2 and stare1 == stare_reject):                    #daca in urma apelarii celor doua functii, benzile arata identic si stare1 este de reject, inseamna ca inputul a fost respins
    print("Input respins")
else:                                                           #cazul in care cele doua benzi nu au avut acelasi rezultat
    print("Inconcludent")

print("Banda: ")
for el in banda:
    if type(el) == list:
        for i in el:
            print(i, end=" ")
    else:
        print(el, end=" ")
print('\n')