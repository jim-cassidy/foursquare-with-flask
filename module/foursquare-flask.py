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
from app import app
from db_setup import init_db, db_session
from forms import MusicSearchForm
from flask import flash, render_template, request, redirect, url_for
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


 
@app.route("/echo")
def echo():

    conn = sqlite3.connect('saved.db')
    print ("connected...")
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM list")
 
    rows = cur.fetchall()
 
    listvenue = []

    for row in rows:
        listvenue.append(row[0])

 
    
    numberpick = request.args.get('text', '')
   

    writetopage = "<BR>The id you picked is : " + numberpick


 
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
 
  

    venID = request.args.get('text', '') 

    for x in range(1):
      for y in range(1):
          center = distcust(p,distance,x,y)

          
          url = "https://api.foursquare.com/v2/venues/5150ea24e4b01a75860ec291?&client_id=%s&client_secret=%s&v=%s" % ( client_id, client_secret, time.strftime("%Y%m%d"))

       
          try:
              print ("getting venue information.....")

              req = urllib2.Request(url)
              response = urllib2.urlopen(req)
              data = json.loads(response.read())
              requests = req             
 
 
   	      data22 = DataFrame(data["response"])
	     
              response.close     
               
	      aa1 = data22.loc[ [ "canonicalUrl"][0] ]
   	      aa2 = str(aa1)
	      print (aa2)
	      aa3 = aa2.split()
	      aa4 = aa3[1]
	      print (aa4 )
	   

              df2 = DataFrame()
              venue_ids = []
              frames = []
 
              for d in data["id"]:                
                   
                  requested_keys2 = [ "id" ]
                  url2 = "https://api.foursquare.com/v2/venues/4cab5ccf44a8224b3a502d40/%s?client_id=%s&client_secret=%s&v=%s" % (d, client_id, client_secret, time.strftime("%Y%m%d"))
                  req2 = urllib2.Request(url2)
                  response2 = urllib2.urlopen(req2)
                  data2 = json.loads(response2.read())
                  response.close()
                  ddata = data2['response']               

 		  print ("response")
		  print ( data2 )
                 
                  nom_data = json_normalize(ddata['venue'])

                  if "price.currency" not in nom_data.columns:
                      nom_data["price.currency"] = 'NONE'
  
                  if "rating" not in nom_data.columns:
                      nom_data["rating"] = 'NONE'                 

                  venue_ids.append(d)
                  frames.append(nom_data[requested_keys2])
                   
               
                  time.sleep(1)


              df2 = pd.concat(frames, keys=venue_ids)

              mdata = pd.merge(data, df2,how='left',on='id', suffixes=('_x', '_y'))

          
              df = df.append(mdata,ignore_index=True)
              print ( df.id )
           
              time.sleep(1)  
          
          except Exception, e:
              print e
    

    results = []


    return ( "HTTP address" + aa4 ) 

 

 
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
     
    p = {'lat': 40.783011, 'long': -73.965368} # central NYC, at Central Park
 
    distance = 10000
    limit = 50
    gridSize = 10
    df = DataFrame()
    df3 = DataFrame()
    requested_keys = ["categories","id","location","name"]
   
  

    
    if ( choice_made == "Colleges & Universities" ):
      category_id = "4d4b7105d754a06372d81259" 
      
    
    if ( choice_made == "Food" ):
      category_id = "4d4b7105d754a06374d81259"
       

    if ( choice_made == "Event" ):
      category_id = "4d4b7105d754a06373d81259"
      

 
    
 
    for x in range(1):
      for y in range(1):
          print ("**")
          center = distcust(p,distance,x,y)
      
         
          url = "https://api.foursquare.com/v2/venues/search?near=%s,%s&intent=browse&radius=%s&client_id=%s&client_secret=%s&categoryId=%s&v=%s&query=%s" % (location_city, location_state, distance, client_id, client_secret, category_id, time.strftime("%Y%m%d"), search_made)
          
      

          try:
           
              req = urllib2.Request(url)
              response = urllib2.urlopen(req)
              data = json.loads(response.read())
              print (data)
              response.close()
              
              requested_keys = ["name","id"]
              data22 = DataFrame(data["response"]['venues'])[requested_keys]
              
              data22.to_csv("test3.csv")

        
              print("____________")
   

              print ( data22.loc[0][0] )

   
               
             
             

              df2 = DataFrame()
              venue_ids = []
              frames = []

           
              df2 = pd.concat(frames, keys=venue_ids)

              mdata = pd.merge(data, df2,how='left',on='id', suffixes=('_x', '_y'))

          

              df = df.append(mdata,ignore_index=True)
            
           
              time.sleep(1)  
          
          except Exception, e:
              print e
     

    results = []

    lines = ""
   
    print ( data22 )
   
    conn = sqlite3.connect('saved.db')
    print ("connected...")
    cur = conn.cursor()
  
    cur.execute("INSERT INTO list ( names , id ) VALUES ( '110', '120a' )")
    conn.commit()
    print ("executed...")
    c = conn.cursor()
 
    sql = '''INSERT INTO list (names, id) VALUES (?, ?)'''
    
 
    c.execute("DELETE FROM list") 

    counttemp = 0

     


 
    for xx1 in range(10):
      print ( xx1 )
      print ("---")
      print ("name is: " , data22.loc[xx1][0] )
      print ("id is: ", data22.loc[xx1][1] )
   
      lines = lines + "Name: &nbsp;&nbsp;  " + data22.loc[xx1][0] + " <BR>  ID: &nbsp;&nbsp; " + data22.loc[xx1][1] + " <BR> "
      lines = lines + "<BR>"
      aa = data22.loc[xx1][1]
      bb = data22.loc[xx1][0]
      print (aa + " " + bb )
  
      c.execute('INSERT INTO list VALUES(?, ?)', ( aa, bb,) )
      
     
    print ("writing to webpage...")

    conn.commit()
    
   
      
    search_string = search.data['search']
    choice_string = search.data['select']
  
    fullStr = '-'.join(choice_string)
 
    
    print ("choice------------>",fullStr)
    print "".join(choice_string)
    tqry = db_session.query(Album)
    print ("-------------------")
    print (tqry)
    print ("-------------------")
   
    return lines + '<form action="/echo" method="GET"><input name="text"><input type="submit" value="ID"></form>'

    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()

    if not results:
   
        return lines
  	
       
    else:
       
        return "test"
 
if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001)
