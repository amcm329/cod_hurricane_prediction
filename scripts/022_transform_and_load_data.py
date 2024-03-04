"""
  The following code performs these operations: 
  1.- Calls 021_download_data.py to get the URLs of pdfs related to hurricanes.
  2.- Dumps information from the pdfs and saves it as txts
  3.- Checks each one of the txts and extracts only quantitative information 
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
  
import wget
import meteostat
import pandas as pd

def clean_and_transform_data():
  
    !scrapy runspider scraper.py

    handler = open()

    filename = wget.download(complete_url, out=splitted_element)


if __name__ == "__main__":

    #If the option is whether explicit or it doesn't exist, we use the prebuilt model.
    if os.environ["ETL_OPERATIONS"] == "yes" or os.environ["ETL_OPERATIONS"] is None:
        print("Using default dataset")
         
    else:
        clean_and_transform_data()
      

