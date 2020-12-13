import re
from pathlib import Path


class Chalkhorn:
    """Wrangle some Makefile help."""

    def __init__(self, filenames):
        """Construct."""
        self.filenames = filenames.split(" ")
        self.makefiles = list(map(Path, self.filenames))
        self.targets = []

        target_matcher = re.compile(r"^[a-zA-Z0-9].*$")
        for file in self.makefiles:
            content = file.read_text().splitlines()
            for line in content:
                if target_matcher.match(line):
                    self.targets.append(Target(line))

        self.has_categories = any(list(map(lambda x: x.category, self.targets)))


class Target:
    """Parse a `make` target."""

    def __init__(self, content):
        """Construct."""
        self.parts = content.split(":")
        self.name = self.parts[0]
        self.help = None
        self.category = None
        self.parse_line()

    def parse_line(self):
        """Parse the text beyond the `target` name."""
        parts = self.parts[1].split("##")

        if len(parts) > 1:
            help_words = parts[1].strip().split(" ")
            if help_words[0].startswith("@"):
                self.category = help_words[0][1:]
                help_words = help_words[1:]

            self.help = " ".join(help_words)
