import os
import tempfile
import unittest

from modules.file_organizer import organize_directory, find_duplicates


class TestFileOrganizer(unittest.TestCase):
    def test_file_org_and_dups(self):
        with tempfile.TemporaryDirectory() as td:
            # create dummy files
            for name, content in [
                ("a.txt", b"hello"),
                ("b.txt", b"hello"),
                ("c.jpg", b"\xff\xd8\xff"),
            ]:
                p = os.path.join(td, name)
                with open(p, 'wb') as f:
                    f.write(content)

            logs = organize_directory(td)
            self.assertTrue(any("Moved" in l for l in logs))

            dups = find_duplicates(td)
            has_dup = any(len(paths) >= 2 for _, paths in dups)
            self.assertTrue(has_dup)


if __name__ == '__main__':
    unittest.main()
