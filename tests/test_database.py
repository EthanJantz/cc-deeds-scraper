"""Unit tests for database operations"""

import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base, Document, Entity, Pin, PriorDoc
from scrape import insert_content, create_tables


@pytest.mark.database
class TestDatabaseOperations:
    """Test cases for database operations"""

    @pytest.fixture
    def test_engine(self):
        """Create a test database engine"""
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine

    @pytest.fixture
    def test_session(self, test_engine):
        """Create a test session"""
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
        session = SessionLocal()
        yield session
        session.close()

    def test_create_tables(self, test_engine):
        """Test that tables can be created"""
        # Tables should already be created by the fixture
        from sqlalchemy import inspect
        inspector = inspect(test_engine)
        table_names = inspector.get_table_names()
        
        expected_tables = ['documents', 'entities', 'pins', 'prior_docs']
        for table in expected_tables:
            assert table in table_names

    def test_insert_content_valid_document(self, test_session):
        """Test inserting a valid document with all related data"""
        pin = "17293040010000"
        content = {
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

        insert_content(test_session, pin, content)
        test_session.commit()

        # Verify document was inserted
        document = test_session.query(Document).filter_by(doc_num="2024-123456").first()
        assert document is not None
        assert document.pin == pin
        assert document.date_executed == date(2024, 1, 10)
        assert document.date_recorded == date(2024, 1, 15)
        assert document.num_pages == 5
        assert document.address == "123 Main St, Chicago, IL"
        assert document.doc_type == "Warranty Deed"
        assert document.consideration_amount == "$500,000"
        assert document.pdf_url == "https://example.com/document.pdf"

        # Verify entities were inserted
        entities = test_session.query(Entity).filter_by(doc_num="2024-123456").all()
        assert len(entities) == 3
        
        grantors = [e for e in entities if e.entity_status == "grantor"]
        grantees = [e for e in entities if e.entity_status == "grantee"]
        
        assert len(grantors) == 2
        assert len(grantees) == 1
        
        assert grantors[0].entity_name == "John Doe"
        assert grantors[0].trust_number == "TR-123"
        assert grantors[1].entity_name == "Jane Smith"
        assert grantors[1].trust_number is None
        assert grantees[0].entity_name == "ABC Corporation"
        assert grantees[0].trust_number == "TR-456"

        # Verify related pins were inserted
        pins = test_session.query(Pin).filter_by(doc_num="2024-123456").all()
        assert len(pins) == 2
        pin_values = [p.related_pin for p in pins]
        assert "17293040020000" in pin_values
        assert "17293040030000" in pin_values

        # Verify prior documents were inserted
        prior_docs = test_session.query(PriorDoc).filter_by(doc_num="2024-123456").all()
        assert len(prior_docs) == 2
        prior_doc_nums = [p.prior_doc_num for p in prior_docs]
        assert "2023-123456" in prior_doc_nums
        assert "2023-789012" in prior_doc_nums

    def test_insert_content_no_date_executed(self, test_session):
        """Test inserting document without date executed"""
        pin = "17293040010000"
        content = {
            "doc_info": {
                "document_number": "2024-123456",
                "date_recorded": "01/15/2024",
                "#_of_pages": "5",
                "address": "123 Main St, Chicago, IL",
                "document_type": "Warranty Deed",
                "consideration_amount": "$500,000"
            },
            "entities": {
                "grantors": [],
                "grantees": []
            },
            "related_pins": [],
            "prior_docs": [],
            "pdf_url": "https://example.com/document.pdf"
        }

        insert_content(test_session, pin, content)
        test_session.commit()

        document = test_session.query(Document).filter_by(doc_num="2024-123456").first()
        assert document is not None
        assert document.date_executed is None
        assert document.date_recorded == date(2024, 1, 15)

    def test_insert_content_no_entities(self, test_session):
        """Test inserting document with no entities"""
        pin = "17293040010000"
        content = {
            "doc_info": {
                "document_number": "2024-123456",
                "date_recorded": "01/15/2024",
                "document_type": "Warranty Deed"
            },
            "entities": {
                "grantors": [],
                "grantees": []
            },
            "related_pins": [],
            "prior_docs": [],
            "pdf_url": "https://example.com/document.pdf"
        }

        insert_content(test_session, pin, content)
        test_session.commit()

        document = test_session.query(Document).filter_by(doc_num="2024-123456").first()
        assert document is not None
        
        entities = test_session.query(Entity).filter_by(doc_num="2024-123456").all()
        assert len(entities) == 0

    def test_insert_content_invalid_date_format(self, test_session):
        """Test that invalid date format raises an exception"""
        pin = "17293040010000"
        content = {
            "doc_info": {
                "document_number": "2024-123456",
                "date_executed": "invalid-date",
                "date_recorded": "01/15/2024",
                "document_type": "Warranty Deed"
            },
            "entities": {
                "grantors": [],
                "grantees": []
            },
            "related_pins": [],
            "prior_docs": [],
            "pdf_url": "https://example.com/document.pdf"
        }

        with pytest.raises(ValueError):
            insert_content(test_session, pin, content)

    def test_insert_content_missing_required_fields(self, test_session):
        """Test that missing required fields raises an exception"""
        pin = "17293040010000"
        content = {
            "doc_info": {
                # Missing document_number
                "date_recorded": "01/15/2024",
                "document_type": "Warranty Deed"
            },
            "entities": {
                "grantors": [],
                "grantees": []
            },
            "related_pins": [],
            "prior_docs": [],
            "pdf_url": "https://example.com/document.pdf"
        }

        with pytest.raises(KeyError):
            insert_content(test_session, pin, content) 