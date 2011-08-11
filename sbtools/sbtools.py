from sboptparse import SBToolsOptionParser
from sbtool import SBToolError
import textwrap
import pkg_resources
import os
import sys

class SBToolsError(Exception):
    """An exception class for SBTools errors."""
    def __init__(self, value):
        self.value = str(value)
    def __str__(self):
        return self.value

class SubcommandConflictWarning(SBToolsError):
    """An exception class for subcommand conflicts."""
    def __init__(self, value):
        self.value = str(value)

class NameConflictWarning(SBToolsError):
    """An exception class for tool name conflicts."""
    def __init__(self, value):
        self.value = str(value)

class UnknownSubcommandError(SBToolsError):
    """
    An exception class for SBTools errors where an unknown subcommand
    is encountered. The exception should be raised with the unknown
    subcommand passed to it and an appropriate message is printed when
    the exception is handled.
    """
    def __init__(self, value):
        self.value = str(value)

class NoSubcommandError(SBToolsError):
    """
    An exception class that is raised when no subcommands are provided
    to sbtools.
    """
    def __init__(self):
        self.value = "No subcommand provided."

class SBTools:
    """
    SBTools is the main class in the SBTools framework. Its primary
    duties are to parse the command line, build the list of plug-ins
    that are available, provide querying methods for plug-ins, and
    call the appropriate plug-in to do the actual work when the script
    is run.
    """
    def __init__(self):
        self.parser = self.init_parser()
        self.tcmdlist = []
        self.cmdmap = {} # subcommand -> [plug-in module, builtin?]
        self.namemap = {} # toolname -> [plug-in module, builtin?]

    def init_parser(self):
        """Populate and return the parser object."""
        pkg_env = pkg_resources.Environment()
        versionstr = "%%prog %s" % (pkg_env[self.__module__.split('.')[0]][0].version)
        parser = SBToolsOptionParser(sbtools=self,
                                     usage="%prog <subcommand> [options] [args]",
                                     version=versionstr)

        parser.add_option("--verbose-load", action="callback", callback=self.verbose_load,
                          help="report actions and results when loading plug-ins")

        return parser

    def verbose_load(self, option, opt, value, parser):
        """
        Callback function for the '--verbose-load' option. This method
        resets member variables and then calls build_tool_list()
        telling it to print its actions.
        """
        self.tcmdlist = []
        self.cmdmap = {}
        self.namemap = {}
        self.build_tool_list(verbose_load=True)
        self.parser.exit()

    def parse_options(self):
        """Read the command-line arguments."""
        # Check if any subcommands are found. If a subcommand is
        # found, do not parse the arguments here.
        foundargs = False
        self.args = []
        for arg in sys.argv[1:]:
            if not arg.startswith(("--", "-")):
                foundargs = True
                self.args.append(arg)

        if not foundargs:
            (self.options, self.args) = self.parser.parse_args()

        # Make sure a subcommand was provided.
        if len(self.args) == 0:
            raise NoSubcommandError()

        # Check for unknown subcommands.
        if not self.cmdmap.has_key(self.args[0]):
            raise UnknownSubcommandError(self.args[0])

    def add_tool(self, cls, name, isbuiltin, subcommands):
        """
        Add the tool implemented in cls to the subcommand list and the
        plugin map. The tool is not added if any of the subcommands in
        the subcommands parameter list is already taken by a loaded
        plugin.
        """
        # Make sure none of the tool subcommands is already taken.
        for sc in subcommands:
            if self.cmdmap.has_key(sc):
                msg = textwrap.fill("WARNING: subcommand conflict with command '%s'; not loading %s plugin." % (sc, name), 78)
                raise SubcommandConflictWarning(msg)

        # Make sure another tool with the same name is not already
        # loaded.
        if self.namemap.has_key(name):
            msg = textwrap.fill("WARNING: name conflict with tool '%s' (subcommand '%s'); not loading %s plugin." % (name, subcommands[0], name), 78)
            raise NameConflictWarning(msg)

        # Everything checks out; add the tool.
        self.tcmdlist.append(subcommands)
        self.namemap[name] = [cls, isbuiltin]
        for sc in subcommands:
            self.cmdmap[sc] = [cls, isbuiltin]

    def build_tool_list(self, builtin_only=False, supp_plugin_locations=[], verbose_load=False):
        """
        Construct the list of available tools.

        This method differentiates between plug-ins that are builtin
        (i.e., are part of the framework) and plug-ins that are
        independently installed.

        If True, the builtin_only parameter does not load
        independently installed plug-ins. This was designed primarily
        for use by the unit tests to create a controlled environment.

        The supp_plugin_locations parameter is a list containing
        directories in which to search for independently installed
        plug-ins. This was designed primarily for use by the unit
        tests to create a controlled environment.
        """
        entrypoint = 'SBTools.plugins'

        # Get plugins.
        pkg_env = pkg_resources.Environment()
        for name in pkg_env:
            if verbose_load:
                sys.stdout.write("Found '%s' package..." % (name))
            # Determine if the plug-in is builtin.
            if name == self.__module__.split('.')[0]:
                isbuiltin = True
            else:
                isbuiltin = False
                if builtin_only:
                    # Skipped non-core packages (mostly for testing).
                    continue
            egg = pkg_env[name][0]
            egg.activate()
            for pdata in egg.get_entry_map(entrypoint):
                pdatasplit = pdata.split()
                if len(pdatasplit) == 0:
                    # Then no plug-in name (or subcommands) was
                    # provided.
                    if verbose_load:
                        sys.stdout.write("Un-named plug-in...cannot load...")
                    continue
                elif len(pdatasplit) == 1:
                    # Then no plug-in subcommands were provided.
                    if verbose_load:
                        sys.stdout.write("'%s' plug-in...no subcommands...cannot load..." % (pdatasplit[0]))
                    continue
                plugname = pdatasplit[0]
                subcommands = pdatasplit[1:]
                if verbose_load:
                    sys.stdout.write("'%s' plug-in..." % (plugname))

                entry_point = egg.get_entry_info(entrypoint, pdata)
                try:
                    cls = entry_point.load()
                except pkg_resources.VersionConflict, e:
                    if verbose_load:
                        sys.stdout.write("version conflict: %s..." % (e))
                    continue
                except pkg_resources.DistributionNotFound, e:
                    if verbose_load:
                        sys.stdout.write("missing dependency: %s..." % (e))
                    continue
                except ImportError, e:
                    if verbose_load:
                        sys.stdout.write("cannot import: %s..." % (e))
                    continue
                else:
                    if verbose_load:
                        sys.stdout.write("loaded...")

                # Populate the subcommand list and the plugin map.
                try:
                    self.add_tool(cls, plugname, isbuiltin, subcommands)
                except SubcommandConflictWarning, msg:
                    print msg
                except NameConflictWarning, msg:
                    print msg

            if verbose_load:
                print

        # Get plugins installed in the supp locations (this is mostly
        # to control the tests).
        for supp_loc in supp_plugin_locations:
            pkg_resources.working_set.add_entry(supp_loc)
            pkg_env = pkg_resources.Environment([supp_loc])
            for name in pkg_env:
                if verbose_load:
                    sys.stdout.write("Found '%s' package..." % (name))
                egg = pkg_env[name][0]
                eggname = str(egg).split()[0]
                egg.activate()
                for pdata in egg.get_entry_map(entrypoint):
                    pdatasplit = pdata.split()
                    if len(pdatasplit) == 0:
                        # Then no plug-in name (or subcommands) was
                        # provided.
                        if verbose_load:
                            sys.stdout.write("Un-named plug-in...cannot load...")
                        continue
                    elif len(pdatasplit) == 1:
                        # Then no plug-in subcommands were provided.
                        if verbose_load:
                            sys.stdout.write("'%s' plug-in...no subcommands...cannot load..." % (pdatasplit[0]))
                        continue
                    plugname = pdatasplit[0]
                    subcommands = pdatasplit[1:]
                    if verbose_load:
                        sys.stdout.write("'%s' plug-in..." % (plugname))
                    entry_point = egg.get_entry_info(entrypoint, pdata)

                    try:
                        cls = entry_point.load()
                    except pkg_resources.VersionConflict, e:
                        if verbose_load:
                            sys.stdout.write("version conflict: %s..." % (e))
                        continue
                    except pkg_resources.DistributionNotFound, e:
                        if verbose_load:
                            sys.stdout.write("missing dependency: %s..." % (e))
                        continue
                    except ImportError, e:
                        if verbose_load:
                            sys.stdout.write("cannot import: %s..." % (e))
                        continue
                    else:
                        if verbose_load:
                            sys.stdout.write("loaded...")

                    # Populate the subcommand list and the plugin map.
                    try:
                        self.add_tool(cls, eggname, False, subcommands)
                    except SubcommandConflictWarning, msg:
                        print msg
                    except NameConflictWarning, msg:
                        print msg

                if verbose_load:
                    print

        # Sort the subcommand list so that 'sbtools help' displays the
        # available subcommands in alphabetical order.
        self.tcmdlist.sort()

    def get_full_command(self, tool, lpad=""):
        """
        Returns a string containing the information that appears for a
        plugin in the available subcommands section of the help. The
        returned string has the contents of lpad prepended.

        Example: If the parameter tool is ['mytool', 'my', 'myt'] and
        lpad is "", then this method returns 'mytool (my, myt)'.
        """
        if len(tool) > 1:
            tsubstr = tool[1]
            for tsub in tool[2:]:
                tsubstr += ", %s" % (tsub)
            tstr = "%s (%s)" % (tool[0], tsubstr)
        else:
            tstr = tool[0]
        return "%s%s" % (lpad, tstr)

    def get_subcommands(self):
        """
        Return a formatted string that lists the subcommands available
        for the user to use.
        """
        lpad = " "*3
        tliststr = ""
        for tool in self.tcmdlist:
            tliststr += "%s\n" % (self.get_full_command(tool, lpad))
        return tliststr

    def get_about(self):
        """
        Return 'about' information for the SBTools package.
        """
        return "The SBTools package was developed at the National Renewable Energy Laboratory."

    def has_tool_by_name(self, tname):
        """Returns True if a tool with name tname is installed."""
        return self.namemap.has_key(tname)

    def has_tool_by_subcommand(self, sc):
        """Returns True if a tool with subcommand sc is installed."""
        return self.cmdmap.has_key(sc)

    def get_tool_by_name(self, tname):
        """
        Returns the module of the tool with name tname or None if no
        such tool exists.
        """
        if self.has_tool_by_name(tname):
            return self.namemap[tname][0]
        else:
            return None

    def get_tool_by_subcommand(self, sc):
        """
        Returns the module of the tool with subcommand sc or None if
        no such tool exists.
        """
        if self.has_tool_by_subcommand(sc):
            return self.cmdmap[sc][0]
        else:
            return None

    def is_tool_builtin_by_name(self, tname):
        """
        Returns True if the tool with name tname is a core plug-in,
        False if it is not, and None if no such tool exists.
        """
        if self.has_tool_by_name(tname):
            return self.namemap[tname][1]
        else:
            return None

    def is_tool_builtin_by_subcommand(self, sc):
        """
        Returns True if the tool with subcommand sc is a core plug-in,
        False if it is not, and None if no such tool exists.
        """
        if self.has_tool_by_subcommand(sc):
            return self.cmdmap[sc][1]
        else:
            return None

    def get_toolname_list(self):
        """Return a list containing the toolnames."""
        return self.namemap.keys()

    def get_tool_subcommand_list(self):
        """Return a list containing the tool subcommands."""
        return self.cmdmap.keys()

    def run(self):
        """Run the SBTools framework."""
        self.build_tool_list()
        try:
            self.parse_options()
        except UnknownSubcommandError, msg:
            print self.parser.get_unknown_argument_error(str(msg))
            self.parser.exit()
        except NoSubcommandError:
            print self.parser.get_help()
            self.parser.exit()

        # Run subcommand.
        cls = self.cmdmap[self.args[0]][0]
        tool = cls(self)
        try:
            tool.run()
        except NotImplementedError:
            print textwrap.fill("WARNING: '%s' subcommand does not implement run() method; not running tool." % (self.args[0]), 78)
        except UnknownSubcommandError, msg:
            print self.parser.get_unknown_argument_error(str(msg))
            self.parser.exit()
        except SBToolError, msg:
            if msg.is_wrapped():
                print msg
            else:
                print textwrap.fill("%s" % (str(msg)), 78)

def main():
    """Entry point for the sbtools script."""
    sbtools = SBTools()
    sbtools.run()
