from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os 
import aiofiles
from models import ResponseSignal
from helper.config import get_settings, Settings
from controllers import DataController, Doccontroller, ProcessController
from .schemes.data import ProcessRequest
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
    file_path, file_id= data_controller.gen_unique_file_name(org_fname= file.filename, doc_id=project_id)
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
                            "signal": ResponseSignal.FILE_UPLAOD_SUCCESS.value, 
                            "file_id": file_id
                        }
    )

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):

    file_id      = process_request.file_id
    chunk_size   = process_request.chunk_size
    overlap_size = process_request.overlap_size
    process_controller= ProcessController(project_id=project_id)
    content = process_controller.get_file_content(file_id= file_id)
    
    chunks= process_controller.process_file_content(file_content=content,
                                                    chunk_size= chunk_size,
                                                     overlap_size= overlap_size
                                                        )
    
    if chunks is None or len(chunks) == 0:
        return JSONResponse(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            content =  {
                                "signal" : ResponseSignal.PROCESSING_FAILED.value       
                                          }
                        )     

    return chunks