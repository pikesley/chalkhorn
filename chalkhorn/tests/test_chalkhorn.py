from pathlib import PosixPath
from unittest import TestCase

from lib.chalkhorn import Chalkhorn, Target


class TestChalkhorn(TestCase):
    """Test the Chalkhorn."""

    def test_constructor(self):
        """Test it gets the right data."""
        chalk = Chalkhorn(
            "tests/fixtures/Makefile.foo tests/fixtures/Makefile.bar"
        )
        self.assertEqual(
            chalk.filenames,
            ["tests/fixtures/Makefile.foo", "tests/fixtures/Makefile.bar"],
        )
        self.assertEqual(
            chalk.makefiles,
            [
                PosixPath("tests/fixtures/Makefile.foo"),
                PosixPath("tests/fixtures/Makefile.bar"),
            ],
        )


class TestTarget(TestCase):
    """Test the Target parser."""

    def test_parsing(self):
        """Test it parses target strings."""
        target = Target("foo:")
        self.assertEqual(target.name, "foo")
        self.assertFalse(target.help)

        target = Target("two-words:")
        self.assertEqual(target.name, "two-words")
        self.assertFalse(target.help)

        target = Target("some-target: other-target")
        self.assertEqual(target.name, "some-target")
        self.assertFalse(target.help)

        target = Target("target-with-help:  ## this is the help text")
        self.assertEqual(target.name, "target-with-help")
        self.assertEqual(target.help, "this is the help text")

        target = Target("target-a: target-b target-c ## help for target-a")
        self.assertEqual(target.name, "target-a")
        self.assertEqual(target.help, "help for target-a")
