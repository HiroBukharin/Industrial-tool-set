import sqlite3
import csv

#reference
#http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

#csv file - need to use '' to bracket strings
#csv_file = 'testbook.csv'
csv_file = 'caseloadtest.csv'

#database name - need to use '' to bracket strings
sqlite_file = 'testload.db'

#tables - need to use '' to bracket strings
tab1 = 'geocodes'
tab2 = 'clients'
tab3 = 'wards'

#for column creation - need to use '' to bracket strings
geocodes = 'address TEXT, lat REAL, long REAL'
visits = 'visit_date TEXT, client_ID INTEGER, l_name TEXT, f_name TEXT, birthday TEXT, gender TEXT, SOI TEXT, \
           address TEXT, city TEXT, p_code TEXT, quantity INTEGER, food_provided TEXT, items TEXT'

wards = 'lat_long TEXT, federal TEXT, provincial TEXT, municipal TEXT, city TEXT'

#for insterting a full row - need to use '' to bracket strings
geocode_r = 'address, lat, long'
visits_r = 'visit_date, client_ID, l_name, f_name, birthday, gender, SOI, \
           address, city, p_code, quantity, food_provided, items'
wards_r = 'lat_long, federal, provincial, municipal, city'


#create/connect database
def connect(dbase_name):
    global conn
    try:
        conn = sqlite3.connect(dbase_name)
    #Once you have a Connection, you can create a Cursor object and call its execute() method to perform SQL commands:
        global c
        c = conn.cursor()
    except Exception as e:
        print('ERROR: {}'.format(e))


def create_table(dbase_name,table_name,fields):
    """
    This will connect to or create a database, with a table and fields as specified 
    """
    connect(dbase_name) # connect 
    try:
        c.execute("CREATE TABLE IF NOT EXISTS \
        {table} ({field})".format(table=table_name,field=fields)) # create table and fields
        conn.commit()  # commit
    except Exception as e:
        print('ERROR: {}'.format(e))
        conn.rollback() # reverse in case of error
        raise e
    finally:
        conn.close() # close

def insert_values(dbase_name,table_name,table_columns,values):
    
    connect(dbase_name) # connect or create
    try:
        c.execute("INSERT INTO {tab} ({columns}) VALUES ({the_values})".\
            format(tab=table_name, columns=table_columns, the_values=values))
        conn.commit()  # commit
        conn.close()
    except Exception as e:
        conn.close()
        print('ERROR: {}'.format(e))

def select_and_return_all(dbase_name, search_tab,heading,cell_value):
#def select_and_return(dbase_name):
    '''
    for fetchall lookups
    '''
    connect(dbase_name)
    try:
        c.execute("SELECT * FROM {tn} WHERE {col_value}={vtf}".\
        format(tn=search_tab, col_value=heading,vtf=cell_value))
        all_rows = c.fetchall()
        conn.close()
        return all_rows
        
    except Exception as e:
        conn.close()
        print('ERROR: {}'.format(e))

#csv open function
def open_and_insert_from_file(file,database='I am script test3.db',table="'space vessel'"):

    try:
        with open(file, newline='') as f:
            item_list = csv.reader(f)
            for item in item_list:
                one = item[0]    # add variables for each cell in the row                 
                two = item[1]    # add variables for each cell in the row 
                write_string = "'" + one + "',"  + two  # assemble 
                # text requres the "'" + TEXT + "'," 
                # integers requres no bracketing but should not be converted to int() when opening
                # "," is required between entries
                insert_values(database,table,'name, number', write_string)
                

    except Exception as error:
        print(error)

def open_and_insert_from_file_clients(file,database='I am script test3.db',table="'space vessel'",headers=visits_r):

    try:
        with open(file, newline='') as f:
            item_list = csv.reader(f)
            for item in item_list:

                #errors will occur if the cell has nothing in it
                #a default value will need to be inserted prior, or code will need to be
                #written to parse the strings opened from the file
                
                zero = item[0]      # add variables for each cell in the row                 
                one = item[1]       # add variables for each cell in the row
                two =item[2]        # and so on....
                three =item[3]
                four =item[4]
                five =item[5]
                six =item[6]
                seven =item[7]
                eight =item[8]
                nine =item[9]
                ten =item[10]
                eleven =item[11]
                twelve=item[12]

                # formatted string to insert into the SQL statement
                # integer/real do not need an additional ' but TEXT DOES
                write_string = "'" + zero + "',"  + one + ',' + "'" + two + "'," + "'" + three + "',"   \
                               + "'" + four + "'," + "'" + five + "'," + "'" + six + "'," \
                               + "'" + seven + "'," + "'" + eight + "'," + "'" + nine + "'," \
                               + "'" + ten + "'," + "'" + eleven + "'," + "'" + twelve + "'" # make sure not to have an additional comma
                
                print(write_string)

                # text requres the "'" + TEXT + "'," 
                # integers requres no bracketing but should not be converted to int() when opening
                # "," is required between entries

                insert_values(database,table,headers, write_string)
                

    except Exception as error:
        print(error)





def open_and_return(database=sqlite_file,table=tab2,col_name='f_name',value_to_find="'Matt'"):
    results = select_and_return_all(database,table,col_name,value_to_find)
    print(results)
    
   
#create_table('I am script test3.db',"'space vessel'",'name TEXT, number INTEGER') #works: note quote placement
#insert_values('I am script test3.db',"'space vessel'",'name, number',"'Rupture', 1")#works: note quote placement
#print(select_and_return_all('I am script test3.db',"'space vessel'",'name',"'Rupture'"))
#open_and_insert_from_file(csv_file)
#print(select_and_return_all('I am script test3.db',"'space vessel'",'name',"'Rupture'"))


#create_table(sqlite_file,tab2,visits) #works!
#insert_values(sqlite_file,tab2,visits)#works: note quote placement
        
#print(select_and_return_all('I am script test3.db',"'space vessel'",'name',"'Rupture'"))
#open_and_insert_from_file_clients(file=csv_file,database=sqlite_file,table=tab2,headers=visits_r)

open_and_return()









