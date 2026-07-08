# PR test checklist

## Purpose
Provide a short checklist for syntax parsing, branch diff checks, and targeted tests before submitting PRs.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.