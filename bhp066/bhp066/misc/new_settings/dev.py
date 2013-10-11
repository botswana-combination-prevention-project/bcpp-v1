from .common import *
from .email_settings import *


DEBUG = True

TEMPLATE_DEBUG = DEBUG

#KEY_PATH = PROJECT_DIR.child('keys')
KEY_PATH = os.path.join(PROJECT_DIR, 'keys')
