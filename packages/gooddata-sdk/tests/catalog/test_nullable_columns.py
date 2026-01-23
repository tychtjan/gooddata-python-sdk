# (C) 2024 GoodData Corporation
"""Tests for nullable columns support in declarative models."""

import pytest
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.column import CatalogDeclarativeColumn
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    CatalogDeclarativeAttribute,
    CatalogDeclarativeFact,
    CatalogDeclarativeLabel,
    CatalogDeclarativeAggregatedFact,
    CatalogDeclarativeReferenceSource,
)
from gooddata_sdk.catalog.identifier import CatalogGrainIdentifier


def test_catalog_declarative_column_nullable_fields():
    """Test that CatalogDeclarativeColumn supports nullable fields."""
    column = CatalogDeclarativeColumn(
        name="test_column",
        data_type="STRING",
        is_nullable=True,
        null_value="NULL"
    )
    
    assert column.name == "test_column"
    assert column.data_type == "STRING"
    assert column.is_nullable is True
    assert column.null_value == "NULL"
    
    # Test default values
    column_default = CatalogDeclarativeColumn(
        name="default_column",
        data_type="INT"
    )
    assert column_default.is_nullable is None
    assert column_default.null_value is None


def test_catalog_declarative_fact_nullable_fields():
    """Test that CatalogDeclarativeFact supports nullable fields."""
    fact = CatalogDeclarativeFact(
        id="test_fact",
        title="Test Fact",
        source_column="test_column",
        is_nullable=True,
        null_value="0"
    )
    
    assert fact.id == "test_fact"
    assert fact.title == "Test Fact"
    assert fact.source_column == "test_column"
    assert fact.is_nullable is True
    assert fact.null_value == "0"


def test_catalog_declarative_attribute_nullable_fields():
    """Test that CatalogDeclarativeAttribute supports nullable fields."""
    attribute = CatalogDeclarativeAttribute(
        id="test_attribute",
        title="Test Attribute",
        source_column="test_column",
        labels=[],
        is_nullable=True,
        null_value="UNKNOWN"
    )
    
    assert attribute.id == "test_attribute"
    assert attribute.title == "Test Attribute"
    assert attribute.source_column == "test_column"
    assert attribute.is_nullable is True
    assert attribute.null_value == "UNKNOWN"


def test_catalog_declarative_label_nullable_fields():
    """Test that CatalogDeclarativeLabel supports nullable fields."""
    label = CatalogDeclarativeLabel(
        id="test_label",
        title="Test Label",
        source_column="test_column",
        is_nullable=False,
        null_value=None
    )
    
    assert label.id == "test_label"
    assert label.title == "Test Label" 
    assert label.source_column == "test_column"
    assert label.is_nullable is False
    assert label.null_value is None


def test_catalog_declarative_aggregated_fact_nullable_fields():
    """Test that CatalogDeclarativeAggregatedFact supports nullable fields."""
    agg_fact = CatalogDeclarativeAggregatedFact(
        id="test_agg_fact",
        source_column="test_column",
        is_nullable=True,
        null_value="0.0"
    )
    
    assert agg_fact.id == "test_agg_fact"
    assert agg_fact.source_column == "test_column"
    assert agg_fact.is_nullable is True
    assert agg_fact.null_value == "0.0"


def test_catalog_declarative_reference_source_nullable_fields():
    """Test that CatalogDeclarativeReferenceSource supports nullable fields."""
    target = CatalogGrainIdentifier(id="target_id", type="attribute")
    
    ref_source = CatalogDeclarativeReferenceSource(
        column="ref_column",
        target=target,
        is_nullable=True,
        null_value="EMPTY"
    )
    
    assert ref_source.column == "ref_column"
    assert ref_source.target == target
    assert ref_source.is_nullable is True
    assert ref_source.null_value == "EMPTY"


def test_api_conversion():
    """Test that the models can convert to API objects."""
    column = CatalogDeclarativeColumn(
        name="test_column",
        data_type="STRING",
        is_nullable=True,
        null_value="NULL"
    )
    
    # This should not raise an error
    api_obj = column.to_api()
    assert api_obj is not None
    
    # Test that the API object has the correct class
    assert column.client_class().__name__ == "DeclarativeColumn"