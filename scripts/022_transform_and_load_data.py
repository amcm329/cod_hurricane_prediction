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
import time
import wget
import PyPDF2 
import meteostat
import pdfplumber
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


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


# Starting time---- 6:40 pm
def clean_1(x):
  return x.replace('/ ', '')

def clean_2(x):
  return x.replace('/', ' ')


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
        filename = wget.download(complete_url, out= os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/pdfs")

   
    #Step 3: Extracting quantitative information from pdfs.  
    print("Executing step 3...")
    for filename in os.listdir(os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/pdfs/"):
        fullpath = os.path.join(os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/pdfs/", filename)
        txt_file_name = fullpath.replace("pdf","txt")
        text_file = open(txt_file_name, 'wt')
        text = convert2text(fullpath)
        text_file.write(text)
        text_file.close()

    print('Last file: ', filename)

    #Step 4: 
    print("Executing step 4...")

    #Variable created to gather monthly information.
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    input_path = os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/txts/"
    output_path = os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/csvs/"

    indice = 1
    archivos_descartados = 0

    for filename in os.listdir(input_path):
      try:
        
        #Lectura del txt
        fullpath = os.path.join(input_path, filename)
        f = open(fullpath, "r")
        txt = f.read()

        # Extraemos partes del txt
        try:
          string_huracan_periodo = (txt.split("Table 1. Best track for ")[1]).split('.')[0]
        except:
          string_huracan_periodo = (txt.split("Table 1. Best track data for ")[1]).split('.')[0]

        string_huracan_periodo = string_huracan_periodo.split('\n')[0]

        try:
          huracan = re.findall('^(.+?),', string_huracan_periodo)[0]
        except:
          huracan = re.findall('^(.+?)[0-9]', string_huracan_periodo)[0]

        periodo = re.findall('[0-9].*$', string_huracan_periodo)[0]

        try:
          string_informacion = (txt.split("Table 1. Best track for ")[1]).split('Table 2.')[0]
        except:
          string_informacion = (txt.split("Table 1. Best track data for ")[1]).split('Table 2.')[0]

        informacion = list(map(clean_1,
                          re.findall('[0-9]+ / [0-9]+ [0-9]+.[0-9]+ [0-9]+.[0-9]+ [0-9]+ [0-9]+ [A-Za-z" ]+', string_informacion)
                          )
                      )

        if not informacion:
          informacion = list(map(clean_2,
                                re.findall('[0-9]+/[0-9]+ [0-9]+.[0-9]+ [0-9]+.[0-9]+ [0-9]+ [0-9]+ [A-Za-z" ]+', string_informacion)
                              )
                          )

        # Extraemos informacion adicional
        words_re = re.compile("|".join(months))
        meses = words_re.findall(string_huracan_periodo)
        año = re.findall('[0-9]{4}', periodo)

        # Construimos el dataframe
        df_raw = pd.DataFrame(informacion, columns=['string'])
        df_raw = df_raw['string'].str.split(' ', expand=True)
        df_raw.rename(columns={0:'Date',
                              1:'Time',
                              2:'Latitude (°N)',
                              3:'Longitude (°W)',
                              4:'Pressure (mb)',
                              5:'Wind Speed (kt)',
                              6:'filter'}, inplace=True)

        # Quitamos informacion innecesaria
        df_raw = df_raw.loc[:((df_raw.loc[::-1]['filter']=='"')).idxmax()]
        df_raw.rename(columns={'filter':6}, inplace=True)


        # Concatenamos los campos para generar la categoria del huracan
        concept_columns = [col for col in df_raw.columns if isinstance(col, int)]
        for i in range(0,len(concept_columns)):
          value = concept_columns[i]
          if i==0:
            stage_description = df_raw[value].astype('str')
          else:
            stage_description = stage_description + ' ' + df_raw[value].fillna('').astype('str')

        df_raw['Stage'] = stage_description
        df_raw.drop(concept_columns, axis=1,inplace=True)

        #limpiamos el campo de la categoria para dejarlo en orden
        df_raw['Stage'] = df_raw['Stage'].str.strip()
        df_raw['Stage'] = df_raw.Stage.replace('"', method="ffill")


        # Obtenemos la fecha correcta y su tiempo
        dia = df_raw.Date.loc[0]
        fh_inicio = dia + meses[0] + año[0]

        df_raw['Date'] = df_raw['Date'].astype(int)
        df_raw['days_difference'] =(df_raw.Date - df_raw.Date.shift(1).fillna(dia).astype(int))
        df_raw.loc[df_raw['days_difference']<0, 'days_difference'] = 1
        df_raw['cumulative'] = df_raw.days_difference.cumsum()
        temp = df_raw['cumulative'].apply(np.ceil).apply(lambda x: pd.Timedelta(x, unit='D'))

        fh_inicio_date = datetime.strptime(fh_inicio, '%d%B%Y')
        df_raw['new_date'] =  fh_inicio_date + temp
        df_raw['new_time'] = pd.to_datetime(df_raw.Time, format='%H%M').dt.time
        df_raw['Date Time (UTC)'] = pd.to_datetime(df_raw["new_date"].astype('str') + df_raw["new_time"].astype('str'), format="%Y-%m-%d%H:%M:%S")

        df_raw.drop(['days_difference','cumulative','new_date','new_time','Date','Time'], axis=1,inplace=True)

        #Añadimos campos adicionales
        df_raw['Hurricane Name'] = huracan
        df_raw['Sequential Id'] = indice

        # Ordenamos, ajustamos valores en su formato y guardamos
        df_clean = df_raw[['Sequential Id','Hurricane Name','Date Time (UTC)','Latitude (°N)','Longitude (°W)','Pressure (mb)','Wind Speed (kt)','Stage']]

        df_clean['Latitude (°N)'] = df_clean['Latitude (°N)'].astype('float')
        df_clean['Longitude (°W)'] = df_clean['Longitude (°W)'].astype('float')
        df_clean['Pressure (mb)'] = df_clean['Pressure (mb)'].astype(int)
        df_clean['Wind Speed (kt)'] = df_clean['Wind Speed (kt)'].astype(int)

        csv_file_name = fullpath[:57]+'allcsvs/' + fullpath[65:-4]+'.csv'
        df_clean.to_csv(csv_file_name, index=False)

        indice = indice + 1
        print('Termino con el archivo: ',filename,', lleva de progreso un: ',str(np.round((indice/753)*100,4)),'%')

      except:
        indice = indice + 1
        print('Termino con el archivo: ',filename,', lleva de progreso un: ',str(np.round((indice/753)*100,4)),'%')

        archivos_descartados = archivos_descartados + 1

    print('Numero de archivos descartados: ',str(archivos_descartados), 'Porcebtaje: ', str((archivos_descartados/753*100)))



  
    #Step 5: 
    print("Executing step 5...")
    
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
      

