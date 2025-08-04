# Scraper Test Suite

This directory contains the comprehensive test suite for the Cook County Recorder scraper.

## Test Structure

### `test_utils.py`
Unit tests for utility functions:
- `clean_pin()` - PIN validation and cleaning
- `make_snake_case()` - String conversion to snake_case
- `remove_duplicates()` - List deduplication

### `test_extraction.py`
Unit tests for HTML parsing and data extraction:
- `extract_info()` - Document metadata extraction
- `extract_grantor_grantee()` - Entity extraction
- `extract_prior_documents()` - Prior document extraction
- `extract_related_pins()` - Related PIN extraction

### `test_database.py`
Database operation tests:
- `insert_content()` - Document and related data insertion
- `create_tables()` - Table schema creation
- Database session management

### `test_integration.py`
Integration tests for the full scraping workflow:
- `retrieve_doc_page_urls()` - URL collection
- `scrape_doc_page()` - Document page scraping
- `scrape_pin()` - Complete PIN scraping workflow
- `get_pins_to_scrape()` - PIN list management

### `conftest.py`
Shared test fixtures and configuration:
- Database fixtures
- Mock environment variables
- Sample data fixtures
- Temporary directory management

## Running Tests

### Using Docker Compose (Recommended)
```bash
# Run all tests
docker-compose run scraper-tests

# Run specific test file
docker-compose run scraper-tests pytest tests/test_utils.py -v

# Run tests with coverage
docker-compose run scraper-tests pytest --cov=scrape --cov-report=html
```

### Running Locally
```bash
# Install dependencies
uv sync

# Run all tests
pytest tests/ -v

# Run specific test categories
pytest tests/ -m unit
pytest tests/ -m integration
pytest tests/ -m database

# Run with coverage
pytest tests/ --cov=scrape --cov-report=term-missing
```

## Test Categories

### Unit Tests (`-m unit`)
- Individual function testing
- Mocked dependencies
- Fast execution

### Integration Tests (`-m integration`)
- End-to-end workflow testing
- Mocked HTTP requests
- Database integration

### Database Tests (`-m database`)
- SQLAlchemy operations
- Data persistence
- Transaction management

## Test Configuration

### Environment Variables
- `DB_URL`: Set to `sqlite:///:memory:` for testing
- All external dependencies are mocked

### Fixtures
- `temp_data_dir`: Temporary directory for file operations
- `sample_pin`: Test PIN data
- `sample_document_data`: Complete document data structure
- `sample_html_document`: HTML content for parsing tests

## Mocking Strategy

### HTTP Requests
- All `requests.get()` calls are mocked
- Returns predefined HTML responses
- Tests both success and error scenarios

### File Operations
- File system operations are mocked
- Uses temporary directories
- Tests file reading/writing scenarios

### Database Operations
- Uses SQLite in-memory database
- Each test gets a clean database
- Tests transaction rollback scenarios

## Coverage

The test suite aims for comprehensive coverage of:
- ✅ Utility functions (100%)
- ✅ Data extraction functions (100%)
- ✅ Database operations (100%)
- ✅ Integration workflows (100%)
- ✅ Error handling scenarios
- ✅ Edge cases and boundary conditions

## Adding New Tests

1. **Unit Tests**: Add to appropriate `test_*.py` file
2. **Integration Tests**: Add to `test_integration.py`
3. **Database Tests**: Add to `test_database.py`
4. **Fixtures**: Add to `conftest.py` if shared

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Test Structure
```python
def test_function_name_scenario(self):
    """Test description"""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result == expected_output
```

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:
- Fast execution (< 30 seconds)
- No external dependencies
- Deterministic results
- Clear error reporting 