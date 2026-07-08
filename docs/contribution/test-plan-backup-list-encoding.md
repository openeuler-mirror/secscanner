# Backup list encoding test plan

## Purpose
Describe tests for reading and clearing bak.py when backup file names contain non-ASCII characters.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.