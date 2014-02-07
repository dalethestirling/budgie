import unittest
import os


class TestCadre(unittest.TestCase):
    '''Test case set to test cadre current build'''

    def test_import(self):
        '''Test the import of cadre python module'''
        import cadre

    def test_ssh_call(self):
        '''Test the __call__ that raises the NotImplementedError'''
        import cadre
        with self.assertRaises(NotImplementedError):
            cadre.ssh(os.environ['TESTHOST1'])()

    def test_ssh_run_cmd(self):
        '''Test that a command can be executed on the remote host'''
        import cadre
        self.assertEqual(str(cadre.ssh(os.environ['TESTHOST1']).whoami()).strip('\n'), os.environ['SSHUSR1'])

if __name__ == '__main__':
    # Setup environ vars 
    if not os.environ.has_key('TESTHOST1'):
        os.environ['TESTHOST1'] = 'svr'
    if not os.environ.has_key('SSHUSR1'):
        os.environ['SSHUSR1'] = 'dale'

    unittest.main()
