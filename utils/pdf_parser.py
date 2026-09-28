import pymupdf


def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded PDF file.

    Parameters:
        pdf_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text
    """

    try:
        document = pymupdf.open(
            stream=pdf_file.read(),
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()

    except Exception as e:
        raise Exception(f"Error extracting PDF text: {e}")