import io
from PyPDF2 import PdfReader
from fastapi import HTTPException, status

def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        print("in pdf")
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        if not text.strip():
            raise ValueError("No text found in PDF")
        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"PDF processing failed: {str(e)}"
        )