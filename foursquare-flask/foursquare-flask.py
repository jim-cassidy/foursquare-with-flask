import urllib
import urllib2
import json
import datetime
import pandas as pd
from pandas.io.json import json_normalize
import math
import time
from math import cos
from pandas import DataFrame

# main.py

from app import app
from db_setup import init_db, db_session
from forms import MusicSearchForm
from flask import flash, render_template, request, redirect
from models import Album
import flask

import sqlite3

def distcust(p, d, lat_m, long_m):

    lat = p['lat']
    long = p['long']

    lat1 = lat + lat_m * (d / (11100.0/90*1000) * cos(lat))
    long1 = long + long_m * (d / (11100.0/90*1000))

    return {'lat': lat1, 'long': long1}

init_db()


@app.route("/e")
def hello():
    return '<form action="/echo" method="GET"><input name="text"><input type="submit" value="Echo"></form>'
 
@app.route("/echo")
def echo():

    conn = sqlite3.connect('saved.db')
    print ("connected...")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM list")
 
    rows = cur.fetchall()
 
    listvenue = []

    for row in rows:
       # print("Venue num: " + row + " Venue name: " + row[0])
        listvenue.append(row[0])

    print ( "venue" )
    print ( listvenue[0] )
    
    numberpick = request.args.get('text', '')
   # numberpick2 = int(numberpick)    

    #print ("numberpick:" + numberpick + "-----")
    
    #print ( listvenue[numberpick2] )

    writetopage = "<BR>The id you picked is : " + numberpick



## -------****************************************************************

    ##### 
    ## foursquare code   
   
  

    client_id = "JAH2Y0HES01BIMCMSRULSHTXIVUYLOQPGNJBIC0LWJ4KWMUL"
    client_secret = "GEZ1UJJVLK5YIXKZPMG03UBNBYHMJPA52NAEDO1GSP5IL1PA"
     #p = {'lat': 37.7833, 'long': -122.4167}    # central San Francisco, at Van Ness and Market
    p = {'lat': 40.783011, 'long': -73.965368} # central NYC, at Central Park
 
    distance = 100000
    limit = 20
    gridSize = 10
    df = DataFrame()
    df3 = DataFrame()
    requested_keys = ["categories","id","location","name"]
    category = "food"
  #  category_id = "4d4b7105d754a06374d81259"

    
    if ( choice_made == "Colleges & Universities" ):
      category_id = "4d4b7105d754a06372d81259"
    choice_made = "Food"
   # if ( choice_made == "Food" ):
    category_id = "4d4b7105d754a06374d81259"
   #   print ("FOOD!!!!!!!!!!!!!!!!!!!!!!!!")




    venID = request.args.get('text', '') 

    for x in range(1):
      for y in range(1):
          center = distcust(p,distance,x,y)

          
          url = "https://api.foursquare.com/v2/venues/5150ea24e4b01a75860ec291?&client_id=%s&client_secret=%s&v=%s" % ( client_id, client_secret, time.strftime("%Y%m%d"))

       #   url = "https://api.foursquare.com/v2/venues/VENUE_ID='5150ea24e4b01a75860ec291'?client_id=%s&client_secret=%s&v=%s" % ( client_id, client_secret, time.strftime("%Y%m%d"))
          #url = "https://api.foursquare.com/v2/venues/5e9a2961aba297001b699f51/tips"
       #   url = "https://api.foursquare.com/v2/venues/venueID='5e9a2961aba297001b699f51'?near=%s,%s&intent=browse&radius=%s&category_id=%s&client_id=%s&client_secret=%s&v=%s" % ("Newton", "NJ", distance, category_id, client_id, client_secret, time.strftime("%Y%m%d")
       #  url = "https://api.foursquare.com/v2/venues/search?near=%s,%s&intent=browse&radius=%s&category_id=%s&client_id=%s&client_secret=%s&v=%s&query=%s" % ("Newton", "NJ", distance, category_id, client_id, client_secret, time.strftime("%Y%m%d"),choice_made)
          try:
              print ("trying..")

              req = urllib2.Request(url)
              response = urllib2.urlopen(req)
              data = json.loads(response.read())
              requests = req             
 
              print ( data )

              tips='https://api.foursquare.com/v2/venues/5150ea24e4b01a75860ec291/tips'

              params=dict(client_id=client_id,client_secret=client_secret,v='20200414')

              resp_tips=requests.get(url=tips, params=params)

              data_tips=json.loads(resp_tips.text)

          #    print ( resp_tips )

            
              print (data)
              print ("\n")
              print ("?????????????")
              response.close()
              #print data["response"]['venues']
              data22 = DataFrame(data["response"]['venues'])[requested_keys]
              data22.to_csv("test3.csv")



              df2 = DataFrame()
              venue_ids = []
              frames = []

              #print data["id"]
              for d in data["id"]:                
                  #requested_keys2 = ["id", "price.currency","rating", "likes.count"]
                  requested_keys2 = [ "id" ]
                  url2 = "https://api.foursquare.com/v2/venues/%s?client_id=%s&client_secret=%s&v=%s" % (d, client_id, client_secret, time.strftime("%Y%m%d"))
                  req2 = urllib2.Request(url2)
                  response2 = urllib2.urlopen(req2)
                  data2 = json.loads(response2.read())
                  response.close()
                  ddata = data2['response']               

                 
                  nom_data = json_normalize(ddata['venue'])

                  if "price.currency" not in nom_data.columns:
                      nom_data["price.currency"] = 'NONE'
  
                  if "rating" not in nom_data.columns:
                      nom_data["rating"] = 'NONE'                 

                  venue_ids.append(d)
                  frames.append(nom_data[requested_keys2])
                   
               #   print "getting attr for %s" % nom_data["name"]
                  time.sleep(1)


              df2 = pd.concat(frames, keys=venue_ids)

              mdata = pd.merge(data, df2,how='left',on='id', suffixes=('_x', '_y'))

            #  print mdata

              df = df.append(mdata,ignore_index=True)
              print ( df.id )
            #  print df
  
             # df.to_csv("test.csv")

           #   print center
              time.sleep(1) # stay within API limits
          
          except Exception, e:
              print e
    #####
    #render_template('index.html', form=search)

    results = []

    print ("DF _-----------------------------------")
    print (df)
    print ("---------------------------------------")



    # return "You picked number: " + request.args.get('text', '')
    return ("You picked number: " + request.args.get('text', '') + writetopage) 
 

    # -----------------------

