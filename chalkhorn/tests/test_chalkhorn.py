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

    def test_target_picking(self):
        """Test it can extract the targets from a Makefile."""
        chalk = Chalkhorn("tests/fixtures/Makefile.no-help")
        self.assertEqual(
            list(map(lambda x: x.name, chalk.targets)),
            [
                "all",
                "style",
                "test",
                "install",
                "clean",
                "format",
                "isort",
                "black",
            ],
        )
        self.assertFalse(chalk.has_categories)

        chalk = Chalkhorn("tests/fixtures/Makefile.with-help")
        self.assertEqual(
            list(map(lambda x: x.help, chalk.targets)),
            [
                "run style, test, clean",
                "run the lint checks",
                "run the tests",
                None,
                "clean up the cruft",
                "format the code",
                None,
                None,
            ],
        )
        self.assertFalse(chalk.has_categories)

        chalk = Chalkhorn("tests/fixtures/Makefile.with-categorised-help")
        self.assertTrue(chalk.has_categories)


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

    def test_with_categories(self):
        """Test it parses help with a @category."""
        target = Target(
            "target-x:  ## @category-z this is the help for target-x"
        )
        self.assertEqual(target.name, "target-x")
        self.assertEqual(target.help, "this is the help for target-x")
        self.assertEqual(target.category, "category-z")

        target = Target("target-a: target-b target-c ## @foo some help text")
        self.assertEqual(target.name, "target-a")
        self.assertEqual(target.help, "some help text")
        self.assertEqual(target.category, "foo")
