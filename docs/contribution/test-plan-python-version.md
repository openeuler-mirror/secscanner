# Python version guard test plan

## Purpose
Capture expected exit behavior when secScanner is launched with an unsupported Python major version.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.