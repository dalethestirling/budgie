import unittest
import os
import sys

def the_baker(ssh_obj):
    return ssh_obj.bake(
        '-o', 'UserKnownHostsFile=/dev/null', 
        '-o', 'StrictHostKeyChecking=no' 
        )


class TestCadre(unittest.TestCase):
    '''Test case set to test cadre current build'''

    def test_import(self):
        '''Test the import of cadre python module'''
        import cadre

    def test_ssh_call(self):
        '''Test the __call__ that raises the NotImplementedError'''
        import cadre
        # with self.assertRaises(NotImplementedError):
        #     cadre.ssh('localhost')()
        self.assertRaises(NotImplementedError,cadre.ssh('localhost'))

    def test_ssh_run_cmd(self):
        '''Test that a command can be executed on the remote host'''
        import cadre
        
        self.assertEqual(
            str(the_baker(cadre.ssh('127.0.0.1')).whoami()).strip('\n'), 
            os.environ['USER']
        )

    def test_host_group_exists(self):
        import cadre

        dummy_group = cadre.HostGroup(['localhost', 'localhost1'])
        self.assertTrue(dummy_group.has_key('localhost'))
        self.assertTrue(isinstance(dummy_group['localhost'], cadre.ssh))

    def test_host_group_add(self):
        import cadre
        import tests

        dummy_group1 = cadre.HostGroup()
        dummy_group1.add('localhost')
        localhost1 = tests.the_baker(cadre.ssh('localhost1'))
        dummy_group1.add(localhost1)

        self.assertTrue(dummy_group1.has_key('localhost'))
        self.assertTrue(isinstance(dummy_group1['localhost'], cadre.ssh))

        self.assertTrue(dummy_group1.has_key('localhost1'))
        self.assertTrue(isinstance(dummy_group1['localhost1'], cadre.ssh))

        dummy_group2 = cadre.HostGroup()
        localhost = the_baker(cadre.ssh('localhost'))
        dummy_group2.add([localhost, localhost1])

        self.assertTrue(dummy_group2.has_key('localhost'))
        self.assertTrue(isinstance(dummy_group2['localhost'], cadre.ssh))

        self.assertTrue(dummy_group2.has_key('localhost1'))
        self.assertTrue(isinstance(dummy_group2['localhost1'], cadre.ssh))

    def test_host_group_remove(self):
        import cadre

        localhost = the_baker(cadre.ssh('localhost'))
        localhost1 = the_baker(cadre.ssh('localhost1'))

        dummy_group = cadre.HostGroup([localhost, localhost1])
        del dummy_group['localhost']
        if sys.version_info[:2] == (2,6):
            try:
                dummy_group['localhost']
            except:
                self.assertTrue(isinstance(sys.exc_info()[1], KeyError))
        else:
            with self.assertRaises(KeyError):
                dummy_group['localhost']

    def test_host_group_run(self):
        import cadre

        localhost = the_baker(cadre.ssh('localhost'))
        localhost1 = the_baker(cadre.ssh('localhost1'))

        dummy_group = cadre.HostGroup([localhost, localhost1])
        whoami_result = dummy_group.whoami()
        self.assertEqual(
            whoami_result['localhost'].strip('\n'), 
            whoami_result['localhost1'].strip('\n')
        )

if __name__ == '__main__':

    unittest.main()
