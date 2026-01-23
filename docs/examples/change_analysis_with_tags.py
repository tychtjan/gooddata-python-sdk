#!/usr/bin/env python3
# (C) 2022 GoodData Corporation
"""
Example: Change Analysis with Tag Filtering

This example demonstrates how to use the new include_tags and exclude_tags
parameters in change analysis requests to filter which attributes and measures
are considered during the analysis.

The tag filtering feature allows you to:
- Include only attributes/measures with specific tags (include_tags)
- Exclude attributes/measures with specific tags (exclude_tags)
- Combine both include and exclude filters for fine-grained control

This is useful for focusing change analysis on specific subsets of your data model,
such as only analyzing financial metrics or excluding deprecated measures.
"""

from gooddata_api_client.model.attribute_item import AttributeItem
from gooddata_api_client.model.change_analysis_request import ChangeAnalysisRequest
from gooddata_api_client.model.measure_item import MeasureItem
from gooddata_api_client.model.object_identifier import ObjectIdentifier


def create_change_analysis_request_with_tags():
    """Create a change analysis request with tag filtering."""
    
    # Define the date attribute for time-based analysis
    date_attribute = AttributeItem(
        object_identifier=ObjectIdentifier(id="created_date", type="attribute")
    )
    
    # Define the measure to analyze
    measure = MeasureItem(
        object_identifier=ObjectIdentifier(id="total_revenue", type="measure")
    )
    
    # Create change analysis request with tag filters
    request = ChangeAnalysisRequest(
        analyzed_period="2025-02",  # Period to analyze
        reference_period="2025-01",  # Reference period for comparison
        date_attribute=date_attribute,
        measure=measure,
        
        # NEW: Tag filtering parameters
        include_tags=["financial", "important", "quarterly"],  # Only include items with these tags
        exclude_tags=["deprecated", "test", "internal"],       # Exclude items with these tags
        
        # Optional: Use smart attribute selection
        use_smart_attribute_selection=True
    )
    
    return request


def create_focused_analysis_example():
    """Example of using tags to focus analysis on specific business areas."""
    
    date_attribute = AttributeItem(
        object_identifier=ObjectIdentifier(id="order_date", type="attribute")
    )
    
    measure = MeasureItem(
        object_identifier=ObjectIdentifier(id="sales_amount", type="measure")
    )
    
    # Focus only on sales-related metrics, exclude internal/testing data
    request = ChangeAnalysisRequest(
        analyzed_period="2024-Q4",
        reference_period="2024-Q3",
        date_attribute=date_attribute,
        measure=measure,
        include_tags=["sales", "customer-facing", "kpi"],
        exclude_tags=["internal", "staging", "deprecated"]
    )
    
    return request


def create_quality_focused_analysis():
    """Example of excluding poor quality or unreliable data using tags."""
    
    date_attribute = AttributeItem(
        object_identifier=ObjectIdentifier(id="event_date", type="attribute")
    )
    
    measure = MeasureItem(
        object_identifier=ObjectIdentifier(id="conversion_rate", type="measure")
    )
    
    # Exclude data quality issues and focus on verified metrics
    request = ChangeAnalysisRequest(
        analyzed_period="2025-01",
        reference_period="2024-12",
        date_attribute=date_attribute,
        measure=measure,
        exclude_tags=[
            "data-quality-issues",
            "incomplete",
            "beta",
            "experimental"
        ]
    )
    
    return request


def usage_example():
    """Complete example showing how to use change analysis with tags."""
    
    print("Creating change analysis requests with tag filtering...")
    
    # Example 1: Basic tag filtering
    basic_request = create_change_analysis_request_with_tags()
    print(f"Basic request include_tags: {basic_request.include_tags}")
    print(f"Basic request exclude_tags: {basic_request.exclude_tags}")
    
    # Example 2: Focus on specific business area
    focused_request = create_focused_analysis_example()
    print(f"Focused request include_tags: {focused_request.include_tags}")
    print(f"Focused request exclude_tags: {focused_request.exclude_tags}")
    
    # Example 3: Quality-focused analysis
    quality_request = create_quality_focused_analysis()
    print(f"Quality request exclude_tags: {quality_request.exclude_tags}")
    
    print("\nTag filtering allows you to:")
    print("- Focus analysis on specific business areas or data types")
    print("- Exclude deprecated, experimental, or low-quality data")
    print("- Ensure consistent analysis by including only approved metrics")
    print("- Improve performance by reducing the scope of analysis")


if __name__ == "__main__":
    usage_example()