import re
from pathlib import Path

from termcolor import colored as coloured

COLOURS = {
    "target": "cyan",
    "help": "green",
    "default": "magenta",
    "category": "yellow",
}
SPACER = 16
INDENT = 4


class Chalkhorn:
    """Wrangle some Makefile help."""

    def __init__(self, filenames):
        """Construct."""
        self.filenames = filenames
        self.makefiles = list(map(Path, self.filenames))
        self.targets = []

        target_matcher = re.compile(r"^[a-zA-Z0-9].*$")
        for file in self.makefiles:
            content = file.read_text().splitlines()
            for line in content:
                if target_matcher.match(line):
                    self.targets.append(Target(line))

        self.has_categories = any(list(map(lambda x: x.category, self.targets)))

    def __str__(self):
        """Display ourself as a string."""
        helped = []
        display = ""
        for target in self.targets:
            if target.has_help:
                helped.append(target)

        if not helped:
            return ""

        column_width = find_longest(list(map(lambda x: x.name, helped))) + SPACER
        helped[0].is_default = True

        if self.has_categories:
            cats = {}
            for target in helped:
                if not target.has_category:
                    target.category = "uncategorised"

                if target.category not in cats:
                    cats[target.category] = []

                cats[target.category].append(target)

            # move this to the end
            cats["uncategorised"] = cats.pop("uncategorised")

            for cat in cats:
                display += f"{coloured(cat, COLOURS['category'])}\n"
                display += print_targets(cats[cat], column_width, INDENT)

                display += "\n"

        else:
            display += print_targets(helped, column_width)

        return display


def print_targets(targets, width, indent=0):
    """Print a list of targets."""
    content = ""
    for target in targets:
        content += " " * indent
        content += target.print_name(width)
        content += f"{target.print_help()}\n"

    return content


def find_longest(strings):
    """Find the longest string in a list."""
    longest = 0
    for string in strings:
        if len(string) > longest:
            longest = len(string)

    return longest


class Target:
    """Parse a `make` target."""

    def __init__(self, content):
        """Construct."""
        self.parts = content.split(":")
        self.name = self.parts[0]
        self.help = None
        self.category = None
        self.is_default = False
        self.parse_line()

    @property
    def has_help(self):
        """Do we have `help`."""
        return self.help

    @property
    def has_category(self):
        """Do we have `category`."""
        return self.category

    def parse_line(self):
        """Parse the text beyond the `target` name."""
        parts = self.parts[1].split("##")

        if len(parts) > 1:
            help_words = parts[1].strip().split(" ")
            if help_words[0].startswith("@"):
                self.category = help_words[0][1:]
                help_words = help_words[1:]

            self.help = " ".join(help_words)

    def print_name(self, width):
        """Present our name."""
        return f"{coloured(self.name, COLOURS['target']):{width}}"

    def print_help(self):
        """Present out `help`."""
        content = coloured(self.help, COLOURS["help"])
        if self.is_default:
            content += " "
            content += coloured("(default)", COLOURS["default"])

        return content
