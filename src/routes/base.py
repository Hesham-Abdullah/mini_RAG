# base.py 
from fastapi import FastAPI, APIRouter, Depends
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(r"C:\Users\hesha\Downloads\Projects\Mini_RAG\mini_rag\helpers"), '..')))
from helper.config import get_settings, Settings

base_router= APIRouter(
    prefix="/api/v1",
    tags =["mini_rag"]
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):

    app_name= app_settings.APP_NAME
    app_version= app_settings.APP_VERSION

    return {
        "app_name": app_name,
        "app_version": app_version
    }