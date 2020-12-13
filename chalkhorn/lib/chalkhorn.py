import re
from pathlib import Path

from termcolor import colored as coloured

COLOURS = {"target": "cyan", "help": "green", "default": "magenta"}


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
        for target in self.targets:
            if target.has_help:
                helped.append(target)

        is_first = True
        display = ""
        column_width = find_longest(list(map(lambda x: x.name, helped))) + 16
        for target in helped:
            display += f"{coloured(target.name, COLOURS['target']):{column_width}}"
            display += f"{coloured(target.help, COLOURS['help'])}"
            if is_first:
                display += f" {coloured('(default)', COLOURS['default'])}"
                is_first = False
            display += "\n"

        return display


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
        self.parse_line()

    @property
    def has_help(self):
        """Do we have `help`."""
        return self.help

    def parse_line(self):
        """Parse the text beyond the `target` name."""
        parts = self.parts[1].split("##")

        if len(parts) > 1:
            help_words = parts[1].strip().split(" ")
            if help_words[0].startswith("@"):
                self.category = help_words[0][1:]
                help_words = help_words[1:]

            self.help = " ".join(help_words)
