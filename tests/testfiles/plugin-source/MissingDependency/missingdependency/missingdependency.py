from sbtools.sbtools import UnknownSubcommandError
from sbtools.sbtool import SBTool
from sbtools.sboptparse import SBToolOptionParser
import textwrap

class MissingDependency(SBTool):
    """MissingDependency test plug-in."""
    def __init__(self, sbtools):
        self.sbtools = sbtools
        self.command = "missing-dependency"
        self.altcmds = ['md']
        self.parser = self.init_parser()

    def init_parser(self):
        """Populate and return the parser object."""
        usage = "%s [options] [subcommand]" % (self.command)
        description = "An SBTools test plug-in."

        parser = SBToolOptionParser(self, self.sbtools, usage, description=description)
        return parser

    def get_command(self):
        """Return the primary subcommand of this tool."""
        return self.command

    def get_alt_commands(self):
        """
        Return the alternate subcommands of this tool.
        """
        return self.altcmds

    def get_about(self):
        """Return this tool's 'about' information."""
        return """This test plug-in exists to verify that SBTools behaves correctly when it attempts to load a plug-in for which some dependencies are missing."""

    def print_help(self):
        """Print this tool's help information."""
        self.parser.print_help()

    def run(self):
        """Run the tool."""
        (self.options, self.args) = self.parser.parse_args()
