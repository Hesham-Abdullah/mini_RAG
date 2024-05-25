from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os 
import aiofiles
from models import ResponseSignal
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(r"C:\Users\hesha\Downloads\Projects\Mini_RAG\mini_rag\helpers"), '..')))
from helper.config import get_settings, Settings
from controllers import DataController, Doccontroller
import logging

logger= logging.getLogger("uvicorn.error")

data_router= APIRouter(
    prefix= "/api/v1/data",
    tags=["mini_rag", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
        
    data_controller= DataController()

    is_valid, signal= data_controller.validate_uploaded_file(file)

    if not is_valid:
        return JSONResponse(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            content =  {
                                "signal" : signal     
                                              }
                        )
                    
    doc_dir= Doccontroller().get_doc_path(id= project_id)
    file_path= data_controller.gen_unique_file_name(org_fname= file.filename, doc_id=project_id)
    try:

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        
        logger.error(f"error while uploading file: {e}")
        return JSONResponse(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            content =  {
                                "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value       
                                          }
                        )       

    return JSONResponse(
                        content= {
                            "signal": ResponseSignal.FILE_UPLAOD_SUCCESS.value
                        }
    )