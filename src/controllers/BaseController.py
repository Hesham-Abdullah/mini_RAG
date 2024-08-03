from helper.config import Settings, get_settings
import os
class BaseController():
    def __init__(self):
        self.app_settings= get_settings()
        self.base_dir= os.path.dirname(os.path.dirname(__file__))
        self.docs_dir= os.path.join(self.base_dir, "assets/Docs") 
