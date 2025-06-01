#/usr/bon/env python3

import magic
import streamlit as st

DATA_MIME_MAP = {
    "csv" : "text/plain",
    "txt" : "text/plain",
 #   "xls" : "application/vnd.ms-excel", 
    "xlsx" : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
    "parquet" : "application/vnd.apache.parquet"
}

PDF_MIME_MAP = {
    "pdf" : "application/pdf"
}

MIME_MAP = DATA_MIME_MAP | PDF_MIME_MAP


def upload(file_exts=list(DATA_MIME_MAP.keys()), key=0):

    file = st.file_uploader(       # file is BytesIO
        "Upload", 
        type=file_exts, 
        accept_multiple_files=False, 
        label_visibility="collapsed",
        key=f"file_upload_{key}"
    )
    
    if file is None:
        return None, None
    else:
        return process_upload(file_exts, file)



@st.cache_data
def process_upload(file_exts, file):
    file_name = file.name
    file_ext = file.name.split(".")[-1]
    mime = magic.Magic(mime=True)
    mime_type =  mime.from_buffer(file.getvalue())
    
    expected_types = [MIME_MAP[key] for key in file_exts]

    # openpyxl generated Excel files are recognized as zip files by some servers
    if file_ext in ["xls", "xlsx"]: 
        expected_types.append("application/zip")

    if mime_type in expected_types:
        return file, file_name
    else:
        print(f"File name is {file_name}")
        print(f"MIME type is {mime_type}")
        raise Exception(f"The file is of an unsupported MIME type: {mime_type}.")