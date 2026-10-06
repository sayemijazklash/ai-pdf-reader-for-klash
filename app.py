# import os
# import tempfile

# from fastapi import FastAPI, UploadFile, File, Form, HTTPException

# from processor import process_pdf


# app = FastAPI(
#     title="PDF Extraction API",
#     version="1.0.0"
# )


# @app.get("/health")
# def health():
#     return {"status": "healthy"}


# @app.post("/api/v1/process")
# async def process_document(
#     file: UploadFile = File(...),
#     job_id: str = Form(...),
#     document_id: str = Form(None),
#     template_id: str = Form(None)
# ):

#     if not file.filename.lower().endswith(".pdf"):
#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF files are supported"
#         )

#     temp_path = None

#     try:

#         content = await file.read()

#         if not content:
#             raise HTTPException(
#                 status_code=400,
#                 detail="Empty PDF"
#             )

#         with tempfile.NamedTemporaryFile(
#             delete=False,
#             suffix=".pdf"
#         ) as f:

#             f.write(content)
#             temp_path = f.name

#         result = process_pdf(
#             temp_path,
#             original_filename=file.filename
#         )

#         return {
#             "success": True,
#             "job_id": job_id,
#             "document_id": document_id,
#             "template_id": template_id,
#             "data": result
#         }

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

#     finally:

#         if temp_path and os.path.exists(temp_path):
#             os.remove(temp_path)


import os
import tempfile

from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from processor import process_pdf


app = FastAPI(
    title="Enterprise PDF Extraction API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "PDF Extraction API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/v1/process")
async def process_document(
    file: UploadFile = File(...),
    job_id: str = Form(...),
    document_id: str = Form(None),
    template_id: str = Form(None)
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    temp_path = None

    try:

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="PDF is empty"
            )

        # Temporary PDF
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(content)
            temp_path = temp_file.name

        # Process PDF
        result = process_pdf(
            temp_path,
            original_filename=file.filename
        )

        return {
            "success": True,

            "job_id": job_id,

            "document_id": document_id,

            "template_id": template_id,

            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