@app.route("/test", methods=['GET', 'POST'])
def test():
  
    print (request.args.get('fname', ''))

    conn = sqlite3.connect('saved.db')
    c = conn.cursor()

    c.execute('SELECT * FROM list')
    aa =  c.fetchone()
    return aa

@app.route('/', methods=['GET', 'POST'])
def index():
    print ("!!")
    search = MusicSearchForm(request.form)

    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    ##### 
    ## foursquare code   
   
    

    search_string = search.data['search']
    choice_string = search.data['select']
    location_city = search.data['locationcity']
    location_state = search.data['locationstate']

    test11 = search.data['locationcity']
    print ( test11 )
     
    search_made = ''.join(search_string)    
    choice_made = ''.join(choice_string)
    

    client_id = "JAH2Y0HES01BIMCMSRULSHTXIVUYLOQPGNJBIC0LWJ4KWMUL"
    client_secret = "GEZ1UJJVLK5YIXKZPMG03UBNBYHMJPA52NAEDO1GSP5IL1PA"
     #p = {'lat': 37.7833, 'long': -122.4167}    # central San Francisco, at Van Ness and Market
    p = {'lat': 40.783011, 'long': -73.965368} # central NYC, at Central Park
 
    distance = 10000
    limit = 50
    gridSize = 10
    df = DataFrame()
    df3 = DataFrame()
    requested_keys = ["categories","id","location","name"]
   
  #  category_id = "4d4b7105d754a06374d81259"

    
    if ( choice_made == "Colleges & Universities" ):
      category_id = "4d4b7105d754a06372d81259" 
      print("COLLEGES!!!!!!!!!!!!!!!!!!!!!")
    
    if ( choice_made == "Food" ):
      category_id = "4d4b7105d754a06374d81259"
      print ("FOOD!!!!!!!!!!!!!!!!!!!!!!!!")

    if ( choice_made == "Event" ):
      category_id = "4d4b7105d754a06373d81259"
      print ("Event!!!!!!!!!!!!!!!!!!!!!!!!")

 
    
 
    for x in range(1):
      for y in range(1):
          print ("**")
          center = distcust(p,distance,x,y)
      
         
          url = "https://api.foursquare.com/v2/venues/search?near=%s,%s&intent=browse&radius=%s&client_id=%s&client_secret=%s&categoryId=%s&v=%s&query=%s" % (location_city, location_state, distance, client_id, client_secret, category_id, time.strftime("%Y%m%d"), search_made)
          
        #     url1 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}&locale={}&categoryId={}'.format(CLIENT_ID, CLIENT_SECRET, lat, lng, VERSION, search_query, radius, LIMIT, locale, categoryId)


          try:
           
              req = urllib2.Request(url)
              response = urllib2.urlopen(req)
              data = json.loads(response.read())
              print (data)
              response.close()
              #print data["response"]['venues'] 
              requested_keys = ["name","id"]
              data22 = DataFrame(data["response"]['venues'])[requested_keys]
              
              data22.to_csv("test3.csv")

          #    print("____________")
          #    print (data22['name'] )
              print("____________")
   

              print ( data22.loc[0][0] )

   #           for xx5 in data22['name']:
    #            print (xx5)
               
             
              print ("______!!_____")            

              df2 = DataFrame()
              venue_ids = []
              frames = []

           
              df2 = pd.concat(frames, keys=venue_ids)

              mdata = pd.merge(data, df2,how='left',on='id', suffixes=('_x', '_y'))

            #  print mdata

              df = df.append(mdata,ignore_index=True)
            #  print df
  
             # df.to_csv("test.csv")

           #   print center
              time.sleep(1) # stay within API limits
          
          except Exception, e:
              print e
    #####
    #render_template('index.html', form=search)

    results = []

    lines = ""
  
  #  flash ( data22['name'].to_json() )
  #  print (data22['name'])

 
    print ( data22 )
    print ("**************")
 
    conn = sqlite3.connect('saved.db')
    print ("connected...")
    cur = conn.cursor()
   # cur.execute("PRAGMA table_info(students)")
    cur.execute("INSERT INTO list ( names , id ) VALUES ( '110', '120a' )")
    conn.commit()
    print ("executed...")
    c = conn.cursor()
  #  c.execute('CREATE TABLE list ( names varchar(20) )')
    sql = '''INSERT INTO list (names, id) VALUES (?, ?)'''
   # c.execute("INSERT INTO list ( names ) VALUES ( 'zzz' )")
   # c.executemany(sql,')
 
    c.execute("DELETE FROM list") 

    counttemp = 0

     


