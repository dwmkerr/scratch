#!/usr/bin/env python3

import sys
import os
import re
from typing import List, Tuple

# ANSI color codes
BLUE = "\033[1;34m"       # Bright blue for headings
BOLD_GREEN = "\033[1;32;1m"  # Bold green for key combos
CYAN = "\033[1;36m"       # Cyan for hidden count
RESET = "\033[0m"         # Reset color

# Default markdown file locations
DEFAULT_FILES = [os.path.expanduser("~/.flow.md"), "./flow.md"]

# --- Data Classes ---
class LineItem:
    """Represents a keybinding (e.g. '⌘ + Enter: Toggle iTerm fullscreen')."""
    def __init__(self, combo: str, description: str, checked: bool):
        self.combo = combo
        self.description = description
        self.checked = checked

    def __repr__(self):
        return f"LineItem(combo={self.combo}, checked={self.checked})"

class Section:
    """Represents a section in the markdown (e.g. 'Global', 'Vim')."""
    def __init__(self, title: str):
        self.title = title
        self.items: List[LineItem] = []
        self.hidden_count = 0

    def add_item(self, combo: str, description: str, checked: bool):
        """Adds a keybinding to the section."""
        if checked:
            self.items.append(LineItem(combo, description, checked))
        else:
            self.hidden_count += 1

    def __repr__(self):
        return f"Section(title={self.title}, items={self.items}, hidden={self.hidden_count})"

# --- Parsing Logic ---
def find_flow_md() -> str:
    """Finds the flow.md file from default locations or user-specified file."""
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help"]:
            print_help()
        elif os.path.exists(sys.argv[1]):
            return sys.argv[1]
        else:
            print(f"Error: Specified file '{sys.argv[1]}' not found.")
            sys.exit(1)
    
    for file in DEFAULT_FILES:
        if os.path.exists(file):
            return file

    print("Error: No flow.md file found.")
    sys.exit(1)

def parse_flow_md(file_path: str) -> List[Section]:
    """Parses flow.md and returns a list of structured sections."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sections: List[Section] = []
    current_section = None

    for line in lines:
        line = line.strip()

        # Headings (## Section)
        if line.startswith("## "):
            if current_section:
                sections.append(current_section)
            current_section = Section(line[3:])  # Remove '## ' from heading

        elif re.match(r"- \[.\] ", line):
            match = re.search(r"- \[(.)\] (.+?):\s*(.*)", line)
            if match and current_section:
                checked, combo, desc = match.groups()
                current_section.add_item(combo.strip(), desc.strip(), checked.lower() == "x")

        elif re.match(r"^\s{2,}[\w+]+ \+ ", line):
            parts = line.split(" - ", 1)
            if len(parts) == 2 and current_section:
                combo, desc = parts
                current_section.add_item(combo.strip(), desc.strip(), True)

    if current_section:
        sections.append(current_section)

    return sections

# --- Formatting Logic ---
def format_heading(title: str) -> str:
    """Formats a section heading in blue."""
    return f"{BLUE}{title}{RESET}"

def format_line_item(item: LineItem) -> str:
    """Formats a single keybinding."""
    return f"  {BOLD_GREEN}{item.combo}{RESET}: {item.description}"

def format_section(section: Section) -> str:
    """Formats an entire section, including heading, keybindings, and hidden count."""
    output = [format_heading(section.title)]
    output.extend(format_line_item(item) for item in section.items)
    if section.hidden_count > 0:
        output.append(f"  {CYAN}+{section.hidden_count} hidden{RESET}")
    return "\n".join(output)

# --- Printing ---
def print_sections(sections: List[Section]):
    """Prints all sections to the terminal."""
    print("\n".join(format_section(section) for section in sections))

def print_help():
    """Prints usage information."""
    print("Usage: flow [flowfile]")
    print("  Reads keyboard shortcut bindings from a markdown file.")
    print("  Default locations: ~/.flow.md or ./flow.md")
    print("\nOptions:")
    print("  -h, --help   Show this help message and exit.")
    sys.exit(0)

# --- Main Execution ---
def main():
    """Main function to load and display flow.md."""
    file_path = find_flow_md()
    sections = parse_flow_md(file_path)
    print_sections(sections)

if __name__ == "__main__":
    main()
