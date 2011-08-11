import pkg_resources

class SBToolError(Exception):
    """An exception class for unsuccessful tool runs."""
    def __init__(self, value, prewrapped=False):
        self.value = str(value)
        self.wrapped = prewrapped
    def __str__(self):
        return self.value
    def is_wrapped(self):
        return self.wrapped

class EntryPointError(SBToolError):
    """
    An exception class raised by the get_full_epldata() method when a
    plug-in does not have a corresponding entry point. This should
    only occur when creating these objects manually (such as through
    the Python prompt).
    """
    def __init__(self, value):
        self.value = str(value)
        self.wrapped = False

class SBTool:
    """
    Parent class for all tools developed to run with sbtools.
    """
    def __init__(self, sbtools):
        self.sbtools = sbtools

    def get_command(self):
        """
        Returns the primary subcommand for a derived class, which is
        extracted from the entry point in the setup.py file.
        """
        pdata = self.get_full_epldata()
        pdatasplit = pdata.split()
        return pdatasplit[1]

    def get_alt_commands(self):
        """
        Returns the alternate subcommands for a derived class, which
        is extracted from the entry point in the setup.py file. If no
        alternate subcommands are defined, then an empty list is
        returned.
        """
        pdata = self.get_full_epldata()
        pdatasplit = pdata.split()
        return pdatasplit[2:]

    def get_full_command_str(self):
        """
        Returns the complete command string of the tool, which is the
        same as what appears for the tool in the available subcommands
        list when 'sbtools help' is run.
        """
        return self.sbtools.get_full_command([self.get_command()] +
                                             self.get_alt_commands())

    def get_about(self):
        """
        In a derived-class implementation, this method returns a
        string containing 'about' information for the tool.

        About information may include authors, institution, copyright,
        license information, website URL, and additional information.

        If this method is not overloaded, then when about information
        is requested, the response is that no about information is
        available for the specified tool.
        """
        raise NotImplementedError

    def get_name(self):
        """
        Return the name of this plug-in, as defined in the setup.py
        file.
        """
        pdata = self.get_full_epldata()
        pdatasplit = pdata.split()
        return pdatasplit[0]

    def get_full_epldata(self):
        """
        Return the contents of the left-hand side of the entry point
        for this plug-in.

        This works by checking all SBTools.plugins entry points and
        returning the name of the one whose entrypoint the same as
        this object's class.
        """
        # Try returning the epldata that was already found. If this
        # throws an AttributeError, then the epldata has not yet been
        # extracted.
        try:
            return self.epldata
        except AttributeError:
            pass

        entrypoint = 'SBTools.plugins'
        pkg_env = pkg_resources.Environment()
        egg = pkg_env[self.__module__.split('.')[0]][0]
        for pdata in egg.get_entry_map(entrypoint):
            entry_point = egg.get_entry_info(entrypoint, pdata)
            cls = entry_point.load()
            if isinstance(self, cls):
                self.epldata = pdata
                return self.epldata

        # This should not happen for users, but may happen during
        # tests, for instance with a SBTool object or a subclassed
        # object that does not have a setup.py file.
        raise EntryPointError("This object does not have a corresponding entry point.")

    def get_version(self):
        """
        Return the version string of this package, as defined in the
        setup.py file.
        """
        pkg_env = pkg_resources.Environment()
        return pkg_env[self.__module__.split('.')[0]][0].version

    def print_help(self):
        """
        In a derived-class implementation, this method prints help
        information for the tool.

        If this method is not overloaded, then when help on the tool
        is requested, the response is that no help is available.
        """
        raise NotImplementedError

    def run(self):
        """
        In a derived-class tool implementation, this method must be
        overloaded and run the tool when called.
        """
        raise NotImplementedError
