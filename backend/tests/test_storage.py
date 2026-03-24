"""Tests for attachment storage utilities."""
from app.utils.storage import is_allowed_extension, is_within_size_limit


class TestAllowedExtensions:
    def test_allowed_image(self):
        assert is_allowed_extension("photo.png") is True
        assert is_allowed_extension("photo.jpg") is True
        assert is_allowed_extension("photo.gif") is True

    def test_allowed_document(self):
        assert is_allowed_extension("report.pdf") is True
        assert is_allowed_extension("data.csv") is True
        assert is_allowed_extension("notes.txt") is True
        assert is_allowed_extension("doc.docx") is True

    def test_allowed_archive(self):
        assert is_allowed_extension("files.zip") is True

    def test_allowed_log(self):
        assert is_allowed_extension("server.log") is True

    def test_disallowed_executable(self):
        assert is_allowed_extension("virus.exe") is False
        assert is_allowed_extension("script.sh") is False
        assert is_allowed_extension("code.py") is False

    def test_case_insensitive(self):
        assert is_allowed_extension("PHOTO.PNG") is True
        assert is_allowed_extension("Report.PDF") is True


class TestSizeLimit:
    def test_within_limit(self):
        assert is_within_size_limit(1024) is True  # 1 KB
        assert is_within_size_limit(5 * 1024 * 1024) is True  # 5 MB

    def test_at_limit(self):
        assert is_within_size_limit(10 * 1024 * 1024) is True  # exactly 10 MB

    def test_over_limit(self):
        assert is_within_size_limit(10 * 1024 * 1024 + 1) is False
        assert is_within_size_limit(20 * 1024 * 1024) is False
