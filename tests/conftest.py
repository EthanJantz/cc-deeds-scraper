"""Shared test fixtures and configuration"""

import pytest
import os
import tempfile
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_environment():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'DB_URL': 'sqlite:///:memory:'
    }):
        yield


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create data subdirectory
        data_dir = os.path.join(temp_dir, 'data')
        os.makedirs(data_dir)
        
        # Create logs subdirectory
        logs_dir = os.path.join(temp_dir, 'logs')
        os.makedirs(logs_dir)
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        yield temp_dir
        
        # Restore original directory
        os.chdir(original_cwd)


@pytest.fixture
def sample_pin():
    """Sample PIN for testing"""
    return "17-29-304-001-0000"


@pytest.fixture
def sample_document_data():
    """Sample document data for testing"""
    return {
        "doc_info": {
            "document_number": "2024-123456",
            "date_executed": "01/10/2024",
            "date_recorded": "01/15/2024",
            "#_of_pages": "5",
            "address": "123 Main St, Chicago, IL",
            "document_type": "Warranty Deed",
            "consideration_amount": "$500,000"
        },
        "entities": {
            "grantors": [
                {"name": "John Doe", "trust_number": "TR-123"},
                {"name": "Jane Smith", "trust_number": None}
            ],
            "grantees": [
                {"name": "ABC Corporation", "trust_number": "TR-456"}
            ]
        },
        "related_pins": ["17293040020000", "17293040030000"],
        "prior_docs": ["2023-123456", "2023-789012"],
        "pdf_url": "https://example.com/document.pdf"
    }


@pytest.fixture
def sample_html_document():
    """Sample HTML document for testing"""
    return """
    <html>
        <body>
            <span>Viewing Document</span>
            <table>
                <tr>
                    <td><label>Document Number:</label></td>
                    <td>2024-123456</td>
                </tr>
                <tr>
                    <td><label>Date Recorded:</label></td>
                    <td>01/15/2024</td>
                </tr>
                <tr>
                    <td><label>Document Type:</label></td>
                    <td>Warranty Deed</td>
                </tr>
            </table>
            <span class="fs-5">Grantors</span>
            <table class="table">
                <tbody>
                    <tr>
                        <td><a href="#">John Doe</a></td>
                        <td>TR-123</td>
                    </tr>
                </tbody>
            </table>
            <span class="fs-5">Grantees</span>
            <table class="table">
                <tbody>
                    <tr>
                        <td><a href="#">ABC Corporation</a></td>
                        <td>TR-456</td>
                    </tr>
                </tbody>
            </table>
            <span>Prior Documents</span>
            <table>
                <tbody>
                    <tr>
                        <td>2023-001</td>
                        <td>2023-123456</td>
                    </tr>
                </tbody>
            </table>
            <span>Legal Description</span>
            <table>
                <tbody>
                    <tr>
                        <td>17-29-304-002-0000</td>
                        <td>Some description</td>
                    </tr>
                </tbody>
            </table>
            <a href="/Document/DisplayPdf/123">PDF</a>
        </body>
    </html>
    """ 