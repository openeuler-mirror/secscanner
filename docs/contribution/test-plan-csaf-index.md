# CSAF index parser test plan

## Purpose
Document cases for blank index responses, CRLF line endings, duplicate entries, and retry failure behavior.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.