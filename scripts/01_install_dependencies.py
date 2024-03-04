# Install the requirements located in the file requirements.txt
!pip install --upgrade pip
!pip install --no-cache-dir --progress-bar off -r requirements.txt

#Section for environment variables: 
import os

full_path = os.getenv("OPERATING_SYSTEM_PATH")
     
if full_path is None: 
   #Element doesn't exist.
   os.environ["OPERATING_SYSTEM_PATH"] = "/home/cdsw/"
