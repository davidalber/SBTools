from optparse import OptionParser
import textwrap
import pkg_resources
from sbtool import SBToolError

class SBToolsOptionParser(OptionParser):
    """
    This class overloads the OptionParser class to provide desired
    modified functionality for SBTools class.
    """
    def __init__(self, sbtools, usage, version):
        self.sbtools = sbtools
        OptionParser.__init__(self, usage=usage, version=version)

    def get_help(self):
        """
        Get help string for this parser.
        """
        helpstr = ""
        helpstr += self.get_usage()
        helpstr += "\n"
        helpstr += textwrap.fill(self.expand_prog_name("Type '%prog help <subcommand>' for help on a specific subcommand."), 78)
        helpstr += "\n"
        helpstr += textwrap.fill(self.expand_prog_name("Type '%prog --version' to see the program version."), 78)
        helpstr += "\n"
        helpstr += textwrap.fill(self.expand_prog_name("Type '%prog --verbose-load' to see the packages and plug-ins detected, and if plug-ins are successfully loaded."), 78)
        helpstr += "\n\n"

        helpstr += textwrap.fill("Subcommands consist of built-in subcommands and subcommands provided by installed plug-ins.", 78)
        helpstr += "\n\n"

        helpstr += "Available subcommands:\n"
        helpstr += self.sbtools.get_subcommands()

        return helpstr

    def print_help(self):
        """
        Print help string for this parser.
        """
        print self.get_help()

    def get_unknown_argument_error(self, arg):
        """
        Return an error message for the unknown argument arg.
        """
        return "%s\n%s" % (textwrap.fill("Unknown command: '%s'." % (arg)),
                           self.get_usage_command())

    def get_usage_command(self):
        """
        Return a string containing a message on how to get usage
        information.
        """
        return textwrap.fill(self.expand_prog_name("Type '%prog help' for usage information."), 78)

    def print_usage_command(self):
        """
        Print a message on how to get usage information.
        """
        print self.get_usage_command()


class SBToolOptionParser(OptionParser):
    """
    This class overloads the OptionParser class to provide desired
    modified functionality for tools derived from the SBTool class.
    """
    def __init__(self, tool, sbtools, usage, version=None, description=None):
        self.tool = tool
        self.sbtools = sbtools
        if version is None:
            pkg_env = pkg_resources.Environment()
            version = "%s %s" % (self.tool.get_name(), self.tool.get_version())

        OptionParser.__init__(self, usage=usage, version=version)
        if description is not None:
            self.set_description("%s: %s" % (self.tool.get_full_command_str(), description))

    def get_usage_command(self):
        """
        Returns the standard command to get help for this tool.
        """
        return textwrap.fill(self.sbtools.parser.expand_prog_name("Type '%prog help %s' for usage.") % (self.tool.get_command()), 78)

    def print_usage_command(self):
        """
        Print a message on how to get usage information.
        """
        print self.get_usage_command()

    def error(self, msg):
        """
        Print an error message. This is called when something goes
        wrong when parsing the command line. For example, doing
        'sbtools help --blah' leads to this method being called
        (assuming the plug-in parser does not contain a --blah
        option).
        """
        fullmsg = "Subcommand '%s': %s\n%s" % (self.tool.get_command(), msg,
                                               self.get_usage_command())
        raise SBToolError(fullmsg, True)

    def error_exit(self, msg):
        """
        Produce an error message using the provided message followed
        by a line containing the command for getting usage information
        on this tool.

        The resulting message is passed to an SBToolError exception as
        it is raised.

        This is the standard way of alerting the user and exiting when
        a tool is not used correctly.
        """
        wrappedmsg = textwrap.fill(msg, 78)
        fullmsg = "%s\n%s" % (wrappedmsg, self.get_usage_command())
        raise SBToolError(fullmsg, True)
