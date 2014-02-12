import unittest
import os


class TestCadre(unittest.TestCase):
    '''Test case set to test cadre current build'''

    def test_import(self):
        '''Test the import of cadre python module'''
        import cadre

    # def test_ssh_call(self):
    #     '''Test the __call__ that raises the NotImplementedError'''
    #     import cadre
    #     with self.assertRaises(NotImplementedError):
    #         cadre.ssh('localhost')()

    def test_ssh_run_cmd(self):
        '''Test that a command can be executed on the remote host'''
        print os.environ['USER']
        import cadre
        self.assertEqual(str(cadre.ssh('localhost').whoami()).strip('\n'), os.environ['USER'])

if __name__ == '__main__':

    unittest.main()
