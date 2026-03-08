import zipfile

def extract_metadata_name(file_path, extension):
    """
    Attempts to extract original filename from file metadata.
    """
    if extension == ".zip":
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                # Often people zip a single folder/file, check first item
                names = zf.namelist()
                if names:
                    # Return first part of path if it's a folder, or the filename
                    first = names[0].split('/')[0]
                    if first: return first
        except (zipfile.BadZipFile, OSError):
            pass

    # Placeholder for more complex metadata (EXIF/PDF) if libraries are available
    # For now, return None to fallback to standard naming
    return None
