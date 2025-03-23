# pytest-reporter-html

A pytest plugin that generates comprehensive HTML and JSON test reports with visual charts, filtering, and detailed test information.

## Features

- Interactive HTML reports with charts and graphs
- Detailed test results with expandable error messages
- Categorized test results based on test naming patterns
- Filters to sort and search through test results
- JSON export for CI/CD integration
- Clean, modern UI with responsive design

## Installation

```bash
pip install pytest-reporter-html
```

## Usage

### As a Command Line Tool

```bash
# Basic usage
pytest-reporter

# Specify test files
pytest-reporter --test-files test_api.py test_models.py

# Custom report filenames
pytest-reporter --html custom_report.html --json custom_report.json
```

### As a pytest Plugin

```python
import pytest
from pytest_reporter_html import TestReportPlugin

def test_with_report():
    # Create the plugin
    report_plugin = TestReportPlugin()
    
    # Run pytest with the plugin
    pytest.main(['-v', 'test_file.py'], plugins=[report_plugin])
    
    # Generate reports
    report_plugin.generate_html_report('my_report.html')
    report_plugin.generate_json_report('my_report.json')
```

## Report Features

### Summary Dashboard

The HTML report includes a summary dashboard with:

- Total tests count
- Passed tests count
- Failed tests count
- Skipped tests count
- Error count
- Test duration
- Pass rate percentage

### Visual Charts

- Pie chart showing the distribution of test results
- Bar chart showing test categories with pass/fail breakdown

### Detailed Test Table

- Complete list of all tests with status and duration
- Expandable rows for error details
- Filtering by test status and category
- Search functionality

## Customization

The plugin automatically categorizes tests based on naming patterns. For example:

- `test_create_task()` → Category: "create"
- `test_update_user()` → Category: "update"
- `test_delete_record()` → Category: "delete"

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.