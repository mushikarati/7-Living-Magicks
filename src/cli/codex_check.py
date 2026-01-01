#!/usr/bin/env python3
"""
codex check - Validate token sequences against the 7-color adjacency law.

Usage:
    codex check <file>          # Check a file
    codex check --stdin         # Check from stdin
    codex check --help          # Show help
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Tuple

# Add parent directory to path to import canon modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from canon.canon import (
    validate_sequence,
    SYMBOL_TO_INDEX,
    NAME_TO_INDEX,
    COLORS,
    ADJACENCY_RULE,
)
from canon.gray_event import GrayEvent, create_gray_events_from_violations


def parse_tokens(content: str) -> Tuple[List[int], List[GrayEvent]]:
    """
    Parse token content into color indices.

    Supports:
    - JSON array of indices: [0, 1, 2, 3]
    - JSON array of names: ["Black", "White", "Yellow"]
    - Symbol sequence: ⚫⚪🟡🟤
    - Name sequence (one per line): Black\\nWhite\\nYellow

    Returns:
        (indices, parse_errors)
    """
    content = content.strip()
    indices = []
    parse_errors = []

    # Try JSON first
    if content.startswith('['):
        try:
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError("JSON must be an array")

            for i, item in enumerate(data):
                if isinstance(item, int):
                    if 0 <= item <= 6:
                        indices.append(item)
                    else:
                        parse_errors.append(
                            GrayEvent.unknown_token(i, str(item))
                        )
                elif isinstance(item, str):
                    idx = NAME_TO_INDEX.get(item.lower())
                    if idx is not None:
                        indices.append(idx)
                    else:
                        parse_errors.append(
                            GrayEvent.unknown_token(i, item)
                        )
                else:
                    parse_errors.append(
                        GrayEvent.unknown_token(i, str(item))
                    )
            return indices, parse_errors
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # Try symbol sequence
    for i, char in enumerate(content):
        if char in SYMBOL_TO_INDEX:
            indices.append(SYMBOL_TO_INDEX[char])
        elif char.isspace():
            continue  # Skip whitespace
        else:
            # Try line-based name parsing
            break
    else:
        # Successfully parsed as symbols
        return indices, parse_errors

    # Try line-based name parsing
    if not indices:  # Only if symbol parsing didn't work
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            idx = NAME_TO_INDEX.get(line.lower())
            if idx is not None:
                indices.append(idx)
            else:
                parse_errors.append(
                    GrayEvent.unknown_token(i, line)
                )

    return indices, parse_errors


def format_summary(
    indices: List[int],
    is_valid: bool,
    violations: List[GrayEvent],
    verbose: bool = False
) -> str:
    """Format validation summary."""
    lines = []

    # Header
    status = "PASS ✓" if is_valid else "FAIL ✗"
    lines.append(f"Canon Check: {status}")
    lines.append("")

    # Sequence info
    lines.append(f"Sequence length: {len(indices)}")
    lines.append(f"Adjacency rule: {ADJACENCY_RULE}")
    lines.append("")

    # Violations
    if violations:
        lines.append(f"Gray Events: {len(violations)}")
        lines.append("")
        for event in violations:
            lines.append(f"  [{event.severity.upper()}] Index {event.index}")
            lines.append(f"    Type: {event.type}")
            if event.from_color is not None and event.to_color is not None:
                from_name = COLORS[event.from_color]["name"]
                to_name = COLORS[event.to_color]["name"]
                lines.append(f"    Transition: {from_name}({event.from_color}) → {to_name}({event.to_color})")
                lines.append(f"    Delta: {event.delta} (expected ±1 mod 7)")
            lines.append(f"    Reason: {event.reason}")
            lines.append("")
    else:
        lines.append("No Gray events detected.")
        lines.append("")

    # Verbose: show full sequence
    if verbose and indices:
        lines.append("Full sequence:")
        for i, idx in enumerate(indices):
            color = COLORS[idx]
            symbol = color["symbol"]
            name = color["name"]
            lines.append(f"  {i:3d}: {symbol} {name} ({idx})")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate token sequences against the 7-color adjacency law",
        epilog="""
Examples:
  codex check sequence.txt           # Check a file
  codex check sequence.json          # Check JSON array
  echo "⚫⚪🟡" | codex check --stdin  # Check from stdin
  codex check --stdin -v             # Verbose output
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="File containing token sequence (JSON, symbols, or names)"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read from stdin instead of file"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show full sequence and detailed output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output Gray events as JSON"
    )

    args = parser.parse_args()

    # Determine input source
    if args.stdin:
        content = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

    # Parse tokens
    indices, parse_errors = parse_tokens(content)

    if not indices:
        print("Error: No valid tokens found", file=sys.stderr)
        if parse_errors and args.verbose:
            print("\nParse errors:", file=sys.stderr)
            for err in parse_errors:
                print(f"  {err}", file=sys.stderr)
        sys.exit(1)

    # Validate sequence
    is_valid, violations = validate_sequence(indices)
    all_violations = parse_errors + create_gray_events_from_violations(violations)

    # Output
    if args.json:
        output = {
            "is_valid": is_valid and not parse_errors,
            "sequence_length": len(indices),
            "gray_events": [v.to_dict() for v in all_violations]
        }
        print(json.dumps(output, indent=2))
    else:
        summary = format_summary(indices, is_valid and not parse_errors, all_violations, args.verbose)
        print(summary)

    # Exit code
    sys.exit(0 if (is_valid and not parse_errors) else 1)


if __name__ == "__main__":
    main()
