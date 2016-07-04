import sqlite3
from collections import defaultdict

SDE_path = r'/home/pi/EVE_data/sqlite-latest.sqlite'
BPO_db = r'/home/pi/scripts/eve/DARPA_blueprints.db'
#  All_blueprints :
#  key, time_efficiency, type_id, type_name, quantity, location_id,
#  material_efficiency, runs

buy_list = defaultdict(int)



'''
#create a dictionary of ID : 'text name'
ID_name = {}
for x in number_name:
    ID_name[x[0]]=x[1]
#close the datbase connection
conn.close()


# connect to DARPA blueprints
conn = sqlite3.connect('DARPA_blueprints.db')
cursor = conn.cursor()
'''

def find_name(id_num):
    '''
    takes an id number and finds the plain text name 
    '''
    id_str = str(id_num)
    conn = sqlite3.connect(SDE_path)
    cursor = conn.cursor()
    name = cursor.execute("SELECT typeName FROM invTypes WHERE typeID = ?",(id_num,))
    name_tup = name.fetchone()
    conn.close
    return name_tup[0]

def find_id(item_name):
    '''
    takes an item name and finds the id number
    '''
    conn = sqlite3.connect(SDE_path)
    cursor = conn.cursor()
    id_number = cursor.execute("SELECT typeID FROM invTypes WHERE typeName = ?",(item_name,))
    the_num = id_number.fetchone()
    conn.close
    return the_num[0]

def find_materials(item_ident):
    '''
    takes a item id and returns the build requirements
    '''
    conn = sqlite3.connect(SDE_path)
    cursor = conn.cursor()
    build = cursor.execute("""
    SELECT materialTypeID,quantity
    FROM invTypeMaterials
    WHERE typeID = ?
    """,(item_ident,)
                           )
    
    materials = build.fetchall()
    conn.close
    return materials

def extract_BPO_list():
    '''
    extracts a set of BPOs from the database and returns them as a dictionary
    '''
    conn = sqlite3.connect(BPO_db)
    cursor = conn.cursor()
    name_id = cursor.execute("""SELECT type_id, type_name FROM All_blueprints 
                             WHERE quantity = -1""") #  find all BPO's
    BPO = name_id.fetchall() #  fetch them
    conn.close #  close db connection
    def_dictionary = defaultdict(int)
    for each_tuple in BPO:
        BP_name = each_tuple[1]
        BP_id = each_tuple[0]
        if def_dictionary[BP_name]: # if there is already an entry skip
            pass
        else:
            def_dictionary[BP_name] = BP_id #  enter a value

    return def_dictionary



def extract_material_list_all():
    '''
    extracts a set of materials needed to build all of the BPOs
    '''
    BPO_names = extract_BPO_list()
    

    for e_p in BPO_names:  #  for each blueprint in BPO_names
        p_name = e_p[0].strip(' Blueprint') #  this is the product name
        p_id = find_name(p_name) # this is the id number
        components = find_materials(p_id) #  use the id number to find the build list
        for pair in components:
            m_id = pair[0] #  material ID
            amount = pair[1] #  amount of material
            


print(find_id('Medium Processor Overclocking Unit I'))


