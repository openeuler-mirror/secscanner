# Distribution detection test plan

## Purpose
List tests for os-release, redhat-release, unsupported versions, and missing release files.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.