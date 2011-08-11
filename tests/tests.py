import unittest
import sys
import textwrap
from sbtools import sbtools
from sbtools.sbtools import SBTools
from sbtools.sbtool import SBTool, SBToolError, EntryPointError
from sbtools.builtins import Help, About, File
from sbtools.sboptparse import SBToolsOptionParser, SBToolOptionParser

class TestSBToolsOptionParserMethods(unittest.TestCase):
    """
    Unit tests for the SBToolsOptionParser class.
    """
    def setUp(self):
        self.sbtools = SBTools()
        self.parser = self.sbtools.parser

    def test001_init(self):
        self.assertEqual(self.parser.sbtools, self.sbtools)

    def test002_get_help(self):
        helpstr = self.parser.get_help()
        exptstr = """Usage: sbtools <subcommand> [options] [args]

Type 'sbtools help <subcommand>' for help on a specific subcommand.
Type 'sbtools --version' to see the program version.
Type 'sbtools --verbose-load' to see the packages and plug-ins detected, and
if plug-ins are successfully loaded.

Subcommands consist of built-in subcommands and subcommands provided by
installed plug-ins.

Available subcommands:
%s""" % (self.sbtools.get_subcommands())
        self.assertEqual(helpstr, exptstr)

    def test003_get_unknown_argument_error(self):
        errmsg = self.parser.get_unknown_argument_error('unknown-sc')
        self.assertEqual(errmsg, "Unknown command: 'unknown-sc'.\nType 'sbtools help' for usage information.")

    def test004_get_usage_command(self):
        usagecomm = self.parser.get_usage_command()
        self.assertEqual(usagecomm, "Type 'sbtools help' for usage information.")

class TestSBToolOptionParserMethods(unittest.TestCase):
    """
    Unit tests for the SBToolOptionParser class.
    """
    def setUp(self):
        class TestTool1(SBTool):
            def __init__(self, sbtools):
                self.sbtools = sbtools

            def get_command(self):
                return "TestTool1"

            def get_alt_commands(self):
                return []

        self.sbtools = SBTools()
        self.tool = TestTool1(self.sbtools)
        self.usage = "TestTool1 [options]"
        self.version = "0.1"
        self.description = "The test tool does something."
        self.parser = SBToolOptionParser(self.tool, self.sbtools, self.usage,
                                         self.version, self.description)

    def test001_get_usage_command(self):
        usagecomm = self.parser.get_usage_command()
        self.assertEqual(usagecomm, "Type 'sbtools help %s' for usage." % (self.tool.get_command()))

    def test002_error(self):
        # Make sure the expected exception is raised.
        self.assertRaises(SBToolError, self.parser.error, "unknown option --blah")

        # Make sure the expecte message is passed with the exception.
        try:
            self.parser.error("unknown option --blah")
        except SBToolError, msg:
            self.assertEqual(str(msg), "Subcommand '%s': unknown option --blah\n%s" % (self.tool.get_command(), self.parser.get_usage_command()))

    def test003_error_exit(self):
        # Make sure the expected exception is raised.
        self.assertRaises(SBToolError, self.parser.error_exit, "Filename not provided.")

        # Make sure the expecte message is passed with the exception.
        try:
            self.parser.error_exit("Filename not provided.")
        except SBToolError, msg:
            self.assertEqual(str(msg), "Filename not provided.\n%s" % (self.parser.get_usage_command()))

class TestHelpMethods(unittest.TestCase):
    """
    Unit tests for the Help core plugin.
    """
    def setUp(self):
        self.sbtools = SBTools()
        self.help = Help(self.sbtools)

    def test001_init(self):
        self.assertEqual(self.help.sbtools, self.sbtools)

    def test002_init_parser(self):
        self.assertEqual(self.help.parser.get_usage().strip(), "Usage: help [subcommand]")
        self.assertEqual(self.help.parser.get_description(), "help (h, ?): Provide usage information on the SBTools core package or a plug-in when a subcommand is provided.")

    def test003_get_command(self):
        self.assertEqual(self.help.get_command(), "help")

    def test004_get_alt_commands(self):
        self.assertEqual(self.help.get_alt_commands(), ['h', '?'])

    def test005_get_full_command_str(self):
        self.assertEqual(self.help.get_full_command_str(), "help (h, ?)")

    def test006_get_about(self):
        self.assertEqual(self.help.get_about(), "The Help tool is a core component of the SBTools package.")

    def test007_run_unknown_subcommand(self):
        argv_saved = sys.argv
        sys.argv = ['sbtools', 'help', 'unknown-sc']
        # Make sure the expected exception is raised.
        self.assertRaises(sbtools.UnknownSubcommandError, self.help.run)

        # Make sure the expected message is included with the
        # exception.
        try:
            self.help.run()
        except sbtools.UnknownSubcommandError, msg:
            self.assertEqual(str(msg), "unknown-sc")

        sys.argv = argv_saved

