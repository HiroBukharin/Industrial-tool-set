
'''
This script does a variety functions related to the blueprint database
eve_blueprint_database_maker.py sets up the database and basic tables
this script extracts various features from the SDE and inserts them
into BPO_db 
the eve_CREST_lookup_script.py can update price information

'''


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
    takes an id number and finds the plain text name as a string
    '''
    #id_str = str(id_num)
    conn = sqlite3.connect(SDE_path)
    cursor = conn.cursor()
    name = cursor.execute("SELECT typeName FROM invTypes WHERE typeID = ?",(id_num,))
    name_tup = name.fetchone()
    
    conn.close
    return name_tup[0]

def find_id(item_name):
    '''
    takes an item name and finds the id number as an int
    '''
    conn = sqlite3.connect(SDE_path)
    cursor = conn.cursor()
    id_number = cursor.execute("SELECT typeID FROM invTypes WHERE typeName = ?",(item_name,))
    the_num = id_number.fetchone()
    conn.close
    if the_num:
        return the_num[0]
    else:
        return None

def find_materials(item_ident):
    '''
    takes a item id and returns the build requirements as a collection of tuples
    '''
    if item_ident:
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
    else:
        return None

def extract_BPO_list(BPO_database):
    '''
    extracts a set of BPOs from the database and returns them as a dictionary
    '''
    conn = sqlite3.connect(BPO_database) #  the database that contains all corp BPOs
    cursor = conn.cursor()
    name_id = cursor.execute("""SELECT type_id, type_name FROM All_blueprints 
                             WHERE quantity = -1""") #  find all BPO's
    BPO = name_id.fetchall() #  fetch them, a collection of (id,name)tuples
    conn.close #  close db connection
    def_dictionary = defaultdict(int)
    for each_tuple in BPO:
        BP_name = each_tuple[1]
        BP_id = each_tuple[0]
        if def_dictionary[BP_name]: # if there is already an entry skip
            pass
        else:
            def_dictionary[BP_name] = BP_id #  enter a value

    return def_dictionary #  a reconstructed dictionary of id: name

def extract_material_list_all():
    '''
    extracts a set of materials needed to build all of the BPOs and returns
    them as a list
    '''
    BPO_names = extract_BPO_list(BPO_db)
    print(len(BPO_names), '# of BPO')
    materials = []
    for e_p in BPO_names:  #  for each blueprint in BPO_names
       
        p_name = e_p[:-10].strip() #  this is the product name - 'Blueprint'

        if p_name: #  if the product is present

            p_id = find_id(p_name) # this is the product id number
            
            component = find_materials(p_id) #  use the id number to find the build list
            
            if component:  #  if the item can still be built i.e it hasn't been purged from the db
                for pair in component: # loop through tuples to get name of the building material id
                    m_id = pair[0] #  material name
                    amount = pair[1] #  amount of material                    
                    if m_id not in materials: materials.append(m_id) #  add the name to list
            else:
                print('could not find components for, ',p_name)
        else:
            print(p_name, 'p_name error')
        
    return materials # return a list of all the material IDs needed to build all the BPO



def build_materials_database():
    '''
    pop the items off the list and insert them into a price database

    '''
    conn = sqlite3.connect(BPO_db)
    cursor= conn.cursor()

    building_blocks = extract_material_list_all() #  take the list of building materials
    
    for material in range((len(building_blocks))): #  for each item in the list
        build_material = cursor.execute("""INSERT INTO Build_Materials(ID,price) VALUES (?,?) 
                                        """,(building_blocks.pop(),0))
        conn.commit()

    conn.close()
    

                          


#comps = extract_material_list_all()
#print(find_materials(find_id('Rupture')))# find the id number and then building materials for a rupture






