
# Install the requirements located in the file requirements.txt

!pip install --upgrade pip
!pip install --no-cache-dir --progress-bar off -r requirements.txt

try:
     import cml.data_v1 as cmldata
     SPARK_CONNECTION_NAME = os.getenv("SPARK_CONNECTION_NAME")
     conn = cmldata.get_connection(SPARK_CONNECTION_NAME)
    except: 
