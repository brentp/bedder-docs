#!/usr/bin/env python3
"""
Convert BED files to Mermaid Gantt diagram for visualizing genomic intervals.

Usage:
    python bed_to_mermaid.py file1.bed file2.bed file3.bed
    python bed_to_mermaid.py *.bed
    cat input.bed | python bed_to_mermaid.py
"""

import sys
import argparse
from typing import List, Tuple, Optional

def parse_bed_line(line: str) -> Tuple[str, int, int]:
    """Parse a BED format line and return chromosome, start, end."""
    parts = line.strip().split('\t' if '\t' in line else ' ')
    if len(parts) < 3:
        raise ValueError(f"Invalid BED line: {line}")
    
    chrom = parts[0]
    start = int(parts[1])
    end = int(parts[2])
    
    return chrom, start, end

def read_bed_file(file_path: Optional[str] = None) -> List[Tuple[str, int, int]]:
    """Read BED file from file path or stdin."""
    intervals = []
    
    if file_path and file_path != '-':
        with open(file_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        try:
            intervals.append(parse_bed_line(line))
        except ValueError as e:
            print(f"Warning: Skipping line {line_num}: {e}", file=sys.stderr)
    
    return intervals

def generate_mermaid_gantt(file_data: dict) -> str:
    """Generate Mermaid Gantt diagram from multiple BED files."""
    if not file_data:
        return "gantt\n    title Genomic Intervals\n    dateFormat X\n    axisFormat %s\n"
    
    # Find the overall coordinate range for scaling
    all_coords = []
    for intervals in file_data.values():
        for _, start, end in intervals:
            all_coords.extend([start, end])
    
    if not all_coords:
        return "gantt\n    title Genomic Intervals\n    dateFormat X\n    axisFormat %s\n"
    
    min_coord = min(all_coords)
    
    # Start building the Mermaid gantt with styling for better visibility
    mermaid_lines = [
        "%%{init: {'theme':'base', 'themeVariables': {'primaryTextColor': '#ffffff', 'tertiaryTextColor': '#ffffff', 'sectionBkgColor': '#ffffff', 'altSectionBkgColor': '#ffffff', 'gridColor': '#777777', 'section0': '#ffffff', 'section1': '#ffffff', 'section2': '#ffffff', 'section3': '#ffffff', 'taskTextColor': '#ffffff', 'altTaskTextColor': '#ffffff', 'textColor': '#ffffff'}}}%%",
        "gantt",
        #"    title Genomic Intervals",
        "    dateFormat X",
        "    axisFormat %s",
        "",
    ]
    
    # Add each file as a section
    for file_idx, (filename, intervals) in enumerate(file_data.items()):
        if not intervals:
            continue
            
        # Use filename without extension as section name
        section_name = filename.replace('.bed', '').replace('.BED', '')
        mermaid_lines.append(f"    section {section_name}")
        
        # Sort all intervals by start position
        sorted_intervals = sorted(intervals, key=lambda x: (x[0], x[1]))  # sort by chrom, then start
        
        # Add all intervals to the same section - Mermaid will handle overlaps automatically
        for chrom, start, end in sorted_intervals:
            interval_name = f"{chrom}_{start}-{end}"
            rel_start = start - min_coord
            rel_end = end - min_coord
            mermaid_lines.append(f"    {interval_name} :{rel_start}, {rel_end}")
    
    return "\n".join(mermaid_lines)



def main():
    parser = argparse.ArgumentParser(
        description="Convert BED files to Mermaid Gantt diagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python bed_to_mermaid.py file1.bed file2.bed
    python bed_to_mermaid.py *.bed
    cat intervals.bed | python bed_to_mermaid.py
    echo -e "chr1\\t8\\t12\\nchr1\\t14\\t22\\nchr1\\t20\\t30" | python bed_to_mermaid.py
        """
    )
    
    parser.add_argument(
        'input_files', 
        nargs='*',
        help='BED files to process (use stdin if none provided)'
    )
    
    args = parser.parse_args()
    
    try:
        file_data = {}
        
        if not args.input_files:
            # Read from stdin
            intervals = read_bed_file(None)
            if not intervals:
                print("Warning: No valid intervals found in stdin", file=sys.stderr)
                return 1
            file_data['stdin'] = intervals
        else:
            # Read from multiple files                
            for file_path in args.input_files:
                try:
                    intervals = read_bed_file(file_path)
                    if intervals:
                        # Use just the filename for the key
                        import os
                        filename = os.path.basename(file_path)
                        file_data[filename] = intervals
                    else:
                        print(f"Warning: No valid intervals found in {file_path}", file=sys.stderr)
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found", file=sys.stderr)
                    return 1
        
        if not file_data:
            print("Error: No valid data found in any input", file=sys.stderr)
            return 1
        
        mermaid_diagram = generate_mermaid_gantt(file_data)
        print(mermaid_diagram)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 