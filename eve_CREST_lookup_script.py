import json
import requests
from collections import namedtuple
import sqlite3


#  https://eveonline-third-party-documentation.readthedocs.org/en/latest/
#  https://www.fuzzwork.co.uk/dump/yc118-3-117575/
#  pay attention to the version!!!!
#  plus
#  industryActivityMaterials.csv
#  contains a listing of the blueprint item id,
#  material needed item id and other information
#  probably better to get the sql file and use that

############# project overview ######################

#  run a script to pull out all of the Blueprints darpa owns
#  store it in a database
#  take the output of all those blue prints and poke through the Static Data
#  Export to develop a list of  all the build materials
#  use that list as a reference and store it in a database
#  do a price lookup for the blue print outputs and all the build materials
#  try and figure out the optimal build vs. sell volume of the max number
#  of items that can be produced develop a buy list
#  profit?

# eve kill api example
# https://beta.eve-kill.net/api/kills/solarSystemID/30002187/
# https://beta.eve-kill.net/api/kills/solarSystemID/30002187/no-items/
#
# eve kill docs https://beta.eve-kill.net/api/docs/



# HOW TO USE

#
# populate the visit dictionary opens the json dump from CREST
# it them creates a dictionary of the key info for doing lookups or for
# dropping into a database
#

'''
blue print activities might be
0   None
1   Manufacturing
2   Researching Technology
3   Researching Time Productivity
4   Researching Material Productivity
5   Copying
6   Duplicating
7   Reverse Engineering
8   Invention
'''

# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

items_to_lookup = ['Caracal','Raptor','Rupture','Fenrir']  #  for testing purposes

sol_systems = {
    'Jita': 30000142,
    'Amarr': 30002187,
    'Dodixie':30002659,
    'Rens':30002510,
    'Hek':30002053
    } #system names for price lookups

stations = {
    'Jita 4-4': 60003760,
    'Rens BTT': 60004588,
    'Hek BC': 60005686,
    'Amarr': 60008494,
    'Dodixie 9M10': 60011866
    }

regions = {
    'Metropolis': 10000042,
    'Domain': 10000043,
    'Heimatar': 10000030,
    'The Forge':10000002,
    'Sinq': 10000032
    } 

id_url = r'https://crest-tq.eveonline.com/market/prices/'
# for getting type id's and names i.e. type id 628 = Caracal
# https://developers.eveonline.com/blog/article/the-end-of-public-crest-as-we-know-it

base_url = r'https://crest-tq.eveonline.com/'
market_url = r'/market/'
sell_url = r'/orders/sell/?type=https://crest-tq.eveonline.com/inventory/types/'
buy_url = r'/orders/buy/?type=https://crest-tq.eveonline.com/inventory/types/'

#buy sell example is as follows for trit in metro
#'https://crest-tq.eveonline.com//market/10000042/orders/sell/?type=https://crest-tq.eveonline.com/inventory/types/34/'


# taking the id and then finding prices
buy_sell_url = r'http://api.eve-central.com/api/marketstat/json?&typeid='
# for the api to find the system to find prices for items i.e. Jita or Rens
url_system = r'&usesystem='
url_typeid = r'&typeid='
url_sell = r'/sell/fivePercent' # for eve central's api to find sell prices
url_buy = r'/buy/fivePercent'   # for eve central's api to find buy prices

use_agent = {'user-agent': 'EVE name - Hiro Bukharin, hiro.bukharin@gmail.com'}


id_lookup_dictionary = {}
# the item name = named tuple (.name .e_id .id_num e_href) name, id string, id int, attribute url

def open_CREST_for_id_name(id_url):
    '''
    opens CREST /market/prices endpoint and returns a massive map of the item database
    and returns it as a json object that can then be iterated through to map the item
    number to item name and allow us to do price look ups
    '''
    price_json_object = requests.get(id_url, headers=use_agent)  #lookup the url
    print('opened url with requests')
    return price_json_object.json() # return the results as a json object

    # ['items', 'pageCount_str', 'pageCount', 'totalCount', 'totalCount_str']
    # 'items': returns something like:
    # {'type': {'href': 'https://crest-tq.eveonline.com/types/32772/',
    # 'id_str': '32772', 'id': 32772, 'name': 'Medium Ancillary Shield Booster'},
    # 'averagePrice': 284979.3, 'adjustedPrice': 286018.91}

