import io


def extract_text_from_file(uploaded_file):
    filename = (uploaded_file.filename or "").lower()
    if not filename:
        raise ValueError("Uploaded file has no filename.")

    file_bytes = uploaded_file.read()
    if not file_bytes:
        raise ValueError("Uploaded file is empty.")

    if filename.endswith((".png", ".jpg", ".jpeg")):
        return extract_from_image(file_bytes)

    if filename.endswith(".pdf"):
        return extract_from_pdf(file_bytes)

    raise ValueError(
        "Unsupported file type. Please upload PDF, PNG, JPG or JPEG."
    )


def extract_from_image(file_bytes):
    try:
        from PIL import Image
        import pytesseract
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except ImportError:
        raise ValueError("Image OCR dependencies are not installed.")
    except Exception as error:
        raise ValueError(f"Unable to read image: {error}")


def extract_from_pdf(file_bytes):
    try:
        import fitz
    except ImportError:
        raise ValueError("PyMuPDF is not installed.")

    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")

        pages_text = []
        for page in document:
            page_text = page.get_text("text")
            if page_text.strip():
                pages_text.append(page_text)
        text = "\n".join(pages_text).strip()

        if text:
            document.close()
            return text

        ocr_text = []
        for page in document:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            image_bytes = pixmap.tobytes("png")
            try:
                page_text = extract_from_image(image_bytes)
                if page_text:
                    ocr_text.append(page_text)
            except Exception:
                continue
        document.close()

        final_text = "\n".join(ocr_text).strip()
        if not final_text:
            raise ValueError("Could not extract readable text from PDF.")
        return final_text
    except ValueError:
        raise
    except Exception as error:
        raise ValueError(f"Unable to process PDF: {error}")
