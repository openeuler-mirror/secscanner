# CVSS vector parser unit test plan

## Purpose
Add focused coverage for empty vectors, malformed vector parts, and metric-specific lookups in the CVSS parser.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.