"""Smoke test to verify the test suite is working"""

import pytest


@pytest.mark.unit
def test_smoke():
    """Basic smoke test to verify pytest is working"""
    assert True


@pytest.mark.unit
def test_import_scrape():
    """Test that we can import the main scrape module"""
    try:
        import scrape
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import scrape module: {e}")


@pytest.mark.unit
def test_import_models():
    """Test that we can import the models module"""
    try:
        import models
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import models module: {e}") 