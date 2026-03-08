import os
import shutil
import unittest
from core.detector import detect_file_type
from core.renamer import safe_rename
from core.processor import process_single_file

class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_files"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_magic_detection_jpeg(self):
        file_path = os.path.join(self.test_dir, "test1")
        with open(file_path, "wb") as f:
            f.write(bytes([0xFF, 0xD8, 0xFF, 0xDB])) # JPEG Magic
        
        ext, type_name = detect_file_type(file_path)
        self.assertEqual(ext, ".jpg")

    def test_magic_detection_pdf(self):
        file_path = os.path.join(self.test_dir, "test2")
        with open(file_path, "wb") as f:
            f.write(b"%PDF-1.4 test")
        
        ext, type_name = detect_file_type(file_path)
        self.assertEqual(ext, ".pdf")

    def test_safe_rename_no_conflict(self):
        file_path = os.path.join(self.test_dir, "test3")
        with open(file_path, "w") as f: f.write("test")
        
        success, msg, final_path = safe_rename(file_path, "renamed.txt", dry_run=False)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "renamed.txt")))

    def test_safe_rename_conflict(self):
        file_path = os.path.join(self.test_dir, "test4")
        with open(file_path, "w") as f: f.write("test")
        
        # Create existing file
        with open(os.path.join(self.test_dir, "renamed.txt"), "w") as f: f.write("exist")
        
        success, msg, final_path = safe_rename(file_path, "renamed.txt", dry_run=False)
        self.assertTrue(success)
        self.assertTrue(os.path.basename(final_path), "renamed (1).txt")

if __name__ == "__main__":
    unittest.main()
