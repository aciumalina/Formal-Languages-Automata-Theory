with open('cfg_config_file.txt') as fin:
    ok = 0
    ok1 = 0
    ok2 = 0
    variables = []
    terminals = []
    variables_aux = []      #pe masura ce citim din fisier ne vom introduce in listele auxiliare variabilele si terminalele intalnite
    terminals_aux = []

    rules = {}          #dictionarul in care tinem variabilele si regulile care se aplica

    for linie in fin:
        linie = linie.rstrip('\n')
        linie = "".join(linie.split())

        if linie == 'Variables:':
            ok = 1
        if ok == 1 and linie != 'Variables:' and linie != 'End':
            variables.append(linie)
        if linie == 'End':
            ok = 0

        if linie == 'Terminals:':
            ok1 = 1
        if ok1 == 1 and linie != 'Terminals:' and linie != 'End':
            terminals.append(linie)
        if linie == 'End':
            ok1 = 0

        if linie == "Rules:":
            ok2 = 1
        if ok2 == 1 and linie != "Rules:" and linie != "End":
            linie2 = linie.split(',')
            variables_aux.append(linie2[0])
            punct_start = variables_aux[0]                  #prin conventie am luat prima variabila care se gaseste in setul de reguli ca fiind punctul de start
            if '|' in linie2[1]:
                reguli = linie2[1].split('|')                   #aici verificam daca avem "|" pentru a sti daca unei variabile i se aplica mai multe reguli
                for item in reguli:
                    if linie2[0] not in rules.keys():
                        rules[linie2[0]] = []
                    rules[linie2[0]].append(item)
                    for caracter in item:
                        if caracter not in variables:
                            terminals_aux.append(caracter)
            else:
                if linie2[0] not in rules.keys():
                    rules[linie2[0]] = []
                rules[linie2[0]].append(linie2[1])
                terminals_aux.append(linie2[1])
        if linie == 'End':
            ok2 = 0


    if(variables.sort() == variables_aux.sort() and terminals.sort() == terminals_aux.sort()):
        print("CFG Valid")
    else:
        print("CFG Invalid")




