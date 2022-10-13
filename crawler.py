from bs4 import BeautifulSoup
import re
import urllib

categorii_noi = ["Telefoane","Electrocasnice","Tablete-eReadere","Retelistica & Servere",
            "Gadgets, Wearables & Camere foto-video","Componente Laptop-PC","Accesorii telefoane & tablete"
            ,"Laptop-Calculator-Gaming","TV","Piese telefoane & tablete"]
expresii_noi = ["samsung|iphone|huawei|blackberry|nokia",
     "aragaz|fier de calcat|frigider|uscator|aspirator"
     ,"tableta samsung|apple|asus|huawei|kindle|xiaomi|64gb|128gb|256gb"
     ,"router|stick|memorie|cablu|usb|telecomanda"
     ,"smartwatch|camera foto|ceas|boxa"
     ,"baterie|display|hard disk|procesor|tastatura|mouse"
     ,"cablu|incarcator|husa|folie|baterie externa"
     ,"asus|dell|lenovo|hp|toshiba|ps5|xbox"
     ,"tv samsung|lg|philips|horizon"
     ,"baterie|acumulator|carcasa|husa|baterie|cablu"]

def adunare(ls1,ls2):
    for i in range(len(ls1)):
        ls1[i] += ls2[i]
    return ls1

ls = []
for i in range(len(categorii_noi)):
    lista = [0 for x in range(len(expresii_noi[i].split('|'))+1)]
    ls.append(lista)

with open("output.html", "w") as fout:
    fout.write('<html>\n<head> <meta charset="UTF-8"> \n<title> \nCategoriile intalnite \
               </title>\n</head> <body> <h1> Anunturile de pe <u>OLX.ro</u></h1>')
    lista_url = ["https://www.olx.ro/d/electronice-si-electrocasnice/?currency=RON&page=" + str(i) for i in range(1,26)]

    for url in lista_url:
        res = urllib.request.urlopen(url)
        soup = BeautifulSoup(res, 'lxml')
        titluri = soup.findAll("h6")
        for i in range(0, len(categorii_noi)):
            lista = expresii_noi[i].split('|')
            v = [0 for i in range(len(lista)+1)]               #vector de frecventa pt subcategorii ( ex: iphone, samsung, huawei, etc)
            for titlu in titluri:
                for item in lista:
                    titlu = str(titlu).lower()
                    if (re.search(item, titlu) is not None):
                        titlu = titlu.replace('<h6 class="css-v3vynn-text eu5v0x0">', '')
                        titlu = titlu.replace('</h6>', '')
                        v[lista.index(item)] += 1
                    elif lista.index(item) == len(lista)-1:
                        v[-1] += 1
            ls[i] = adunare(ls[i], v)

    fout.write('<section>')
    for i in range(len(categorii_noi)):
        lista = expresii_noi[i].split('|')
        print(f"<h2>{categorii_noi[i]}: </h2> ", file=fout)
        for cuvant in lista:
            fout.write('<p>')
            print(f"{cuvant}: {ls[i][lista.index(cuvant)]}", file = fout)
            fout.write('</p>')
        print(f"Altceva: {ls[i][-1]}", file = fout)
    fout.write('</section>')
    fout.write('\n')

    fout.write("</body></html>")
