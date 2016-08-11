''' 
setup a blueprint database class
and a build class
which then goes through and sets up a blueprint class for each entry
the build class then delivers a basket of items to build for select hubs and the 
shopping list for each of the hubs chosen

'''




class Blue_Print_Database():
    
    blue_print_index = []  #  list of blueprint ID's

    def __init__(self,blue_path,CREST):
        self.blue_path = blue_path
        self.CREST = CREST

    def find_a_BPO(id_number):
        '''
        return name, number of blueprints owned, location et al.
        '''
        pass

    def find_a_BPC(id_number):
        '''
        same as find_a_BPO except for BPC
        '''
        pass

    def list_all_BPO():
        '''
        list set of all BPO
        '''
        pass

    def list_all_BPC():
        '''
        list all BPC
        '''
        pass

    def list_all_Blueprints():
        '''
        list all Blueprints as tuple of ids
        '''
        pass



class Blueprint():
    '''
    base blueprint class
    initialized off of the unique identifier number assigned by EVE

    '''
    def __init__(self, components, ID_num, location, ME, TE, quantity,runs,build_time):
        self.components = components #  
        self.ID_num = ID_num  #  id num as int corresponds to item type i.e. Rupture
        self.location = location #  int 
        self.ME = ME  #  int
        self.TE = TE  #  int
        self.quantity = quantity #  -1 for original -2 for copy 
        self.runs = runs  # int
        self.build_time = build_time #  time in seconds?

    def cost_to_produce():
        pass

    def build_blueprint():
        pass

    def isk_per_hour(self,hub):
        '''
        
        '''
        pass

class Character:

    def __init__(self):
        pass


class xml_api:

    def __init__(self,API_key,use_agent,):
        self.API_key = API_key
        self.use_agent = use_agent
        pass
    
class build_job():
    def __init__(self,blueprints,buy_list):
    self.blueprints = blueprints
    self.buy_list = buy_list


    def find_basket():
        '''
        find the best items to build
        '''











