# Process detection test plan

## Purpose
Add scenarios for exact process matching, slash-prefixed commands, and process names containing regex metacharacters.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.