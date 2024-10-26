from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os 
import aiofiles
from models import ResponseSignal
from helper.config import get_settings, Settings
from controllers import DataController, Doccontroller, ProcessController
from .schemes.data import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk
import logging



logger= logging.getLogger("uvicorn.error")

data_router= APIRouter(
    prefix= "/api/v1/data",
    tags=["mini_rag", "data"]
)

@data_router.post("/upload/{project_id}")
async def upload_data(request : Request ,project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    project_model= ProjectModel( db_client= request.app.db_client)

    project= await project_model.get_project_or_create_one(project_id=project_id)    
    
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
async def process_endpoint(request : Request, project_id: str, process_request: ProcessRequest):

    file_id      = process_request.file_id
    chunk_size   = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset     = process_request.do_reset  
    process_controller= ProcessController(project_id=project_id)
    content = process_controller.get_file_content(file_id= file_id)

    project_model= ProjectModel( db_client= request.app.db_client)

    project= await project_model.get_project_or_create_one(project_id=project_id)    
    
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
    chunk_model= ChunkModel(db_client= request.app.db_client)

    chunks_records= [
        DataChunk(
                chunk_text= chunk.page_content,
                chunk_metadata= chunk.metadata,
                chunk_order= i+1,
                chunk_project_id= project.id)

        for i, chunk in enumerate(chunks)
    ]

    if do_reset==1:
        _= await chunk_model.delete_chunks_by_project_id(project_id= project.id)


    no_records= await chunk_model.insert_many_chunks(chunks=chunks_records)
    return JSONResponse(
        content={
            "signal" : ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )

    