#!/usr/bin/env python

from pytest_reporter_html import TestReportPlugin
import pytest
import os

def main():
    # Path to the example test file
    this_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(this_dir, "sample_test.py")
    
    # Create the plugin
    report_plugin = TestReportPlugin()
    
    # Run pytest with the plugin
    pytest.main(['-v', test_file], plugins=[report_plugin])
    
    # Generate reports
    html_report = os.path.join(this_dir, "example_report.html")
    json_report = os.path.join(this_dir, "example_report.json")
    
    report_plugin.generate_html_report(html_report)
    report_plugin.generate_json_report(json_report)
    
    print(f"\nReports generated:")
    print(f"HTML: {html_report}")
    print(f"JSON: {json_report}")

if __name__ == "__main__":
    main()