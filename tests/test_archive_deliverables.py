import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVER = ROOT / "tools" / "archive_deliverables.py"


class ArchiveDeliverablesTests(unittest.TestCase):
    def test_archives_files_and_writes_matching_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            archive = root / "archive"
            manifest_copy = root / "manifest-copy.tsv"
            (source / "deliverables").mkdir(parents=True)
            (source / "video").mkdir()
            (source / "deliverables" / "a.bin").write_bytes(b"alpha")
            (source / "video" / "b.mp4").write_bytes(b"beta")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ARCHIVER),
                    "--source-root",
                    str(source),
                    "--archive-root",
                    str(archive),
                    "--path",
                    "deliverables",
                    "--path",
                    "video",
                    "--manifest-copy",
                    str(manifest_copy),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                (archive / "deliverables" / "a.bin").read_bytes(), b"alpha"
            )
            self.assertEqual((archive / "video" / "b.mp4").read_bytes(), b"beta")
            self.assertEqual(
                (archive / "manifest.tsv").read_bytes(), manifest_copy.read_bytes()
            )
            rows = (archive / "manifest.tsv").read_text(encoding="utf-8").splitlines()
            self.assertEqual(rows[0], "sha256\tbytes\tpath")
            self.assertEqual(
                [row.rsplit("\t", 1)[1] for row in rows[1:]],
                ["deliverables/a.bin", "video/b.mp4"],
            )

    def test_refuses_non_empty_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            archive = root / "archive"
            (source / "deliverables").mkdir(parents=True)
            (source / "deliverables" / "a.bin").write_bytes(b"alpha")
            archive.mkdir()
            keep = archive / "keep.txt"
            keep.write_text("preserve", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(ARCHIVER),
                    "--source-root",
                    str(source),
                    "--archive-root",
                    str(archive),
                    "--path",
                    "deliverables",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(keep.read_text(encoding="utf-8"), "preserve")


if __name__ == "__main__":
    unittest.main()
