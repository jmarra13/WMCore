#!/usr/bin/env python
"""
_FileTools_t_

Test class for file handling tools
"""
from __future__ import division

import os
import os.path
import unittest

from Utils import FileTools
from WMQuality.TestInitCouchApp import TestInitCouchApp


class testFileTools(unittest.TestCase):
    """
    Test to see whether we can do Linux
    """

    def setUp(self):
        """
        Do nothing

        """
        self.testInit = TestInitCouchApp(__file__)
        self.testDir = self.testInit.generateWorkDir()

        return

    def tearDown(self):
        """
        Do nothing

        """
        self.testInit.delWorkDir()

        return

    def test_tail(self):
        """
        _tail_

        Can we tail a file?
        """

        a = "a\nb\nc\nd\ne\nf\ng\nh\ni\nj\nk\nl\nm\nn\no\np\n"

        f = open('tmpfile.tmp', 'w')
        f.write(a)
        f.close()

        self.assertEqual(FileTools.tail('tmpfile.tmp', 10), "g\nh\ni\nj\nk\nl\nm\nn\no\np\n")

        self.assertEqual(FileTools.tail('tmpfile.tmp', 2), "o\np\n")

        os.remove('tmpfile.tmp')

        return

    def test_fileInfo(self):
        """
        _fileInfo_

        Test for basic file info
        """
        silly = "This is a rather ridiculous string"
        filename = os.path.join(self.testDir, 'fileInfo.test')

        f = open(filename, 'w')
        f.write(silly)
        f.close()

        info = FileTools.getFileInfo(filename=filename)
        self.assertEqual(info['Name'], filename)
        self.assertEqual(info['Size'], 34)
        return

    def test_getFullPath(self):
        fullPath = FileTools.getFullPath("cd")
        #assuming there is path for cd
        self.assertIsNotNone(fullPath)
        fullPath = FileTools.getFullPath("this_shouldnt_be")
        self.assertEqual(fullPath, None)

if __name__ == "__main__":
    unittest.main()