#    for xx1 in data22['id']:
    for xx1 in range(10):
      print ( xx1 )
      print ("---")
      print ("name is: " , data22.loc[xx1][0] )
      print ("id is: ", data22.loc[xx1][1] )
   #   flash ( xx1 )
   #   flash ("-----") 
      lines = lines + "Name: " + data22.loc[xx1][0] + "ID:" + data22.loc[xx1][1]
      lines = lines + "<BR>"
      aa = data22.loc[xx1][1]
      bb = data22.loc[xx1][0]
      print (aa + " " + bb )
  
      c.execute('INSERT INTO list VALUES(?, ?)', ( aa, bb,) )
      
     
    print ("writing to webpage...")

    conn.commit()
    # Preparing SQL queries to INSERT a record into the database.

    lines = lines + "<form action='/e'>  <label for='fname'>First name:<label><br> <input type='text' id='fname' name='fname' value='John'><br>   <label for='lname'>Last name:<label><br> <input type='text' id='lname' name='lname' value='Doe'><br><br><input type='submit' value='Submit'> </form>"  
      
    search_string = search.data['search']
    choice_string = search.data['select']
  
    fullStr = '-'.join(choice_string)
 
    #flash (search_string)
    #flash ( choice_string[0] )
    print ("choice------------>",fullStr)
    print "".join(choice_string)
    tqry = db_session.query(Album)
    print ("-------------------")
    print (tqry)
    print ("-------------------")
   
    return lines + '<form action="/echo" method="GET"><input name="text"><input type="submit" value="Echo"></form>'

    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()

    if not results:
      #  flash('No results found!')
        return lines
  	
        #return redirect('/')
    else:
        # display results
        #return render_template('results.html', table=table) 
        return "test"
 
if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001)
