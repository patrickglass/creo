#!/usr/bin/env python
import unittest

import creo


class CreoTestCase(unittest.TestCase):

    def test_process_cmd(self):
        retcode, text = creo.process_cmd('ls')
        print "Return Code:", retcode
        print "Response Text:", text
        self.assertEqual(retcode, 0)
        self.assertTrue(text)

    def test_import_twice_for_sys_path_branch(self):
        import creo
        reload(creo)
