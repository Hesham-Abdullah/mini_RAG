from enum import Enum


class ResponseSignal(Enum):

    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_VALIDATED_SUCCESS= "file_validated_successfully"
    FILE_UPLAOD_SUCCESS = "file_uploaded_successfully"
    FILE_UPLOAD_FAILED = "file_uplaod_failed"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESS= "processing_success"