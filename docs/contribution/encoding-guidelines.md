# Encoding handling guidelines

## Purpose
Describe UTF-8 and replacement-error handling for logs, reports, and release files.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.