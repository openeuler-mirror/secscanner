# PRETTY_NAME decoding test plan

## Purpose
Define cases for invalid UTF-8 bytes in os-release output and replacement decoding.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.