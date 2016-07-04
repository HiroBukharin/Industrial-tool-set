import evelink.api  # Raw API access
import evelink.char # Wrapped API access for the /char/ API path
import evelink.eve  # Wrapped API access for the /eve/ API path
import evelink.corp

import sqlite3
import pprint


toon_id = {'mal' : 1884321982, #character ID's 
           'fanya':1640056941,
           'blackwater': 1272029543,
           'kropotkin': 941378046,
           'tesla': 1225771468,
           'cayce': 91959782,
           'gurney': 543244546,
           'waru': 1323311973,
           'bobby': 91355265
           }

# for reference:
# https://github.com/eve-val/evelink/wiki/EVEAPITree


cap_key = (5320499, 'hqmPW4Z3WXjmElWf22wKslljYzHhKn7xAQVZ67pMU4M2DtwuM3b5Qqq83FZgFzjB')
cap_corp_key = (5320542, 'GmaBItPtQxIRdIWTBnAShnJX6kN4KZmotckRtf5t2H2ojvfSuaUaCb0gg5g8GfQD')



eve = evelink.eve.EVE()

# character
'''
api = evelink.api.API(api_key=cap_key)
id_response = eve.character_id_from_name("Character Name")
char = evelink.char.Char(char_id=id_response.result, api=api)
balance_response = char.wallet_balance()

print(balance_response.result)
'''


# corporation
api = evelink.api.API(api_key=cap_corp_key)
darpa = evelink.corp.Corp(api)
#active_jobs = darpa.industry_jobs()

#darpa_jobs = active_jobs.result # returns a dictionary
#print(indy_string.keys())

blue_prints = darpa.blueprints()
darpa_blue = blue_prints.result # returns a dictionary with over 10k keys >.<

'''
http://test-eveonline-third-party-documentation.readthedocs.io/en/latest/xmlapi/character/char_blueprints.html

{'time_efficiency': 20,
'type_id': 12067,
'type_id''type_name': '100MN Afterburner I Blueprint',
'location_flag': 0,
'quantity': -2, ################## -1 = original -2=copy ###########
'location_id': 1019805427658,
'material_efficiency': 10,
'runs': 60}
'''


# connect to database
# http://www.blog.pythonlibrary.org/2012/07/18/python-a-simple-step-by-step-sqlite-tutorial/

conn = sqlite3.connect('DARPA_blueprints.db')
cursor = conn.cursor()

#iterate through the contents of the darpa_blue dictionary

for key in darpa_blue:
    blue_frame = (key,
                  darpa_blue[key]['time_efficiency'],
                  darpa_blue[key]['type_id'],
                  darpa_blue[key]['type_name'],
                  darpa_blue[key]['quantity'],
                  darpa_blue[key]['location_id'],
                  darpa_blue[key]['material_efficiency'],
                  darpa_blue[key]['runs'])

    cursor.execute("INSERT INTO All_blueprints VALUES (?,?,?,?,?,?,?,?)",blue_frame)
    conn.commit()    
    
    

