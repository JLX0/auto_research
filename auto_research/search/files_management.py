import fitz


def sanitize_filename(filename):
    # Remove illegal characters for Windows filenames
    illegal_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in illegal_chars:
        filename = filename.replace(char, '')
    return filename.strip()

def is_pdf_corrupted(file_path):
    try:
        doc = fitz.open(file_path)
        doc.close()
        return True
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return False