def populate_item_dictionary(id_lookup_dictionary):
    '''
    gets the json object created from CREST by open_for_id_name and then iterates through the items
    to make a name, id # dictionary for further lookups
    '''
    the_json = open_CREST_for_id_name(id_url) # load the object from CREST
    end_count = the_json['totalCount'] -1
    #  the last number in the range of lists for the sake of making
    #  a range and using it to index the list of items
    a_range = range(0, end_count) # to iterate through the json['items'] list
    for key in a_range:

        eveItem = namedtuple('eveItem',['name','e_id','id_num','e_href']) # create named tuple object

        name = the_json['items'][key]['type']['name'] # item name i.e. Caracal
        e_id = the_json['items'][key]['type']['id_str'] # id string for item
        id_num = the_json['items'][key]['type']['id'] # id integer for Caracal
        e_href = the_json['items'][key]['type']['href'] # url for different attributes

        item = eveItem(name, e_id, id_num, e_href)  #set named tuple with values
        #print('found {name} with id number {a_id}'.format(name=item.name,a_id=item.e_id))
        id_lookup_dictionary[name] = item # set dictionary value = n tuple

def id_lookup(eve_item):
    '''
    takes an item and looks it up in the dictionary of [name]: tuple values
    for each item in the eve database
    '''
    return id_lookup_dictionary[eve_item].e_id

def lookup_sell(SolarSystem='30000142',ItemID='628'):
    '''
    takes a solar system and item id and finds the average
    (I think) sell price on eve central
    '''
    sell_string = '{base_url}{id_string}{system}{solar_system_id}'.format(
        base_url=buy_sell_url, #base url for eve central
        id_string=ItemID,  # item id to be looked up i.e. 628 which is Caracal
        system=url_system, # the string to add to the base url + item id string
        solar_system_id=SolarSystem  # the system i.e. 30000142 which is Jita
        )
        # get the json object from eve central of price data
    sell_price = requests.get(sell_string,headers=use_agent).json()
    return sell_price[0]['sell']['fivePercent'] # return the price we want

def lookup_buy(SolarSystem=sol_systems['Jita'],ItemID='628'):
    '''
    takes a solar system and item id and finds the average
    (I think) buy price on eve central
    '''
    buy_string = '{base_url}{id_string}{system}{solar_system_id}'.format(
        base_url=buy_sell_url,  # base url for eve central
        id_string=ItemID, # item id to be looked up i.e. 628 which is a Caracal
        system=url_system, # the string to add to the base url + item id string
        solar_system_id=SolarSystem # the system  i.e. 30000142 which is Jita
        )
    #  get the json object from eve central of price data
    buy_price = requests.get(buy_string,headers=use_agent).json()
    return buy_price[0]['buy']['fivePercent']

def find_buy_sell_orders(region_id, item_id,buy=True):
    '''
    takes an item ID and region ID and finds the buy orders for that item through CREST
    returning a json object
    '''
    region_id = str(region_id)
    item_id = str(item_id)
    if buy: #  if buy flag is set True find buy information
        
        lookup_url = base_url + market_url + region_id + buy_url + item_id + '/'
        region_buy = requests.get(lookup_url)
        if region_buy.ok:
            return region_buy.json()
        else:
            print('could not retrieve information, status code: ', region_buy.status_code)
    else: #  we want sell information so return sell information 
        lookup_url = base_url + market_url + region_id + sell_url + item_id + '/'
        region_sell = requests.get(lookup_url)
        if region_sell.ok:
            return region_sell.json()
        else:
            print('could not retrive information, status code: ', region_sell.status_code)


def find_average_station_order(region_id, item_id,station_id,buy=True):
    '''
    find the average sell/buy price of the orders for an item for a set region
    refer to CREST_notes.txt for the structure of the JSON response for each order 
    convert id's to text prior to adding them to the endpoint string
    '''
    pass

def 


'''
populate_item_dictionary(id_lookup_dictionary)

print(lookup_sell())
print(lookup_buy())
'''

sell_test = find_buy_sell_orders(regions['Metropolis'], 34, buy=False)
buy_test = find_buy_sell_orders(regions['Metropolis'], 34, buy=True)
print('number of sell orders in metro for trit is ', len(sell_test['items']))
print('number of buy orders in metro for trit is ', len(buy_test['items']))



