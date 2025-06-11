# Purpose:
#   Unit tests for submitter functions using mocking for file I/O.

import os
import tempfile
from unittest.mock import patch, mock_open
# The test file is importing these functions from the submitter.py file inside the scripts folder.
from scripts.submitter import load_report, prepare_manual_submission, log_preparation

def test_load_report():
    sample_text = "Test bug report content."
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp_file:
        tmp_file.write(sample_text)
        tmp_filename = tmp_file.name

    result = load_report(tmp_filename)
    assert result == sample_text

    os.remove(tmp_filename)

@patch("builtins.open", new_callable=mock_open)
def test_prepare_manual_submission(mock_file):
    report = "Bug report content"
    test_file = "submissions/manual_submission.txt"
    prepare_manual_submission(report, test_file)
    mock_file.assert_called_with(test_file, 'w')
    handle = mock_file()
    handle.write.assert_any_call("=== MANUAL SUBMISSION REQUIRED ===\n")
    handle.write.assert_any_call("=== REPORT CONTENT ===\n\n")
    handle.write.assert_any_call(report)

@patch("builtins.open", new_callable=mock_open)
def test_log_preparation(mock_file):
    log_file = "logs/test_submission.log"
    log_preparation("Ready", log_file)
    mock_file.assert_called_with(log_file, 'a')
    handle = mock_file()
    handle.write.assert_called_with("Preparation status: Ready\n")
