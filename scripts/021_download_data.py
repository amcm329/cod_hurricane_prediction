"""
The following document retrieves all the information from the NOAA site.
The documents that will be extracted are only pdfs regarding hurricanes, more accurately, 
their geographical and meteorological characteristics.
"""
#Section for environment variables: 
import os

full_path = os.getenv("OPERATING_SYSTEM_PATH")
     
if full_path is None: 
   #Element doesn't exist.
   os.environ["OPERATING_SYSTEM_PATH"] = "/home/cdsw/"

#How to execute it (this will be done in another code).
#scrapy runspider scraper.py

#Error with Scrapy
#https://stackoverflow.com/questions/76995567/error-when-crawl-data-epollreactor-object-has-no-attribute-handlesignals

import re
import wget
import scrapy

class QuoteSpider(scrapy.Spider):
      name = "spider-pdf"
      #Here will be stored all the LINKS to the pfds.
      aux_urls = []
      initial_year = 2023#2002
      count = 0
      #It's year + 1
      final_year = 2024

      #We are getting only the urls of etl files
      for x in range(initial_year,final_year):

          if count < 1:   
              #Adding only available regions (Atlantic, Pacific, Central):
              for z in ["atl","epac","cpac"]:

                  #Looping throughout the mentioned years.
                  current_url = "https://www.nhc.noaa.gov/data/tcr/index.php?season={0}&basin={1}".format(x,z)
                  aux_urls.append(current_url)

          else: 
               break

          count += 1 
           
      start_urls = aux_urls
      #print(start_urls)


    """
       Function that extracts from a html document the URLS contanining "PDF" references.
    """
    def parse(self, response):

        #A file of urls will be created so we can then extract them. 
        final_links = []
        HDR_SELECTOR = '.hdr'
        base_url = "https://www.nhc.noaa.gov/data/tcr/"
        
        #Pattern to recognize only pdfs. 
        pattern = re.compile("^[A-Za-z0-9]+_[A-Za-z0-9]+.pdf$")

        #Opening the file of urls.
        handler = open(os.getenv("OPERATING_SYSTEM_PATH") + "src/auxiliary/url_links.txt","a")
    
        for hdr in response.css(HDR_SELECTOR):
            #Extracting links.
            current_links = hdr.xpath('a/@href').extract()
            #print(hdr.xpath('a/@href').extract())  
            #print(hdr.css(AHREF_SELECTOR).extract_first()) 
            
            for element in current_links: 

                splitted_element = element.split("/")[-1]
                #print(splitted_element)

                #Adding only pdfs to the list of urls. 
                if not(pattern.match(splitted_element) is None):     
                   complete_url = base_url + splitted_element                
                   final_links.append(complete_url)
                   
                   handler.write(complete_url + "\n")
                   
                   #print(complete_url)
                   #filename = wget.download(complete_url, out=splitted_element)
         
        handler.close()         
        #print(final_links)         
            

