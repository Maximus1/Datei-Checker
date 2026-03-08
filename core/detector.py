from .signatures import SIGNATURES

def detect_file_type(file_path):
    """Detect file extension by checking magic bytes."""
    try:
        # Read max 512 bytes for signature detection
        with open(file_path, "rb") as f:
            header = f.read(512)

        if not header:
            return None, "Empty File"

        for sig_info in SIGNATURES:
            sig = sig_info["sig"]
            offset = sig_info["offset"]
            if header[offset:offset+len(sig)] == sig:
                # Handle common multi-type headers like PK (ZIP, DOCX, etc)
                if sig == b"PK\x03\x04":
                    if b"word/" in header: return ".docx", "Word Document"
                    if b"xl/" in header: return ".xlsx", "Excel Spreadsheet"
                    if b"ppt/" in header: return ".pptx", "PowerPoint Presentation"
                    return ".zip", "ZIP Archive"

                # Handle RIFF (WAV, WEBP)
                if sig == b"RIFF":
                    if header[8:12] == b"WEBP": return ".webp", "WebP Image"
                    if header[8:12] == b"WAVE": return ".wav", "WAV Audio"
                    return ".riff", "RIFF File"

                return sig_info["ext"], sig_info["name"]

        return None, "Unknown Type"
    except OSError as e:
        return None, f"Error: {str(e)}"
