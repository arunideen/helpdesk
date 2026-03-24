"""Tests for email format parsing and validation."""
import pytest
from app.email.parser import (
    parse_subject,
    parse_body,
    parse_email_content,
    ParsedAttachment,
)
from app.models.ticket import TicketCategory, TicketPriority


class TestParseSubject:
    def test_valid_subject(self):
        category, summary, errors = parse_subject("[Bug] Login page crashes on submit")
        assert category == TicketCategory.BUG
        assert summary == "Login page crashes on submit"
        assert errors == []

    def test_valid_subject_feature(self):
        category, summary, errors = parse_subject("[Feature] Add dark mode")
        assert category == TicketCategory.FEATURE
        assert summary == "Add dark mode"
        assert errors == []

    def test_valid_subject_case_insensitive(self):
        category, summary, errors = parse_subject("[bug] Lowercase category")
        assert category == TicketCategory.BUG
        assert errors == []

    def test_invalid_category(self):
        category, summary, errors = parse_subject("[Unknown] Some issue")
        assert category is None
        assert len(errors) == 1
        assert "Invalid category" in errors[0]

    def test_missing_category_tag(self):
        category, summary, errors = parse_subject("No category here")
        assert category is None
        assert summary is None
        assert len(errors) == 1
        assert "Subject must follow format" in errors[0]

    def test_empty_subject(self):
        category, summary, errors = parse_subject("")
        assert category is None
        assert len(errors) == 1

    def test_reply_prefix_stripped(self):
        category, summary, errors = parse_subject("RE: [Bug] Original issue")
        assert category == TicketCategory.BUG
        assert summary == "Original issue"
        assert errors == []

    def test_forward_prefix_stripped(self):
        category, summary, errors = parse_subject("Fwd: [Infra] Server down")
        assert category == TicketCategory.INFRA
        assert errors == []


class TestParseBody:
    def test_valid_body(self):
        body = """Project: MyApp
Priority: High
Description:
The login page throws a 500 error when submitting the form.
Steps to reproduce:
1. Go to /login
2. Enter credentials
3. Click submit"""
        project, priority, description, errors = parse_body(body)
        assert project == "MyApp"
        assert priority == TicketPriority.HIGH
        assert "login page throws a 500 error" in description
        assert errors == []

    def test_missing_project(self):
        body = """Priority: Low
Description:
Some description"""
        project, priority, description, errors = parse_body(body)
        assert project is None
        assert any("Project" in e for e in errors)

    def test_missing_priority(self):
        body = """Project: MyApp
Description:
Some description"""
        project, priority, description, errors = parse_body(body)
        assert priority is None
        assert any("Priority" in e for e in errors)

    def test_missing_description(self):
        body = """Project: MyApp
Priority: Medium"""
        project, priority, description, errors = parse_body(body)
        assert description is None
        assert any("Description" in e for e in errors)

    def test_empty_description(self):
        body = """Project: MyApp
Priority: Medium
Description:
"""
        project, priority, description, errors = parse_body(body)
        assert any("empty" in e.lower() for e in errors)

    def test_invalid_priority(self):
        body = """Project: MyApp
Priority: SuperHigh
Description:
Some issue"""
        project, priority, description, errors = parse_body(body)
        assert priority is None
        assert any("Invalid priority" in e for e in errors)

    def test_all_priorities_valid(self):
        for p in ["Low", "Medium", "High", "Critical"]:
            body = f"Project: X\nPriority: {p}\nDescription:\nTest"
            _, priority, _, errors = parse_body(body)
            assert priority is not None
            assert not any("priority" in e.lower() for e in errors)


class TestParseEmailContent:
    def test_valid_email(self):
        parsed = parse_email_content(
            message_id="<msg1@test.com>",
            sender_email="user@test.com",
            subject="[Bug] Login broken",
            body="Project: MyApp\nPriority: High\nDescription:\nLogin is broken",
            attachments=[],
        )
        assert parsed.is_valid
        assert parsed.category == TicketCategory.BUG
        assert parsed.project == "MyApp"
        assert parsed.priority == TicketPriority.HIGH
        assert "Login is broken" in parsed.description
        assert parsed.errors == []

    def test_invalid_email_collects_all_errors(self):
        parsed = parse_email_content(
            message_id="<msg2@test.com>",
            sender_email="user@test.com",
            subject="No format at all",
            body="Just some random text",
            attachments=[],
        )
        assert not parsed.is_valid
        assert len(parsed.errors) >= 3  # subject + project + priority + description

    def test_attachments_preserved(self):
        att = ParsedAttachment(
            filename="screenshot.png",
            content_type="image/png",
            content=b"fake-image-data",
            size_bytes=15,
        )
        parsed = parse_email_content(
            message_id="<msg3@test.com>",
            sender_email="user@test.com",
            subject="[Bug] With attachment",
            body="Project: X\nPriority: Low\nDescription:\nSee attached",
            attachments=[att],
        )
        assert parsed.is_valid
        assert len(parsed.attachments) == 1
        assert parsed.attachments[0].filename == "screenshot.png"

    def test_reply_headers_captured(self):
        parsed = parse_email_content(
            message_id="<msg4@test.com>",
            sender_email="user@test.com",
            subject="[General] Test",
            body="Project: X\nPriority: Low\nDescription:\nTest",
            attachments=[],
            in_reply_to="<original@test.com>",
            references="<original@test.com> <other@test.com>",
        )
        assert parsed.in_reply_to == "<original@test.com>"
        assert "<other@test.com>" in parsed.references
