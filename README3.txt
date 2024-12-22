How to Run Integration Tests
Prerequisites
Python 3.6 or higher
pytest
requests

You can install the required packages using pip:
pip install pytest requests

Running the Integration Tests
Navigate to the 3_integration_testing directory.
Run the pytest command:
pytest

The tests will run, and you will see the results in your terminal.

Test Structure
test_endpoints.py: Contains integration tests for API endpoints.
test_workflow.py: Contains tests for complete application workflows.