class TestAboutMethods(unittest.TestCase):
    """
    Unit tests for the About core plugin.
    """
    def setUp(self):
        self.sbtools = SBTools()
        self.about = About(self.sbtools)

    def test001_init(self):
        self.assertEqual(self.about.sbtools, self.sbtools)

    def test002_init_parser(self):
        self.assertEqual(self.about.parser.get_usage().strip(), "Usage: about [subcommand]")
        self.assertEqual(self.about.parser.get_description(), "about: Provide 'about' information on the SBTools core package or a plugin when a subcommand is provided.")

    def test003_get_command(self):
        self.assertEqual(self.about.get_command(), "about")

    def test004_get_alt_commands(self):
        self.assertEqual(self.about.get_alt_commands(), [])

    def test005_get_full_command_str(self):
        self.assertEqual(self.about.get_full_command_str(), "about")

    def test006_get_about(self):
        self.assertEqual(self.about.get_about(), "The About tool is a core component of the SBTools package.")

    def test007_run_unknown_subcommand(self):
        argv_saved = sys.argv
        sys.argv = ['sbtools', 'about', 'unknown-sc']

        # Make sure the expected exception is raised.
        self.assertRaises(sbtools.UnknownSubcommandError, self.about.run)

        # Make sure the expected message is included with the
        # exception.
        try:
            self.about.run()
        except sbtools.UnknownSubcommandError, msg:
            self.assertEqual(str(msg), "unknown-sc")

        sys.argv = argv_saved

class TestFileMethods(unittest.TestCase):
    """
    Unit tests for the About core plugin.
    """
    def setUp(self):
        self.sbtools = SBTools()
        self.file = File(self.sbtools)

    def test001_init(self):
        self.assertEqual(self.file.sbtools, self.sbtools)

    def test002_init_parser(self):
        self.assertEqual(self.file.parser.get_usage().strip(), "Usage: file SUBCOMMAND")
        self.assertEqual(self.file.parser.get_description(), "file: Print the path and filename of the specified subcommand's plugin.")

    def test003_get_command(self):
        self.assertEqual(self.file.get_command(), "file")

    def test004_get_alt_commands(self):
        self.assertEqual(self.file.get_alt_commands(), [])

    def test005_get_full_command_str(self):
        self.assertEqual(self.file.get_full_command_str(), "file")

    def test005_get_about(self):
        self.assertEqual(self.file.get_about(), "The File tool is a core component of the SBTools package.")

    def test006_run_missing_subcommand(self):
        saved_argv = sys.argv
        sys.argv = ['sbtools', 'file']
        # Make sure the expected exception is thrown.
        self.assertRaises(SBToolError, self.file.run)

        # Make sure the expected message is attached to the exception.
        try:
            self.file.run()
        except SBToolError, msg:
            self.assertEqual(str(msg), "Missing subcommand argument.\nType 'sbtools help file' for usage.")

        sys.argv = saved_argv

    def test007_run_unknown_subcommand(self):
        argv_saved = sys.argv
        sys.argv = ['sbtools', 'file', 'unknown-sc']

        # Make sure the expected exception is raised.
        self.assertRaises(sbtools.UnknownSubcommandError, self.file.run)

        # Make sure the expected message is included with the
        # exception.
        try:
            self.file.run()
        except sbtools.UnknownSubcommandError, msg:
            self.assertEqual(str(msg), "unknown-sc")

        sys.argv = argv_saved

