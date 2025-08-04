"""Unit tests for utility functions in the scraper"""

import pytest
from scrape import clean_pin, make_snake_case, remove_duplicates


@pytest.mark.unit
class TestCleanPin:
    """Test cases for the clean_pin function"""

    def test_clean_pin_valid_format(self):
        """Test cleaning a valid PIN with hyphens"""
        pin = "17-29-304-001-0000"
        result = clean_pin(pin)
        assert result == "17293040010000"
        assert len(result) == 14

    def test_clean_pin_already_clean(self):
        """Test cleaning a PIN that's already clean"""
        pin = "17293040010000"
        result = clean_pin(pin)
        assert result == "17293040010000"

    def test_clean_pin_with_spaces(self):
        """Test cleaning a PIN with spaces"""
        pin = "17 29 304 001 0000"
        result = clean_pin(pin)
        assert result == "17293040010000"

    def test_clean_pin_invalid_length(self):
        """Test that invalid PIN length raises AssertionError"""
        with pytest.raises(AssertionError):
            clean_pin("123456789")

    def test_clean_pin_invalid_type(self):
        """Test that non-string input raises AssertionError"""
        with pytest.raises(AssertionError):
            clean_pin(12345678901234)

    def test_clean_pin_with_letters(self):
        """Test that letters are filtered out"""
        pin = "17-29-304-001-0000ABC"
        result = clean_pin(pin)
        assert result == "17293040010000"


@pytest.mark.unit
class TestMakeSnakeCase:
    """Test cases for the make_snake_case function"""

    def test_make_snake_case_simple(self):
        """Test converting simple string to snake_case"""
        result = make_snake_case("Document Number")
        assert result == "document_number"

    def test_make_snake_case_already_snake(self):
        """Test string that's already in snake_case"""
        result = make_snake_case("document_number")
        assert result == "document_number"

    def test_make_snake_case_multiple_spaces(self):
        """Test string with multiple consecutive spaces"""
        result = make_snake_case("Document  Number")
        assert result == "document__number"

    def test_make_snake_case_non_string_input(self):
        """Test that non-string input is converted to string"""
        result = make_snake_case(123)
        assert result == "123"

    def test_make_snake_case_empty_string(self):
        """Test empty string"""
        result = make_snake_case("")
        assert result == ""

    def test_make_snake_case_special_characters(self):
        """Test string with special characters"""
        result = make_snake_case("Document # Number")
        assert result == "document_#_number"


@pytest.mark.unit
class TestRemoveDuplicates:
    """Test cases for the remove_duplicates function"""

    def test_remove_duplicates_no_duplicates(self):
        """Test list with no duplicates"""
        input_list = ["a", "b", "c"]
        result = remove_duplicates(input_list)
        assert result == ["a", "b", "c"]

    def test_remove_duplicates_with_duplicates(self):
        """Test list with duplicates"""
        input_list = ["a", "b", "a", "c", "b"]
        result = remove_duplicates(input_list)
        assert result == ["a", "b", "c"]

    def test_remove_duplicates_consecutive_duplicates(self):
        """Test list with consecutive duplicates"""
        input_list = ["a", "a", "b", "b", "c"]
        result = remove_duplicates(input_list)
        assert result == ["a", "b", "c"]

    def test_remove_duplicates_empty_list(self):
        """Test empty list"""
        input_list = []
        result = remove_duplicates(input_list)
        assert result == []

    def test_remove_duplicates_single_item(self):
        """Test list with single item"""
        input_list = ["a"]
        result = remove_duplicates(input_list)
        assert result == ["a"]

    def test_remove_duplicates_all_same(self):
        """Test list with all same items"""
        input_list = ["a", "a", "a"]
        result = remove_duplicates(input_list)
        assert result == ["a"] 