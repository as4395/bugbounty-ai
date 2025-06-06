# Logs

This folder contains log files generated during the execution of the Bug Bounty AI Workflow.

## Purpose

Logs are used to track system activity, record scanning/reporting actions, and help debug any issues during automated workflows.

## File(s)

- **`bugbounty.log`** – Central log file for status messages, errors, warnings, and info across all modules.

## Notes

- The log file is automatically generated when the system runs.
- You can enable or disable file logging via the `to_file=True` parameter in `logger.log()` calls.
