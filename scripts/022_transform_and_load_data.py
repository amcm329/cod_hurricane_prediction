"""
  The following code performs these operations: 
  1.- Calls 021_download_data.py to get the URLs of pdfs related to hurricanes.
  2.- Dumps information from the pdfs and saves it as txts.
  3.- Checks each one of the txts and extracts only quantitative information. 
  regarding hurricane behavior.
  4.- Concatenates all this information into a pandas dataframe.
  5.- Appends Meteostat information to the dataframe.
"""

#Section for environment variables: 
import os

full_path = os.getenv("OPERATING_SYSTEM_PATH")
     
if full_path is None: 
   #Element doesn't exist.
   os.environ["OPERATING_SYSTEM_PATH"] = "/home/cdsw/"

import re
import json
import math
import time
import wget
import PyPDF2 
import pdfplumber
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from meteostat import Point, Daily, Hourly, Stations


"""
  Auxiliary function for Step 2.
"""
def convert2text(current_file):
    contract_file = current_file
    contract_text = ''
    with pdfplumber.open(contract_file, laparams = { "all_texts": True }) as pdfppp:
        num_pag = pdfppp.pages
        my_len = len(num_pag)
        
        for i in range(my_len):
            texto_aux = num_pag[i].filter(lambda obj: obj.get("text") != " ")
            contract_text = contract_text + '\n' + texto_aux.extract_text(x_tolerance=1)
    
    return contract_text[1:]


""" 
  Auxiliary function created for step 4. 
"""
def clean_1(x):
  return x.replace('/ ', '')


"""
  Auxiliary function created for step 4.
"""
def clean_2(x):
  return x.replace('/', ' ')

"""
   Auxiliary function for step 5 that, based on the latitude and longitude, gathers the closests meteorological locations whitin a radius of  1.5 KM
T  his is used to obtain the most accurate information for a given position
"""
def closest_stations(row):

    current_latitude = row["latitude"]
    current_longitude = row["longitude"]

    local_stations_dict = df_stations_dict.copy()

    list_closest_stations_id = []
    list_closest_stations_distance = []
    list_closest_stations_elevation = []
    stations_keys = list(df_stations_dict.keys())

    for current_station in local_stations_dict.keys():
        current_local_station_latitude = local_stations_dict[current_station]["latitude"]
        current_local_station_longitude =  local_stations_dict[current_station]["longitude"]

        #Calculating the euclidean distance from the current point to all the stations.
        local_stations_dict[current_station]["euclidean_distance"] = math.sqrt((current_latitude - current_local_station_latitude)**2 + (current_longitude - current_local_station_longitude)**2)

    #Sorting the closests stations in ascending order.
    local_stations_sorted = sorted(local_stations_dict.items(), key=lambda x: x[1]['euclidean_distance'], reverse=False)

    for final_local_station in local_stations_sorted:
        current_dictionary = final_local_station[1]
        current_distance = current_dictionary["euclidean_distance"]

        #This is the threshold, which means that the stations within a radius of 1.5 KM.
        if current_distance <= 1.5:
           list_closest_stations_id.append(final_local_station[0])
           list_closest_stations_distance.append(current_distance)
           list_closest_stations_elevation.append(current_dictionary["elevation"])

    row["closest_stations"] = list_closest_stations_id

    return row







