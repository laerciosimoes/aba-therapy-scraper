import pytest

from scrapper.TeamExtractor import TeamExtractor


def test_ensure_protocol_adds_https():
    extractor = TeamExtractor()
    # Cases without and with existing schemes
    assert extractor.ensure_protocol("example.com") == "https://example.com"
    assert extractor.ensure_protocol("http://example.com") == "http://example.com"
    assert extractor.ensure_protocol("https://example.com") == "https://example.com"


def test_extract_success(monkeypatch):
    # Dummy implementations to simulate SmartScraperGraph and SmartScraperMultiGraph
    class DummyGraph:
        def __init__(self, prompt, source, config):
            self.prompt = prompt
            self.source = source
            self.config = config

        def run(self):
            # Simulate extracting page content
            return {"content": "<html>dummy content</html>"}

    class DummyMultiGraph:
        def __init__(self, prompt, source, config):
            self.prompt = prompt
            self.source = source
            self.config = config

        def run(self):
            # Simulate extracting team member details
            return {
                "team_members": [
                    {"name": "Alice", "position": "Engineer"},
                    {"name": "Bob", "position": "Manager"},
                ]
            }

    # Patch the imported classes in the TeamExtractor module
    monkeypatch.setattr(
        "scrapper.TeamExtractor.SmartScraperGraph",
        DummyGraph,
    )
    monkeypatch.setattr(
        "scrapper.TeamExtractor.SmartScraperMultiGraph",
        DummyMultiGraph,
    )

    extractor = TeamExtractor()
    result = extractor.extract("example.com")
    expected = [
        {"Url": "example.com", "name": "Alice", "position": "Engineer"},
        {"Url": "example.com", "name": "Bob", "position": "Manager"},
    ]
    assert result == expected


def test_extract_empty_on_no_content(monkeypatch):
    # Simulate graph returning empty content
    class EmptyContentGraph:
        def __init__(self, prompt, source, config):
            pass

        def run(self):
            return {"content": ""}

    monkeypatch.setattr(
        "scrapper.TeamExtractor.SmartScraperGraph",
        EmptyContentGraph,
    )

    extractor = TeamExtractor()
    # Should return empty list when no content
    assert extractor.extract("example.com") == []


def test_extract_empty_on_exception(monkeypatch, capsys):
    # Simulate graph initialization raising an exception
    class BadGraph:
        def __init__(self, prompt, source, config):
            raise RuntimeError("Initialization failed")

    monkeypatch.setattr(
        "scrapper.TeamExtractor.SmartScraperGraph",
        BadGraph,
    )

    extractor = TeamExtractor()
    result = extractor.extract("example.com")
    captured = capsys.readouterr()

    # Should catch exception and return empty list, printing the error
    assert result == []
    assert "Error: Initialization failed" in captured.out
