from sbtool import SBTool
from sbtools import UnknownSubcommandError
from sboptparse import SBToolOptionParser
import os
import textwrap
import pkg_resources

class Help(SBTool):
    """The Help plug-in."""
    def __init__(self, sbtools):
        self.sbtools = sbtools
        self.parser = self.init_parser()

    def init_parser(self):
        """Populate and return the parser object."""
        usage = "%s [subcommand]" % (self.get_command())
        description = "Provide usage information on the SBTools core package or a plug-in when a subcommand is provided."
        return SBToolOptionParser(self, self.sbtools, usage, description=description)

    def get_about(self):
        """Return this tool's 'about' information."""
        return "The Help tool is a core component of the SBTools package."

    def print_help(self):
        """Print this tool's help information."""
        self.parser.print_help()

    def run(self):
        """Run the tool."""
        (self.options, self.args) = self.parser.parse_args()
        if len(self.args) == 1:
            self.sbtools.parser.print_help()
        else:
            # Get help on the specified subcommand.
            sc = self.args[1]
            cls = self.sbtools.get_tool_by_subcommand(sc)
            if cls is None:
                # An unrecognized subcommand was used.
                raise UnknownSubcommandError(sc)
            tool = cls(self.sbtools)
            try:
                tool.print_help()
            except NotImplementedError:
                print textwrap.fill("No help available on %s tool." % (tool.get_name()), 78)

class About(SBTool):
    """The About plug-in."""
    def __init__(self, sbtools):
        self.sbtools = sbtools
        self.parser = self.init_parser()

    def init_parser(self):
        """Populate and return the parser object."""
        usage = "%s [subcommand]" % (self.get_command())
        description = "Provide 'about' information on the SBTools core package or a plugin when a subcommand is provided."
        return SBToolOptionParser(self, self.sbtools, usage, description=description)

    def get_about(self):
        """Return this tool's 'about' information."""
        return "The About tool is a core component of the SBTools package."

    def print_help(self):
        """Print this tool's help information."""
        self.parser.print_help()

    def run(self):
        """Run the tool."""
        (self.options, self.args) = self.parser.parse_args()
        if len(self.args) == 1:
            # Get 'about' information for the SBTools framework.
            tool = self.sbtools
        else:
            # Get 'about' information on the specified subcommand.
            sc = self.args[1]
            cls = self.sbtools.get_tool_by_subcommand(sc)
            if cls is None:
                # An unrecognized subcommand was used.
                raise UnknownSubcommandError(sc)
            tool = cls(self.sbtools)
        try:
            aboutstr = tool.get_about()
            lines = aboutstr.splitlines()
            for line in lines:
                print textwrap.fill(line, 78)
        except NotImplementedError:
            print "No 'about' information available."

class File(SBTool):
    """The File plug-in."""
    def __init__(self, sbtools):
        self.sbtools = sbtools
        self.parser = self.init_parser()

    def init_parser(self):
        """Populate and return the parser object."""
        usage = "%s SUBCOMMAND" % (self.get_command())
        description = "Print the path and filename of the specified subcommand's plugin."
        return SBToolOptionParser(self, self.sbtools, usage, description=description)

    def get_about(self):
        """Return this tool's 'about' information."""
        return "The File tool is a core component of the SBTools package."

    def print_help(self):
        """Print this tool's help information."""
        self.parser.print_help()

    def run(self):
        """Run the tool."""
        (self.options, self.args) = self.parser.parse_args()
        if len(self.args) != 2:
            self.parser.error_exit("Missing subcommand argument.")
        else:
            # Get filename information on the specified subcommand.
            sc = self.args[1]
            cls = self.sbtools.get_tool_by_subcommand(sc)
            if cls is None:
                # An unrecognized subcommand was used.
                raise UnknownSubcommandError(sc)
            isbuiltin = self.sbtools.is_tool_builtin_by_subcommand(sc)
            tool = cls(self.sbtools)
            if isbuiltin:
                print "%s is a builtin tool." % (tool.get_name())
            else:
                pkg_env = pkg_resources.Environment()
                egg = pkg_env[tool.__module__.split('.')[0]][0]
                print egg.location
