from fastapi import FastAPI, APIRouter, Depends, UploadFile 
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(r"C:\Users\hesha\Downloads\Projects\Mini_RAG\mini_rag\helpers"), '..')))
from helpers.config import get_settings, Settings

data_router= APIRouter(
    prefix= "/api/v1/data",
    tags=["mini_rag", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    pass
