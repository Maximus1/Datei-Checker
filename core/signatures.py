SIGNATURES = [
    # Image Formats
    {"ext": ".jpg", "sig": bytes([0xFF, 0xD8, 0xFF]), "offset": 0, "name": "JPEG Image"},
    {"ext": ".png", "sig": bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]), "offset": 0, "name": "PNG Image"},
    {"ext": ".gif", "sig": b"GIF8", "offset": 0, "name": "GIF Image"},
    {"ext": ".bmp", "sig": b"BM", "offset": 0, "name": "Bitmap Image"},
    {"ext": ".webp", "sig": b"RIFF", "offset": 0, "name": "WebP Image"}, # Needs sub-check for WEBP

    # Documents
    {"ext": ".pdf", "sig": b"%PDF-", "offset": 0, "name": "PDF Document"},
    {"ext": ".doc", "sig": bytes([0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1]), "offset": 0, "name": "Legacy MS Office"},
    {"ext": ".docx", "sig": b"PK\x03\x04", "offset": 0, "name": "Office Open XML / ZIP"}, # ZIP based

    # Archives
    {"ext": ".zip", "sig": b"PK\x03\x04", "offset": 0, "name": "ZIP Archive"},
    {"ext": ".rar", "sig": b"Rar!", "offset": 0, "name": "RAR Archive"},
    {"ext": ".7z", "sig": b"7z\xBC\xAF\x27\x1C", "offset": 0, "name": "7-Zip Archive"},
    {"ext": ".tar.gz", "sig": bytes([0x1F, 0x8B]), "offset": 0, "name": "Gzip Archive"},

    # Media
    {"ext": ".mp3", "sig": b"ID3", "offset": 0, "name": "MP3 Audio"},
    {"ext": ".mp4", "sig": b"ftyp", "offset": 4, "name": "MP4 Video"},
    {"ext": ".mkv", "sig": bytes([0x1A, 0x45, 0xDF, 0xA3]), "offset": 0, "name": "Matroska Video"},
    {"ext": ".wav", "sig": b"RIFF", "offset": 0, "name": "WAV Audio"},

    # Database / Executable
    {"ext": ".sqlite", "sig": b"SQLite format 3\x00", "offset": 0, "name": "SQLite Database"},
    {"ext": ".exe", "sig": b"MZ", "offset": 0, "name": "Windows Executable"},
]
