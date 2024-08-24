from .BaseController import BaseController
from .DocController import Doccontroller
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import processingEnum



class ProcessController(BaseController):

    def __init__(self,project_id: str):
        super().__init__()
        self.project_id= project_id
        self.project_path= Doccontroller().get_doc_path(id= self.project_id)
    

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]
    
    
    def get_file_loader(self, file_id: str):
        
        file_path= os.path.join(self.project_path, file_id)
        file_ext= self.get_file_extension(file_id=file_id)

        if file_ext == processingEnum.TXT.value:
            return TextLoader(file_path, encoding= "utf-8")
        
        if file_ext == processingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        return None
    
    def get_file_content(self, file_id: str):
        
        loader= self.get_file_loader(file_id= file_id)

        return loader.load()
    

    def process_file_content(self,file_content: list, chunk_size: int=100, overlap_size: int= 20):

        text_splitter= RecursiveCharacterTextSplitter(
            chunk_size= chunk_size,
            chunk_overlap= overlap_size,
            length_function= len
        )

        text_content= [
            rec.page_content
            for rec in file_content
        ]

        text_meta= [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            text_content,
            metadatas=text_meta
        )
        return chunks