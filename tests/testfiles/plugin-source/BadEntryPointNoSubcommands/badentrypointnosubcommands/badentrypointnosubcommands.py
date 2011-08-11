from sbtools.sbtools import UnknownSubcommandError
from sbtools.sbtool import SBTool
from sbtools.sboptparse import SBToolOptionParser
import textwrap

class BadEntryPointNoSubcommands(SBTool):
    """BadEntryPointNoSubcommands test plug-in."""
    def __init__(self, sbtools):
        self.sbtools = sbtools
        self.command = "bad-entry"
        self.altcmds = ['be']
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
        return """This test plug-in exists to verify that SBTools behaves correctly when it encounters a plug-in that has an incorrectly defined entry point."""

    def print_help(self):
        """Print this tool's help information."""
        self.parser.print_help()

    def run(self):
        """Run the tool."""
        (self.options, self.args) = self.parser.parse_args()
