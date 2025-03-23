import pytest
import json
import os
from datetime import datetime
from collections import defaultdict
import re

class TestReportPlugin:
    """Pytest plugin to collect test results and generate a report."""
    
    def __init__(self):
        self.test_results = []
        self.summary = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "error": 0,
            "duration": 0
        }
        self.categories = defaultdict(lambda: {"passed": 0, "failed": 0, "skipped": 0, "error": 0})
        self.start_time = None
        
    def pytest_sessionstart(self, session):
        self.start_time = datetime.now()
    
    def pytest_sessionfinish(self, session, exitstatus):
        self.summary["duration"] = (datetime.now() - self.start_time).total_seconds()
        
    def pytest_runtest_logreport(self, report):
        if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
            test_name = report.nodeid.split("::")[-1]
            test_file = report.nodeid.split("::")[0]
            
            # Extract category from test name
            # Assuming test functions follow patterns like test_create_task, test_update_task, etc.
            category_match = re.search(r'test_(\w+)_', test_name)
            if category_match:
                category = category_match.group(1)
            else:
                category = "other"
            
            # Capture test docstring for description
            docstring = report.longrepr if hasattr(report, 'longrepr') else None
            if hasattr(report, 'function') and report.function.__doc__:
                description = report.function.__doc__.strip()
            else:
                description = test_name
            
            # Format error message if any
            error_message = ""
            if hasattr(report, "longrepr") and report.longrepr:
                if isinstance(report.longrepr, tuple):
                    error_message = str(report.longrepr[2])
                else:
                    error_message = str(report.longrepr)
            
            # Update summary statistics
            self.summary["total"] += 1
            self.summary[report.outcome] += 1
            self.categories[category][report.outcome] += 1
            
            # Store detailed test result
            self.test_results.append({
                "name": test_name,
                "file": test_file,
                "category": category,
                "description": description,
                "outcome": report.outcome,
                "duration": report.duration,
                "error_message": error_message if report.outcome == "failed" else ""
            })
    
    def generate_html_report(self, output_file="test_report.html"):
        """Generate an HTML report from the test results."""
        template = self._get_html_template()
        
        # Calculate pass rate percentage
        pass_rate = (self.summary["passed"] / self.summary["total"]) * 100 if self.summary["total"] > 0 else 0
        
        # Convert test results and categories to JSON for template
        test_results_json = json.dumps(self.test_results)
        categories_json = json.dumps(dict(self.categories))
        
        # Generate HTML report
        html_report = template.format(
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            test_results=test_results_json,
            categories=categories_json,
            total=self.summary["total"],
            passed=self.summary["passed"],
            failed=self.summary["failed"],
            skipped=self.summary["skipped"],
            error=self.summary["error"],
            duration=f"{self.summary['duration']:.2f}",
            pass_rate=f"{pass_rate:.1f}"
        )
        
        # Write the report to file
        with open(output_file, "w") as f:
            f.write(html_report)
        
        print(f"Test report generated: {os.path.abspath(output_file)}")
        return html_report
    
    def generate_json_report(self, output_file="test_report.json"):
        """Generate a JSON report from the test results."""
        report_data = {
            "summary": self.summary,
            "categories": dict(self.categories),
            "tests": self.test_results,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(output_file, "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"JSON report generated: {os.path.abspath(output_file)}")
        return report_data
        
    def _get_html_template(self):
        """Return the HTML template for the report."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Test Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }}
        .timestamp {{
            font-size: 14px;
            color: #7f8c8d;
        }}
        .summary-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            flex: 1;
            min-width: 150px;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .card-title {{
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .card-value {{
            font-size: 24px;
            font-weight: bold;
        }}
        .pass {{
            background-color: #e8f5e9;
            color: #2e7d32;
        }}
        .fail {{
            background-color: #ffebee;
            color: #c62828;
        }}
        .skip {{
            background-color: #e3f2fd;
            color: #1565c0;
        }}
        .error {{
            background-color: #fff3e0;
            color: #e65100;
        }}
        .total {{
            background-color: #f3e5f5;
            color: #6a1b9a;
        }}
        .time {{
            background-color: #e8eaf6;
            color: #283593;
        }}
        .rate {{
            background-color: #e0f2f1;
            color: #00695c;
        }}
        .chart-container {{
            display: flex;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .chart {{
            flex: 1;
            height: 300px;
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        .test-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .test-table th, .test-table td {{
            text-align: left;
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }}
        .test-table th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .test-table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .status-badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .passed {{
            background-color: #e8f5e9;
            color: #2e7d32;
        }}
        .failed {{
            background-color: #ffebee;
            color: #c62828;
        }}
        .skipped {{
            background-color: #e3f2fd;
            color: #1565c0;
        }}
        .error-badge {{
            background-color: #fff3e0;
            color: #e65100;
        }}
        .details-row {{
            display: none;
            background-color: #f9f9f9;
        }}
        .details-content {{
            padding: 15px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 13px;
            color: #333;
        }}
        .error-message {{
            background-color: #ffebee;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 12px;
            color: #c62828;
        }}
        .filter-container {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .filter-dropdown {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: white;
        }}
        .search-input {{
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>FastAPI Tasks API Test Report</h1>
            <div class="timestamp">Generated on: {datetime}</div>
        </div>
        
        <div class="summary-container">
            <div class="summary-card total">
                <div class="card-title">TOTAL TESTS</div>
                <div class="card-value">{total}</div>
            </div>
            <div class="summary-card pass">
                <div class="card-title">PASSED</div>
                <div class="card-value">{passed}</div>
            </div>
            <div class="summary-card fail">
                <div class="card-title">FAILED</div>
                <div class="card-value">{failed}</div>
            </div>
            <div class="summary-card skip">
                <div class="card-title">SKIPPED</div>
                <div class="card-value">{skipped}</div>
            </div>
            <div class="summary-card error">
                <div class="card-title">ERROR</div>
                <div class="card-value">{error}</div>
            </div>
            <div class="summary-card time">
                <div class="card-title">DURATION (s)</div>
                <div class="card-value">{duration}</div>
            </div>
            <div class="summary-card rate">
                <div class="card-title">PASS RATE</div>
                <div class="card-value">{pass_rate}%</div>
            </div>
        </div>
        
        <div class="chart-container">
            <div class="chart" id="results-chart">
                <h3>Test Results</h3>
                <canvas id="results-pie-chart"></canvas>
            </div>
            <div class="chart" id="categories-chart">
                <h3>Tests by Category</h3>
                <canvas id="categories-bar-chart"></canvas>
            </div>
        </div>
        
        <h2>Test Details</h2>
        
        <div class="filter-container">
            <select class="filter-dropdown" id="status-filter">
                <option value="all">All Statuses</option>
                <option value="passed">Passed</option>
                <option value="failed">Failed</option>
                <option value="skipped">Skipped</option>
                <option value="error">Error</option>
            </select>
            <select class="filter-dropdown" id="category-filter">
                <option value="all">All Categories</option>
            </select>
            <input type="text" class="search-input" id="search-input" placeholder="Search test names...">
        </div>
        
        <table class="test-table" id="test-table">
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Category</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                </tr>
            </thead>
            <tbody id="test-table-body">
                <!-- Test rows will be populated by JavaScript -->
            </tbody>
        </table>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        // Parse test results and categories from JSON
        const testResults = {test_results};
        const categories = {categories};
        
        // Function to initialize the dashboard
        function initializeDashboard() {{
            renderResultsChart();
            renderCategoriesChart();
            populateTestTable();
            setupFilters();
        }}
        
        // Render test results pie chart
        function renderResultsChart() {{
            const ctx = document.getElementById('results-pie-chart').getContext('2d');
            new Chart(ctx, {{
                type: 'pie',
                data: {{
                    labels: ['Passed', 'Failed', 'Skipped', 'Error'],
                    datasets: [{{
                        data: [{passed}, {failed}, {skipped}, {error}],
                        backgroundColor: [
                            '#66bb6a',  // green
                            '#ef5350',  // red
                            '#42a5f5',  // blue
                            '#ffa726'   // orange
                        ],
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    legend: {{
                        position: 'right'
                    }}
                }}
            }});
        }}
        
        // Render categories bar chart
        function renderCategoriesChart() {{
            const categoryNames = Object.keys(categories);
            const passedData = categoryNames.map(cat => categories[cat].passed || 0);
            const failedData = categoryNames.map(cat => categories[cat].failed || 0);
            const skippedData = categoryNames.map(cat => categories[cat].skipped || 0);
            const errorData = categoryNames.map(cat => categories[cat].error || 0);
            
            const ctx = document.getElementById('categories-bar-chart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: categoryNames,
                    datasets: [
                        {{
                            label: 'Passed',
                            backgroundColor: '#66bb6a',
                            data: passedData
                        }},
                        {{
                            label: 'Failed',
                            backgroundColor: '#ef5350',
                            data: failedData
                        }},
                        {{
                            label: 'Skipped',
                            backgroundColor: '#42a5f5',
                            data: skippedData
                        }},
                        {{
                            label: 'Error',
                            backgroundColor: '#ffa726',
                            data: errorData
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        xAxes: [{{
                            stacked: true,
                            gridLines: {{
                                display: false
                            }}
                        }}],
                        yAxes: [{{
                            stacked: true,
                            ticks: {{
                                beginAtZero: true
                            }}
                        }}]
                    }}
                }}
            }});
        }}
        
        // Populate the test details table
        function populateTestTable() {{
            const tableBody = document.getElementById('test-table-body');
            tableBody.innerHTML = '';
            
            // Populate category filter dropdown
            const categoryFilter = document.getElementById('category-filter');
            const uniqueCategories = [...new Set(testResults.map(test => test.category))];
            uniqueCategories.forEach(category => {{
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categoryFilter.appendChild(option);
            }});
            
            // Create table rows for each test
            testResults.forEach((test, index) => {{
                const row = document.createElement('tr');
                row.setAttribute('data-test-index', index);
                row.setAttribute('data-status', test.outcome);
                row.setAttribute('data-category', test.category);
                
                // Make the row expandable if it has an error message
                if (test.error_message) {{
                    row.classList.add('expandable');
                    row.style.cursor = 'pointer';
                    row.onclick = function() {{
                        const detailsRow = document.getElementById(`details-row-${{index}}`);
                        if (detailsRow.style.display === 'table-row') {{
                            detailsRow.style.display = 'none';
                        }} else {{
                            detailsRow.style.display = 'table-row';
                        }}
                    }};
                }}
                
                row.innerHTML = `
                    <td><strong>${{test.name}}</strong><br><small>${{test.description}}</small></td>
                    <td>${{test.category}}</td>
                    <td><span class="status-badge ${{test.outcome}}">${{test.outcome}}</span></td>
                    <td>${{test.duration.toFixed(3)}}</td>
                `;
                
                tableBody.appendChild(row);
                
                // Add details row for errors
                if (test.error_message) {{
                    const detailsRow = document.createElement('tr');
                    detailsRow.id = `details-row-${{index}}`;
                    detailsRow.className = 'details-row';
                    detailsRow.innerHTML = `
                        <td colspan="4">
                            <div class="details-content">
                                <div class="error-message">${{test.error_message.replace(/</g, '&lt;').replace(/>/g, '&gt;')}}</div>
                            </div>
                        </td>
                    `;
                    tableBody.appendChild(detailsRow);
                }}
            }});
        }}
        
        // Setup filters for the test table
        function setupFilters() {{
            const statusFilter = document.getElementById('status-filter');
            const categoryFilter = document.getElementById('category-filter');
            const searchInput = document.getElementById('search-input');
            
            function applyFilters() {{
                const statusValue = statusFilter.value;
                const categoryValue = categoryFilter.value;
                const searchValue = searchInput.value.toLowerCase();
                
                const rows = document.querySelectorAll('#test-table-body > tr:not(.details-row)');
                
                rows.forEach(row => {{
                    const testIndex = row.getAttribute('data-test-index');
                    const detailsRow = document.getElementById(`details-row-${{testIndex}}`);
                    
                    const status = row.getAttribute('data-status');
                    const category = row.getAttribute('data-category');
                    const testName = testResults[testIndex].name.toLowerCase();
                    const testDesc = testResults[testIndex].description.toLowerCase();
                    
                    const statusMatch = statusValue === 'all' || status === statusValue;
                    const categoryMatch = categoryValue === 'all' || category === categoryValue;
                    const searchMatch = searchValue === '' || 
                                      testName.includes(searchValue) || 
                                      testDesc.includes(searchValue);
                    
                    if (statusMatch && categoryMatch && searchMatch) {{
                        row.style.display = 'table-row';
                        if (detailsRow) {{
                            // Keep details row hidden unless expanded
                            detailsRow.style.display = 'none';
                        }}
                    }} else {{
                        row.style.display = 'none';
                        if (detailsRow) {{
                            detailsRow.style.display = 'none';
                        }}
                    }}
                }});
            }}
            
            statusFilter.addEventListener('change', applyFilters);
            categoryFilter.addEventListener('change', applyFilters);
            searchInput.addEventListener('input', applyFilters);
        }}
        
        // Initialize the dashboard when the page loads
        document.addEventListener('DOMContentLoaded', initializeDashboard);
    </script>
</body>
</html>
"""