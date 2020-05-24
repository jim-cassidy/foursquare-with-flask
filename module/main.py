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


def distcust(p, d, lat_m, long_m):
    lat = p['lat']
    long = p['long']

    lat1 = lat + lat_m * (d / (11100.0/90*1000) * cos(lat))
    long1 = long + long_m * (d / (11100.0/90*1000))

    return {'lat': lat1, 'long': long1}


init_db()



@app.route('/', methods=['GET', 'POST'])
def index():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    writetoscreen = 'write'
  
    test = ['one', 'two', 'three'] 
    test.append('four') 

    ##### 
    ## foursquare code   

    client_id = "JAH2Y0HES01BIMCMSRULSHTXIVUYLOQPGNJBIC0LWJ4KWMUL"
    client_secret = "GEZ1UJJVLK5YIXKZPMG03UBNBYHMJPA52NAEDO1GSP5IL1PA"
     #p = {'lat': 37.7833, 'long': -122.4167}    # central San Francisco, at Van Ness and Market
    p = {'lat': 40.783011, 'long': -73.965368} # central NYC, at Central Park
 
    distance = 500
    limit = 1
    gridSize = 1
    df = DataFrame()
  #  requested_keys = ["categories","id","location","name"]
    requested_keys = [ "name"]
    category = "high school"
    category_id = "4bf58dd8d48988d13d941735"

    

    #for x in [x1 / 10.0 for x1 in range(-3*gridSize, 3*gridSize)]:
     # for y in [y1 / 10.0 for y1 in range(-3*gridSize, 3*gridSize)]:

    for x in range(1):
      for y in range(1):



          center = distcust(p,distance,x,y)
          url = "https://api.foursquare.com/v2/venues/search?ll=%s,%s&intent=browse&radius=%s&categoryId=%s&client_id=%s&client_secret=%s&v=%s" % (center["lat"], center["long"], distance, category_id, client_id, client_secret, time.strftime("%Y%m%d"))
          try:
              req = urllib2.Request(url)
              response = urllib2.urlopen(req)
              data = json.loads(response.read())
              response.close()
           #   print data["response"]['venues']
              writetoscreen = data["response"]['venues']
            #  print ( writetoscreen )
              data = DataFrame(data["response"]['venues'])
              dataA = str(data)
              dataB = dataA.splitlines()
              
            
              print ("---------------------------------")
              df2 = DataFrame()
              venue_ids = []
              frames = []

              #print data["id"]
              for d in data["id"]:                
                  requested_keys2 = ["id", "price.currency","rating", "likes.count"]

                  url2 = "https://api.foursquare.com/v2/venues/%s?client_id=%s&client_secret=%s&v=%s" % (d, client_id, client_secret, time.strftime("%Y%m%d"))
                  req2 = urllib2.Request(url2)
                  response2 = urllib2.urlopen(req2)
                  data2 = json.loads(response2.read())
                  response.close()
                  ddata = data2['response']               


                  writetoscreen = ddata
               #   print ( ddata )
               #   print ("*ddata*")
                  nom_data = json_normalize(ddata['venue'])

                  if "price.currency" not in nom_data.columns:
                      nom_data["price.currency"] = 'NONE'
  
                  if "rating" not in nom_data.columns:
                      nom_data["rating"] = 'NONE'                 

                  venue_ids.append(d)
                  frames.append(nom_data[requested_keys2])
                  print ("getting attr for %s" % nom_data["name"])
                  test.append( nom_data["name"] )
                  print ("******************************") 
                 

                  print ("******************************")

                  time.sleep(1)


              df2 = pd.concat(frames, keys=venue_ids)

              mdata = pd.merge(data, df2,how='left',on='id', suffixes=('_x', '_y'))

        #      print mdata

              df = df.append(mdata,ignore_index=True)
         #     print df
  
              df.to_csv("test.csv")

              
                        

             
              time.sleep(1) # stay within API limits
          
          except Exception, e:
              req = urllib2.Request(url)
              response = urllib2.urlopen(req)
              data = json.loads(response.read())
              response.close()
           #   print data["response"]['venues']
              writetoscreen = data["response"]['venues']
            #  print ( writetoscreen )
              data = DataFrame(data["response"]['venues'])
              dataA = str(data)
              dataB = dataA.splitlines()
          
  
               
              strC = "test"
              
              #print ( data["name"] )
              strA = data["name"]
              strB = str (strA) 
              strC = strB.splitlines()

              for xx in range(0,len(strC)-1):
                printlines = strC[xx]
              #  print ( printlines[5:50] )

  
              strD = strC[0]
              strE = strD[5:50]
              print ( strE )
              print ("---------------------------------")
              df2 = DataFrame()
              venue_ids = []
              frames = []
             # print ("!!")
             # print e



    #####


    results = []
    search_string = search.data['search']
    
   
    printlines2 = ""
    

    if search.data['search'] == '':
        qry = db_session.query(Album)
        results = qry.all()


    if not results:
        for xx in range(0,len(strC)-1):
                printlines = strC[xx]
                print ( printlines[5:50] )
                printlines2 = printlines2 + printlines[5:50] 
                printlines2 = printlines2 + "<br/>"
        flash(strE)
    #    return redirect('/')
        return printlines2
    else:
        # display results
        return printlines2
       # return render_template('results.html', table=table)

if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(port=5001)