class TestSBToolMethods(unittest.TestCase):
    """
    Unit tests for the SBTool class.
    """
    def setUp(self):
        self.sbtools = SBTools()
        self.sbtool = SBTool(self.sbtools)

    def test001_init(self):
        self.assertEqual(self.sbtool.sbtools, self.sbtools)

    def test002_get_command(self):
        self.assertRaises(EntryPointError, self.sbtool.get_command)

    def test003_get_alt_commands(self):
        self.assertRaises(EntryPointError, self.sbtool.get_alt_commands)

    def test004_get_full_command_str(self):
        self.assertRaises(EntryPointError, self.sbtool.get_full_command_str)

    def test005_get_about(self):
        self.assertRaises(NotImplementedError, self.sbtool.get_about)

    def test006_get_name(self):
        self.assertRaises(EntryPointError, self.sbtool.get_name)

    def test007_get_full_epldata(self):
        self.assertRaises(EntryPointError, self.sbtool.get_full_epldata)

    def test008_get_version(self):
        self.assertEqual(self.sbtool.get_version(), "0.5")

    def test009_print_help(self):
        self.assertRaises(NotImplementedError, self.sbtool.print_help)

    def test010_run(self):
        self.assertRaises(NotImplementedError, self.sbtool.run)        

class TestSBToolsMethods(unittest.TestCase):
    """
    Unit tests for the SBTools class.
    """
    def setUp(self):
        self.sbtools = SBTools()

    def test001_init(self):
        self.assertEqual(self.sbtools.tcmdlist, [])
        self.assertEqual(self.sbtools.cmdmap, {})
        self.assertEqual(self.sbtools.namemap, {})

    def test002_init_parser(self):
        self.assertEqual(self.sbtools.parser.get_version(), "sbtools 0.5")
        self.assertEqual(self.sbtools.parser.get_usage().strip(), "Usage: sbtools <subcommand> [options] [args]")

    def test003_parse_options_no_subcommand(self):
        saved_argv = sys.argv
        sys.argv = ['sbtools']
        # Make sure the expected exception is raised.
        self.assertRaises(sbtools.NoSubcommandError, self.sbtools.parse_options)
        sys.argv = saved_argv

    def test004_parse_options_unknown_subcommand(self):
        saved_argv = sys.argv
        sys.argv = ['sbtools', 'unknown-sc']
        # Make sure the expected exception is raised.
        self.assertRaises(sbtools.UnknownSubcommandError, self.sbtools.parse_options)

        # Make sure the expected message is included with the exception.
        try:
            self.sbtools.parse_options()
        except sbtools.UnknownSubcommandError, msg:
            self.assertEqual(str(msg), 'unknown-sc')
        sys.argv = saved_argv

    def test005_add_tool(self):
        self.sbtools.tcmdlist = []
        self.sbtools.cmdmap = {}
        self.sbtools.namemap = {}

        class TestTool1(SBTool):
            def __init__(self, sbtools):
                self.sbtools = sbtools

            def get_subcommands(self):
                return ["TestTool1"]

        class TestTool2(SBTool):
            def __init__(self, sbtools):
                self.sbtools = sbtools

            def get_subcommands(self):
                return ["TestTool2", "tt2"]

        class TestTool3(SBTool):
            def __init__(self, sbtools):
                self.sbtools = sbtools

            def get_subcommands(self):
                return ["TestTool3", "tt3", "ttool3"]

        class SCConflictTestTool1(SBTool):
            def __init__(self, sbtools):
                self.sbtools = sbtools

            def get_subcommands(self):
                return ["TestTool1", "tt1", "ttool1"]

        class SCConflictTestTool2(SBTool):
            def __init__(self, sbtools):
                self.sbtools = sbtools

            def get_subcommands(self):
                return ["ConflictTestTool2", "ctt2", "ttool3"]

        class NameConflictTestTool1(SBTool):
            def __init__(self, sbtools):
                self.sbtools = sbtools

            def get_subcommands(self):
                return ["NameConflictTestTool1"]

        # Start adding the tools.
        self.assertEqual(self.sbtools.tcmdlist, [])
        self.assertEqual(self.sbtools.cmdmap, {})
        self.assertEqual(self.sbtools.namemap, {})

        # Add tool 1.
        ttool = TestTool1(self.sbtools)
        self.sbtools.add_tool(TestTool1, "TestTool1", True, ttool.get_subcommands())
        self.assertEqual(self.sbtools.tcmdlist, [['TestTool1']])
        self.assertEqual(self.sbtools.cmdmap, {'TestTool1': [TestTool1, True]})
        self.assertEqual(self.sbtools.namemap, {'TestTool1': [TestTool1, True]})

        # Add tool 2.
        ttool = TestTool2(self.sbtools)
        self.sbtools.add_tool(TestTool2, "TestTool2", False, ttool.get_subcommands())
        self.assertEqual(self.sbtools.tcmdlist, [['TestTool1'], ['TestTool2', 'tt2']])
        self.assertEqual(self.sbtools.cmdmap, {'TestTool1': [TestTool1, True], 'TestTool2': [TestTool2, False], 'tt2': [TestTool2, False]})
        self.assertEqual(self.sbtools.namemap, {'TestTool1': [TestTool1, True], 'TestTool2': [TestTool2, False]})

        # Add tool 3.
        ttool = TestTool3(self.sbtools)
        self.sbtools.add_tool(TestTool3, "TestTool3", False, ttool.get_subcommands())
        self.assertEqual(self.sbtools.tcmdlist, [['TestTool1'], ['TestTool2', 'tt2'], ['TestTool3', 'tt3', 'ttool3']])
        self.assertEqual(self.sbtools.cmdmap, {'TestTool1': [TestTool1, True], 'TestTool2': [TestTool2, False], 'tt2': [TestTool2, False], 'TestTool3': [TestTool3, False], 'tt3': [TestTool3, False], 'ttool3': [TestTool3, False]})
        self.assertEqual(self.sbtools.namemap, {'TestTool1': [TestTool1, True], 'TestTool2': [TestTool2, False], 'TestTool3': [TestTool3, False]})

        # Add subcommand conflict tool 1.
        ttool = SCConflictTestTool1(self.sbtools)
        self.assertRaises(sbtools.SubcommandConflictWarning, self.sbtools.add_tool, SCConflictTestTool1, 'SCConflictTestTool1', True, ttool.get_subcommands())
        try:
            self.sbtools.add_tool(SCConflictTestTool1, 'SCConflictTestTool1', True, ttool.get_subcommands())
        except sbtools.SubcommandConflictWarning, msg:
            self.assertEqual(str(msg), textwrap.fill("WARNING: subcommand conflict with command 'TestTool1'; not loading SCConflictTestTool1 plugin.", 78))

        # Add subcommand conflict tool 2.
        ttool = SCConflictTestTool2(self.sbtools)
        self.assertRaises(sbtools.SubcommandConflictWarning, self.sbtools.add_tool, SCConflictTestTool2, 'SCConflictTestTool2', False, ttool.get_subcommands())
        try:
            self.sbtools.add_tool(SCConflictTestTool2, 'SCConflictTestTool2', False, ttool.get_subcommands())
        except sbtools.SubcommandConflictWarning, msg:
            self.assertEqual(str(msg), textwrap.fill("WARNING: subcommand conflict with command 'ttool3'; not loading SCConflictTestTool2 plugin.", 78))

        # Add name conflict test tool 1.
        ttool = NameConflictTestTool1(self.sbtools)
        self.assertRaises(sbtools.NameConflictWarning, self.sbtools.add_tool, NameConflictTestTool1, 'TestTool1', False, ttool.get_subcommands())
        try:
            self.sbtools.add_tool(NameConflictTestTool1, 'TestTool1', False, ttool.get_subcommands())
        except sbtools.NameConflictWarning, msg:
            self.assertEqual(str(msg), textwrap.fill("WARNING: name conflict with tool 'TestTool1' (subcommand 'NameConflictTestTool1'); not loading TestTool1 plugin.", 78))

    def test006_build_tool_list(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        keys = ['about', 'blank', 'bl', 'file', 'help', 'h', '?']
        names = ['About', 'Help', 'File', 'Blank']
        self.assertEqual(self.sbtools.tcmdlist, [['about'], ['blank', 'bl'], ['file'], ['help', 'h', '?']])
        self.assertEqual(len(self.sbtools.cmdmap), len(keys))
        for key in keys:
            self.assertTrue(self.sbtools.cmdmap.has_key(key))
        self.assertEqual(len(self.sbtools.namemap), len(names))
        for name in names:
            self.assertTrue(self.sbtools.namemap.has_key(name))

    def test007_get_full_toolname(self):
        t1 = ['tname']
        t2 = ['tname', 'alt1']
        t3 = ['tname', 'alt1', 'alt2']
        t4 = ['tname', 'alt1', 'alt2', 'alt3', 'alt4']
        self.assertEqual(self.sbtools.get_full_command(t1), 'tname')
        self.assertEqual(self.sbtools.get_full_command(t1, '   '), '   tname')
        self.assertEqual(self.sbtools.get_full_command(t2), 'tname (alt1)')
        self.assertEqual(self.sbtools.get_full_command(t3), 'tname (alt1, alt2)')
        self.assertEqual(self.sbtools.get_full_command(t4), 'tname (alt1, alt2, alt3, alt4)')

    def test008_get_subcommands(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])
        sclist = self.sbtools.get_subcommands()
        self.assertEqual(sclist, """   about
   blank (bl)
   file
   help (h, ?)
""")

    def test009_get_about(self):
        self.assertEqual(self.sbtools.get_about(), "The SBTools package was developed at the National Renewable Energy Laboratory.")

    def test010_has_tool_by_name(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        good_names = ['About', 'Help', 'File', 'Blank']
        bad_names = ['Blah', 'Check', 'Not a real plug-in']
        for name in good_names:
            self.assertTrue(self.sbtools.has_tool_by_name(name))
        for name in bad_names:
            self.assertFalse(self.sbtools.has_tool_by_name(name))

    def test011_has_tool_by_subcommand(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        good_scs = ['about', 'blank', 'bl', 'file', 'help', 'h', '?']
        bad_scs = ['blah', 'check', 'notreal']
        for sc in good_scs:
            self.assertTrue(self.sbtools.has_tool_by_subcommand(sc))
        for sc in bad_scs:
            self.assertFalse(self.sbtools.has_tool_by_subcommand(sc))

    def test012_get_tool_by_name(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        good_names = ['About', 'Help', 'File', 'Blank']
        bad_names = ['Blah', 'Check', 'Not a real plug-in']
        for name in good_names:
            self.assertEqual(self.sbtools.get_tool_by_name(name), self.sbtools.namemap[name][0])
        for name in bad_names:
            self.assertEqual(self.sbtools.get_tool_by_name(name), None)

    def test013_get_tool_by_subcommand(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        good_scs = ['about', 'blank', 'bl', 'file', 'help', 'h', '?']
        bad_scs = ['blah', 'check', 'notreal']
        for sc in good_scs:
            self.assertEqual(self.sbtools.get_tool_by_subcommand(sc), self.sbtools.cmdmap[sc][0])
        for sc in bad_scs:
            self.assertEqual(self.sbtools.get_tool_by_subcommand(sc), None)

    def test014_is_tool_builtin_by_name(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        good_names = ['About', 'Help', 'File', 'Blank']
        bad_names = ['Blah', 'Check', 'Not a real plug-in']
        for name in good_names:
            self.assertEqual(self.sbtools.is_tool_builtin_by_name(name), self.sbtools.namemap[name][1])
        for name in bad_names:
            self.assertEqual(self.sbtools.is_tool_builtin_by_name(name), None)

    def test015_is_tool_builtin_by_subcommand(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        good_scs = ['about', 'blank', 'bl', 'file', 'help', 'h', '?']
        bad_scs = ['blah', 'check', 'notreal']
        for sc in good_scs:
            self.assertEqual(self.sbtools.is_tool_builtin_by_subcommand(sc), self.sbtools.cmdmap[sc][1])
        for sc in bad_scs:
            self.assertEqual(self.sbtools.is_tool_builtin_by_subcommand(sc), None)

    def test016_get_toolname_list(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        names = ['About', 'Help', 'File', 'Blank']
        tnlist = self.sbtools.get_toolname_list()
        self.assertEqual(len(tnlist), len(names))
        for name in names:
            self.assertTrue(name in tnlist)

    def test017_get_tool_subcommand_list(self):
        self.sbtools.build_tool_list(True, ['tests/testfiles/plugins'])

        scs = ['about', 'blank', 'bl', 'file', 'help', 'h', '?']
        sclist = self.sbtools.get_tool_subcommand_list()
        self.assertEqual(len(sclist), len(scs))
        for sc in scs:
            self.assertTrue(sc in sclist)

class SBToolsTestSuite(unittest.TestSuite):
    """
    Test suite for the SBTools tests.
    """
    def __init__(self):
        sys.argv[0] = 'sbtools'
        unittest.TestSuite.__init__(self)
        self.addTest(unittest.makeSuite(TestSBToolsOptionParserMethods))
        self.addTest(unittest.makeSuite(TestSBToolOptionParserMethods))
        self.addTest(unittest.makeSuite(TestHelpMethods))
        self.addTest(unittest.makeSuite(TestAboutMethods))
        self.addTest(unittest.makeSuite(TestFileMethods))
        self.addTest(unittest.makeSuite(TestSBToolMethods))
        self.addTest(unittest.makeSuite(TestSBToolsMethods))

def runTests():
    suite = SBToolsTestSuite()
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == '__main__':
    sys.argv[0] = 'sbtools'
    runTests()
