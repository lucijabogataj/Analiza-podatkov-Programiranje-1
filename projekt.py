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
    rx = re.compile(r'row (?P<lastnosti_ponudbe>)".*?data-lat=
                    r'data-naslov="(?P<naslov>)".*?
                    r'data-cena="(?P<cena>)".*?
                    r'data-doplacilo="(?P<doplacilo>)".*?
                    r'data-lokal="(?P<ime>)" .*?
                    r'data-city="(?P<mesto>)".*?
                    r'checked="checked".*?value="(?P<ocena>)"'
                    , re.DOTALL)
    data = re.search(rx, block)
    slovar_informacij = data.groupdict()
    return slovar_informacij

def ads_from_file(filename, directory):
    '''Parse the ads in filename/directory into a dictionary list.'''
    page = read_file_to_string(filename, directory)
    blocks = page_to_ads(page)
    ads = [get_dict_from_ad_block(block) for block in blocks]
    return ads


def ads_frontpage():
return ads_from_file(cat_directory, frontpage_filename)



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
write_cat_ads_to_csv(ads, cat_directory, csv_filename
