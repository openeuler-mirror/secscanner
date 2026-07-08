# Rootkit empty suite test plan

## Purpose
Document expected behavior when the rootkit check directory has no matching R-numbered modules.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.