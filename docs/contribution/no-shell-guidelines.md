# No-shell subprocess guidelines

## Purpose
Document when to prefer subprocess argument lists over shell-form commands.

## Suggested coverage
- Validate the success path with representative input.
- Validate the failure or empty-input path.
- Keep mocks local to the test so it can run without changing host security settings.

## Notes
This file is intentionally isolated so the branch can be reviewed independently.