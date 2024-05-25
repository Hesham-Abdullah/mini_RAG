from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import os

class Doccontroller(BaseController):
    def __init__(self):
        super().__init__()

    def get_doc_path(self, id: str):
        doc_dir= os.path.join(self.docs_dir, id)

        if not os.path.exists(doc_dir): 
            os.makedirs(doc_dir)

        return doc_dir
    
