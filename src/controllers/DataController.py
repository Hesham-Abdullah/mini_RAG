from .BaseController import BaseController
from .DocController import Doccontroller
from fastapi import UploadFile
from models import ResponseSignal
import random, string, re, os



class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.size_scale= 1048576 # convert MB to B
    

    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
        
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_UPLAOD_SUCCESS.value
    
    
    def gen_rand_keys(self, length: int = 4):
        return "".join(random.choices(string.digits, k=length))
    

    def get_clean_fname(self, org_fname: str):
        cleaned_fname= re.sub(r"[^\w.]", "", org_fname.strip())
        cleaned_fname= cleaned_fname.replace(" ", "_")
        return cleaned_fname
    
    def gen_unique_file_name(self, org_fname: str, doc_id: str):

        rand_id = self.gen_rand_keys()
        doc_path = Doccontroller().get_doc_path(id= doc_id)
        cleaned_fname= self.get_clean_fname(org_fname= org_fname)

        new_file_name= os.path.join(
            doc_path, 
            rand_id + "_" + cleaned_fname
        )
        while os.path.exists(new_file_name):
            rand_id= self.gen_rand_keys()
            new_file_name= os.path.join(
                doc_path, 
                rand_id + "_" + cleaned_fname
            )
        return new_file_name
        