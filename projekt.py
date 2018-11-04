import re
import csv
import os

nahajalisce_strani = r'C:\Users\Lucija\Downloads'
shranjena_stran = 'Imenik_lokalov_Studentska_prehrana.htm'
vzorec_bloka = re.compile(
    r'<div class="row restaurant(.*?)<div class="pull-right margin-right-10">', 
    re.DOTALL)
vzorec_podatkov = re.compile(r'row(?P<lastnosti_ponudbe>.+?)".*?data-lat=.*?'
                    r'data-naslov="(?P<naslov>.+?)".*?'
                    r'data-cena="(?P<cena>.+?)".*?'
                    r'data-doplacilo="(?P<doplacilo>.+?)".*?'
                    r'data-posid="(?P<id>.+?)".*?'
                    r'data-lokal="(?P<ime>.+?)" .*?'
                    r'data-city="(?P<mesto>.+?)".*?'
                    r'acidjs-rating-disabled">(?P<ocena>.*?)<br />.*?',
                             re.DOTALL)
vzorec_ocene = re.compile(r'checked="checked".*?value="(?P<ocena>.+?)".*?',
                          re.DOTALL)
slovar_lastnosti_ponudbe = {'1': 'Vegetarijansko',
                            '3': 'Dostop za invalide',
                            '5': 'Dostava', '7': 'Solata',
                            '8': 'Dostop za invalide (WC)',
                            '9': 'Študentske ugodnosti',
                            '10': 'Celiakiji prijazni obroki',
                            '20': 'Odprt ob vikendih',
                            '21': 'Kosilo',
                            '22': 'Pizza',
                            '23': 'Hitra hrana',
                            '69': 'Nov lokal'}

def vsebina_datoteke(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()

def page_to_blocks(page):
    '''Split "page" to a list of blocks.'''
    lokali = re.findall(vzorec_bloka, page)
    return lokali

def get_information_from_block(block):
    '''Build a dictionary containing information.'''
    data = re.search(vzorec_podatkov, block)
    slovar_informacij = data.groupdict()
    return slovar_informacij

def lokali_iz_datoteke(directory, filename):
    '''Parse the ads in filename/directory into a dictionary list.'''
    page = vsebina_datoteke(directory, filename)
    lokali = []
    for block in page_to_blocks(page):
        lokali.append(get_information_from_block(block))
    return lokali

def izlusci_oceno(lokali):
    for lokal in lokali:
        if 'checked="checked"' in lokal['ocena']:
            for ujemanje in re.finditer(vzorec_ocene, lokal['ocena']):
                nova_ocena = ujemanje.group('ocena')
            lokal['ocena'] = int(nova_ocena)
        else:
            lokal['ocena'] = 0
    return lokali

def izlusci_lastnosti_ponudbe(lokali):
    for lokal in lokali:
        vzorec_lastnosti = re.compile(r'(\d+)', re.DOTALL)
        lastnosti_lokala = set()
        for ujemanje in re.finditer(vzorec_lastnosti,
                                    lokal['lastnosti_ponudbe']):
            lastnosti_lokala.add(slovar_lastnosti_ponudbe[ujemanje.group(0)])
        lokal['lastnosti_ponudbe'] = lastnosti_lokala
    return lokali

def pripravi_lastnosti_ponudbe_za_zapis(lokali):
    ponudba = []
    for lokal in lokali:
        for lastnost in lokal['lastnosti_ponudbe']:
            ponudba.append({'id': int(lokal['id']),
                            'lastnost': lastnost})
    return ponudba

def pripravi_podatke_za_zapis(lokali):
    podatki = []
    for lokal in lokali:
        slovar = {}
        slovar['id'] = int(lokal['id'])
        slovar['cena'] = round(float(lokal['cena'][:-3])
                               + float(lokal['cena'][-2:]) * 0.01, 2)
        slovar['doplacilo'] = round(float(lokal['doplacilo'][:-3])
                                    + float(lokal['doplacilo'][-2:]) * 0.01, 2)
        slovar['naslov'] = lokal['naslov']
        slovar['ocena'] = lokal['ocena']
        slovar['mesto'] = lokal['mesto']
        slovar['ime'] = lokal['ime']
        podatki.append(slovar)
    return podatki

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

lokali = lokali_iz_datoteke(nahajalisce_strani, shranjena_stran)
precisceni_lokali = izlusci_oceno(izlusci_lastnosti_ponudbe(lokali))
ponudba = pripravi_lastnosti_ponudbe_za_zapis(precisceni_lokali)
podatki = pripravi_podatke_za_zapis(precisceni_lokali)
zapisi_csv(podatki, ['id', 'cena', 'doplacilo', 'mesto', 'ocena','ime',
                     'naslov'], 'studentska_prehrana.csv')
zapisi_csv(ponudba, ['id', 'lastnost'], 'lastnosti_ponudbe.csv')
