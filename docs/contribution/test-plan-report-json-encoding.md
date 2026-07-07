# Report JSON encoding test plan

## Purpose
Capture checks for UTF-8 JSON output and non-ASCII warning text preservation.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.