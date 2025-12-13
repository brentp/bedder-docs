#!/usr/bin/env python3
"""
Test script to extract and run examples from intersection.md
Uses -o flag to write output to file (avoids TTY issues).
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

def extract_examples(md_path: Path) -> list[dict]:
    """Extract command/output pairs from markdown file."""
    content = md_path.read_text()
    
    examples = []
    
    # Find all code blocks that start with $ bedder
    pattern = r'```\s*\n\$ (bedder [^\n]+)\n(.*?)```'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        command = match.group(1).strip()
        output = match.group(2).strip()
        
        # Skip if the command has a trailing backtick (malformed in the doc)
        if command.endswith('`'):
            command = command[:-1]
        
        examples.append({
            'command': command,
            'expected_output': output
        })
    
    return examples


def run_example(example: dict, bedder_path: str, test_num: int, tmpdir: Path) -> tuple[bool, str, str, str]:
    """Run a single example and check output."""
    command = example['command']
    expected = example['expected_output']
    
    # Replace 'bedder' with actual path
    full_command = command.replace('bedder', bedder_path, 1)
    
    # Use unique output file for each test
    outfile = tmpdir / f"output_{test_num}.bed"
    if ' -o ' not in full_command:
        full_command += f" -o {outfile}"
    
    try:
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if outfile.exists():
            actual = outfile.read_text().strip()
        else:
            actual = ""
        
        # Normalize whitespace for comparison (tabs vs spaces)
        def normalize(s):
            return '\n'.join('\t'.join(line.split()) for line in s.strip().split('\n'))
        
        if normalize(actual) == normalize(expected):
            return True, "", actual, result.stderr
        else:
            return False, "Output mismatch", actual, result.stderr
    
    except Exception as e:
        return False, f"Error: {e}", "", ""


def main():
    bedder_path = "./bedder"
    md_path = Path(__file__).parent.parent / "docs" / "subcommands" / "intersection.md"
    
    if not md_path.exists():
        print(f"ERROR: Markdown file not found: {md_path}")
        sys.exit(1)
    
    if not Path(bedder_path).exists():
        print(f"ERROR: bedder binary not found at: {bedder_path}")
        sys.exit(1)
    
    examples = extract_examples(md_path)
    
    print(f"Found {len(examples)} examples to test\n")
    print("="*80)
    
    passed = 0
    failed = 0
    failures = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        for i, example in enumerate(examples, 1):
            cmd = example['command']
            print(f"\nTest {i}:")
            print(f"  $ {cmd}")
            
            success, error, actual, stderr = run_example(example, bedder_path, i, tmpdir)
            
            if success:
                print(f"  ✓ PASSED")
                passed += 1
            else:
                print(f"  ✗ FAILED")
                failed += 1
                
                # Collect failure details
                err_lines = [l for l in stderr.split('\n') if 'error:' in l.lower()]
                failures.append({
                    'test': i,
                    'command': cmd,
                    'expected': example['expected_output'],
                    'actual': actual,
                    'errors': err_lines
                })
            print("-"*80)
    
    print(f"\n{'='*80}")
    print(f"Results: {passed} passed, {failed} failed out of {len(examples)} tests")
    
    if failures:
        print("\n" + "="*80)
        print("FAILURE DETAILS:")
        print("="*80)
        for f in failures:
            print(f"\nTest {f['test']}:")
            print(f"  Command: $ {f['command']}")
            if f['errors']:
                for e in f['errors']:
                    print(f"  ERROR: {e}")
            print(f"  Expected:")
            for line in f['expected'].split('\n'):
                print(f"    {line}")
            print(f"  Got:")
            for line in (f['actual'].split('\n') if f['actual'] else ['(empty)']):
                print(f"    {line}")
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