"""
  The following operation gathers all the steps mentioned previously.
"""
def clean_and_transform_data():

    #Step 1: retrieving all the valid urls from the NOAA website.
    print("Executing step 1...")
    !scrapy runspider scraper.py

    #Step 2: getting all pds based on the mentioned links.
    print("Executing step 2...")
    handler = open(os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/url_links.txt","a")
    lines = handler.read_lines()
    handler.close()

    for complete_url in lines: 
        filename = wget.download(complete_url, out = os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/pdfs")

   
    #Step 3: Extracting quantitative information from pdfs.  
    print("Executing step 3...")
    for filename in os.listdir(os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/pdfs/"):
        if "pdf" in filename: 
           fullpath = os.path.join(os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/pdfs/", filename)
           txt_file_name = fullpath.replace("pdf","txt")
           text_file = open(txt_file_name, 'wt')
           text = convert2text(fullpath)
           text_file.write(text)
           text_file.close()

    print('Last file: ', filename)

    #Step 4: Extracting relevant information from the txt.
    print("Executing step 4...")

    #Variable created to gather monthly information.
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    input_path = os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/txts/"
    output_path = os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/csvs/"

    indice = 1
    discarded_files = 0

    for filename in os.listdir(input_path):
      try:
        
        #Reading current txt
        fullpath = os.path.join(input_path, filename)
        f = open(fullpath, "r")
        txt = f.read()

        # Extracting txt sections.
        try:
          string_hurricane_period = (txt.split("Table 1. Best track for ")[1]).split('.')[0]
        except:
          string_hurricane_period = (txt.split("Table 1. Best track data for ")[1]).split('.')[0]

        string_hurricane_period = string_hurricane_period.split('\n')[0]

        try:
          hurricane = re.findall('^(.+?),', string_hurricane_period)[0]
        except:
          hurricane = re.findall('^(.+?)[0-9]', string_hurricane_period)[0]

        period = re.findall('[0-9].*$', string_hurricane_period)[0]

        try:
          string_information = (txt.split("Table 1. Best track for ")[1]).split('Table 2.')[0]
        except:
          string_information = (txt.split("Table 1. Best track data for ")[1]).split('Table 2.')[0]

        information = list(map(clean_1,
                          re.findall('[0-9]+ / [0-9]+ [0-9]+.[0-9]+ [0-9]+.[0-9]+ [0-9]+ [0-9]+ [A-Za-z" ]+', string_information)
                          )
                      )

        if not information:
          information = list(map(clean_2,
                                re.findall('[0-9]+/[0-9]+ [0-9]+.[0-9]+ [0-9]+.[0-9]+ [0-9]+ [0-9]+ [A-Za-z" ]+', string_information)
                              )
                          )

        # Extracting additional information.
        words_re = re.compile("|".join(months))
        current_months = words_re.findall(string_hurricane_period)
        current_year = re.findall('[0-9]{4}', period)

        # Building the dataframe.
        df_raw = pd.DataFrame(information, columns=['string'])
        df_raw = df_raw['string'].str.split(' ', expand=True)
        df_raw.rename(columns={0:'Date',
                              1:'Time',
                              2:'Latitude (°N)',
                              3:'Longitude (°W)',
                              4:'Pressure (mb)',
                              5:'Wind Speed (kt)',
                              6:'filter'}, inplace=True)

        # Removing useless information.
        df_raw = df_raw.loc[:((df_raw.loc[::-1]['filter']=='"')).idxmax()]
        df_raw.rename(columns={'filter':6}, inplace=True)

        # Concatenating fields to generate hurricane category.
        concept_columns = [col for col in df_raw.columns if isinstance(col, int)]
        for i in range(0,len(concept_columns)):
          value = concept_columns[i]
          if i==0:
            stage_description = df_raw[value].astype('str')
          else:
            stage_description = stage_description + ' ' + df_raw[value].fillna('').astype('str')

        df_raw['Stage'] = stage_description
        df_raw.drop(concept_columns, axis=1,inplace=True)

        # Cleaning and sortering category field.
        df_raw['Stage'] = df_raw['Stage'].str.strip()
        df_raw['Stage'] = df_raw.Stage.replace('"', method="ffill")

        # Getting right date and time.
        current_day = df_raw.Date.loc[0]
        start_date = current_day + current_months[0] + current_year[0]

        df_raw['Date'] = df_raw['Date'].astype(int)
        df_raw['days_difference'] =(df_raw.Date - df_raw.Date.shift(1).fillna(current_day).astype(int))
        df_raw.loc[df_raw['days_difference']<0, 'days_difference'] = 1
        df_raw['cumulative'] = df_raw.days_difference.cumsum()
        temp = df_raw['cumulative'].apply(np.ceil).apply(lambda x: pd.Timedelta(x, unit='D'))

        start_date_date = datetime.strptime(start_date, '%d%B%Y')
        df_raw['new_date'] =  start_date_date + temp
        df_raw['new_time'] = pd.to_datetime(df_raw.Time, format='%H%M').dt.time
        df_raw['Date Time (UTC)'] = pd.to_datetime(df_raw["new_date"].astype('str') + df_raw["new_time"].astype('str'), format="%Y-%m-%d%H:%M:%S")

        df_raw.drop(['days_difference','cumulative','new_date','new_time','Date','Time'], axis=1,inplace=True)

        # Adding additional fields.
        df_raw['Hurricane Name'] = hurricane
        df_raw['Sequential Id'] = indice

        # Sorting and adjusting values, we save changes as well.
        df_clean = df_raw[['Sequential Id','Hurricane Name','Date Time (UTC)','Latitude (°N)','Longitude (°W)','Pressure (mb)','Wind Speed (kt)','Stage']]

        df_clean['Latitude (°N)'] = df_clean['Latitude (°N)'].astype('float')
        df_clean['Longitude (°W)'] = df_clean['Longitude (°W)'].astype('float')
        df_clean['Pressure (mb)'] = df_clean['Pressure (mb)'].astype(int)
        df_clean['Wind Speed (kt)'] = df_clean['Wind Speed (kt)'].astype(int)

        csv_file_name = fullpath.replace("txt","csv")
        df_clean.to_csv(csv_file_name, index=False)

        indice = indice + 1
        print('File completed: ',filename,', with progress: ',str(np.round((indice/753)*100,4)),'%')

      except:
        indice = indice + 1
        print('File completed: ',filename,', with progress: ',str(np.round((indice/753)*100,4)),'%')

        discarded_files = discarded_files + 1

    print('Number of discarded files: ',str(discarded_files), 'Percentage: ', str((discarded_files/753*100)))

  
    #Step 5: Appending meteorological information by using meteostat.
    print("Executing step 5...")

    #Concatenating all csvs.
    csv_path = os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/csvs/
    all_elements = os.listdir(csv_path)

    list_of_dfs = []
    for element in all_elements:
        if ".csv" in element:
           list_of_dfs.append(pd.read_csv(path + element))

    df = pd.concat(list_of_dfs)
    df.columns = ["sequential_id","name","timestamp_utc","latitude","longitude","pressure","wind_speed","stage"]
    df = df[["sequential_id","name","timestamp_utc","latitude","longitude","pressure","wind_speed"]

    #Getting meteorological stations available so we can retrieve the closest information possible given both latitude and
    #longitude
    df_stations = pd.read_csv("drive/MyDrive/HackathonCloudera/Model\'sDatasets/stations_locations.csv").set_index('id')
    #print(type(df_stations))
    df_stations_dict = df_stations.to_dict("index")
    #print(df_stations_dict)

    
    
  
    print("Process completed.")

#---------------------------------------------------------
###################### Main section ######################
#---------------------------------------------------------
  
if __name__ == "__main__":

    #If the option is whether explicit or it doesn't exist, we use the prebuilt model.
    if os.environ["ETL_OPERATIONS"] == "no" or os.environ["ETL_OPERATIONS"] is None:
        print("Using default dataset")
         
    else:
        clean_and_transform_data()
      

