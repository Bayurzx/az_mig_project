import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL = os.environ.get('POSTGRES_URL')  #TODO: Update value
    POSTGRES_USER = os.environ.get('POSTGRES_URL') #TODO: Update value
    POSTGRES_PWL = os.environ.get('POSTGRES_PWL') or "xxxxxxxxxxxxx." # or '<POSTGRES_PWL_STRING>'  #TODO: Update value
    POSTGRES_DBL = "techconfdb"  #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PWL,url=POSTGRES_URL,db=POSTGRES_DBL)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4txxxxxxxx'
    SERVICE_BUS_CONNECTION_STRING =os.environ.get('POSTGRES_URL') or 'Endpoint=sb://notificationqueue.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=PttkwZfk+xxxxxxxxxxxxxxxxxxx=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS = 'bayurzx@gmail.com'
    SENDGRIDFAKE_API_KEY = os.environ.get('POSTGRES_URL') or 'SGF.xxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False