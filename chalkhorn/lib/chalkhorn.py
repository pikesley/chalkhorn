from pathlib import Path


class Chalkhorn:
    """Wrangle some Makefile help."""

    def __init__(self, filenames):
        """Construct."""
        self.filenames = filenames.split(" ")
        self.makefiles = list(map(Path, self.filenames))


class Target:
    """Parse a `make` target."""

    def __init__(self, content):
        """Construct."""
        self.parts = content.split(":")
        self.name = self.parts[0]
        self.category = None

    @property
    def help(self):
        """Extract the help text."""
        parts = self.parts[1].split("##")

        if len(parts) > 1:
            help_words = parts[1].strip().split(" ")
            if help_words[0].startswith("@"):
                self.category = help_words[0][1:]
                help_words = help_words[1:]

            return " ".join(help_words)

        return None
