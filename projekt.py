import re
import csv
import os

def vsebina_datoteke(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        return file_in.read()

def page_to_blocks(page):
    '''Split "page" to a list of blocks.'''
    rx = re.compile(r'<div class="row restaurant(.*?)<div class="pull-right margin-right-10">', re.DOTALL)
    lokali = re.findall(rx, page)
    return lokali


def get_information_from_block(block):
    '''Build a dictionary containing information.'''
    rx = re.compile(r'row(?P<lastnosti_ponudbe>.+?)".*?data-lat=.*?'
                    r'data-naslov="(?P<naslov>.+?)".*?'
                    r'data-cena="(?P<cena>.+?)".*?'
                    r'data-doplacilo="(?P<doplacilo>.+?)".*?'
                    r'data-lokal="(?P<ime>.+?)" .*?'
                    r'data-city="(?P<mesto>.+?)".*?'
                    r'checked="checked".*?value="(?P<ocena>.+?)".*?', re.DOTALL)
    data = re.search(rx, block)
    slovar_informacij = data.groupdict()
    return slovar_informacij

#do tukaj je po mojem OK






def lokali_iz_datoteke(directory, filename):
    '''Parse the ads in filename/directory into a dictionary list.'''
    page = vsebina_datoteke(filename, directory)
    blocks = page_to_blocks(page)
    lokali = [get_information_from_block(block) for block in blocks]
    return lokali



#def ads_frontpage():
#return lokali_iz_datoteke(cat_directory, frontpage_filename)


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

def write_csv(fieldnames, rows, directory, filename):
    '''Write a CSV file to directory/filename. The fieldnames must be a list of
    strings, the rows a list of dictionaries each mapping a fieldname to a
    cell-value.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_cat_ads_to_csv(ads, directory, filename):
    '''Write a CSV file containing one ad from "ads" on each row.'''
    write_csv(ads[0].keys(), ads, directory, filename)


def write_cat_csv(ads):
    '''Save "ads" to "cat_directory"/"csv_filename"'''
    write_cat_ads_to_csv(ads, cat_directory, csv_filename)


#lokali_iz_datoteke(r'U:\Programiranje 1\Analiza-podatkov-Programiranje-1', 'Imenik_lokalov_Studentska_prehrana.htm')

blok =  '''row service-1 service-3 service-20 service-21"
         data-lat="46.05249470" data-lon="14.51100380" 
         data-naslov="Trubarjeva cesta 40"
         data-cena="6,53" data-doplacilo="3,90"
         data-posid="1478" 
         data-detailslink="/sl/restaurant/Details/1478"
         data-lokal="ABI FALAFEL" 
         data-city="LJUBLJANA" 
         data-sort-group="65">
        <div class="col-md-12"  data-distance="" >
            <div class="shadow-wrapper">
                <div class="bg-light rounded box-shadow shadow-effect-2">
                    

                    <h2 class="no-margin color-blue">
                        <a href="/sl/restaurant/Details/1478">
                            ABI FALAFEL
                        </a>

                       

                        

                        


                    </h2>


                        
                   

                    <div class="acidjs-rating-stars acidjs-rating-disabled">
                        <form>
                                <input type="radio" name="group-1478" id="1478-0" value="5" /><label for="1478-0"></label>
                                                            <input checked="checked" type="radio" name="group-1478" id="1478-1" value="4" /><label for="1478-1"></label>
                                                            <input type="radio" name="group-1478" id="1478-2" value="3" /><label for="1478-2"></label>
                                                            <input type="radio" name="group-1478" id="1478-3" value="2" /><label for="1478-3"></label>
                                                            <input type="radio" name="group-1478" id="1478-4" value="1" /><label for="1478-4"></label>




                        </form>
                    </div>
                    
                    <br />


                    <small><i>Trubarjeva cesta 40, 1000 Ljubljana</i>
                    <span id="dist_1478" class="pull-right"></span>
                    
                    </small>
       
                    
                    <br />

                    <br />


                    <br />
                    
                    <br />
                    <div class="row">
                        <div class="col col-md-3">
                            <small>
                                <span class="text-bold">Doplačilo : &nbsp;</span>
                                <span class=" color-light-grey">3,90 EUR</span>
                                 
                                <br />
                                <span class="text-bold">Cena obroka : &nbsp;</span>
                                <span class=" color-light-grey">6,53 EUR</span>
                            </small>
                        </div>

'''

page = vsebina_datoteke(r'U:\Programiranje 1\Analiza-podatkov-Programiranje-1', 'Imenik_lokalov_Studentska_prehrana.htm')[:100000]
lokali = []
for block in page_to_blocks(page):
    lokali.append(get_information_from_block(block))
    print(lokali[-1])
    
#print(get_information_from_block(blok))

