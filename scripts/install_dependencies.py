
# Install the requirements
!pip install --upgrade pip
!pip install --no-cache-dir --progress-bar off -r requirements.txt

#import os

# Install cmlapi package
#try:
#    import cmlapi
#except ModuleNotFoundError:
#    import os
#    cluster = os.getenv("CDSW_API_URL")[:-1]+"2"
#    !pip3 install {cluster}/python.tar.gz
#    import cmlapi
