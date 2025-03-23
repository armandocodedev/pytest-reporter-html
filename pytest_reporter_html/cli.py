#!/usr/bin/env python

import sys
import pytest
import argparse
from .plugin import TestReportPlugin

def main():
    """Run tests and generate reports."""
    parser = argparse.ArgumentParser(description="Run tests and generate HTML/JSON reports")
    parser.add_argument("--test-files", nargs="*", help="Specific test files to run")
    parser.add_argument("--html", default="test_report.html", help="HTML report filename")
    parser.add_argument("--json", default="test_report.json", help="JSON report filename")
    parser.add_argument("--title", default="Test Report", help="Report title")
    
    args, pytest_args = parser.parse_known_args()
    
    # Create the plugin instance
    report_plugin = TestReportPlugin()
    
    # Construct pytest args
    if args.test_files:
        pytest_args.extend(args.test_files)
    
    # Run pytest with our plugin
    print(f"Running tests: {' '.join(pytest_args)}")
    exit_code = pytest.main(pytest_args, plugins=[report_plugin])
    
    # Generate reports
    report_plugin.generate_html_report(args.html)
    report_plugin.generate_json_report(args.json)
    
    print("\nTest Summary:")
    print(f"Total: {report_plugin.summary['total']}")
    print(f"Passed: {report_plugin.summary['passed']}")
    print(f"Failed: {report_plugin.summary['failed']}")
    print(f"Skipped: {report_plugin.summary['skipped']}")
    print(f"Error: {report_plugin.summary['error']}")
    print(f"Duration: {report_plugin.summary['duration']:.2f} seconds")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())