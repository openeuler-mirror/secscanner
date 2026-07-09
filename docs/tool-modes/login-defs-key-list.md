# login_defs_key_list mode usage

## Source
$rel

## Default mode
$mode

## Purpose
This note records the default behavior of the tool and provides a review target for branches that make the mode selectable from the command line.

## Review checklist
- The default behavior should remain compatible with $mode.
- Any added --mode option should document valid choices in argparse.
- Mode-specific options should only be shown when they affect reachable code paths.