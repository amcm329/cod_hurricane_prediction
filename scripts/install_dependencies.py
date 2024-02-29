
# Install the requirements

!pip install --upgrade pip
!pip install --no-cache-dir --log --progress-bar off scripts/pip-req.log -r requirements.txt

import os
import json
import requests

# Install cmlapi package
try:
    import cmlapi
except ModuleNotFoundError:
    import os
    cluster = os.getenv("CDSW_API_URL")[:-1]+"2"
    !pip3 install {cluster}/python.tar.gz
    import cmlapi 
  
from cmlapi.rest import ApiException
