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
        # with self.assertRaises(NotImplementedError):
        #     cadre.ssh('localhost')()
        self.assertRaises(NotImplementedError,cadre.ssh('localhost'))

    def test_ssh_run_cmd(self):
        '''Test that a command can be executed on the remote host'''
        import cadre
        
        self.assertEqual(str(cadre.ssh().bake(
            '-o', 'UserKnownHostsFile=/dev/null', '-o',  
            'StrictHostKeyChecking=no', '127.0.0.1'
        ).whoami()).strip('\n'), os.environ['USER'])

    def test_host_group_exists(self):
        import cadre

        dummy_group = cadre.HostGroup(['localhost', 'localhost2'])
        self.assertTrue(dummy_group.has_key('localhost'))
        self.assertTrue(isinstance(dummy_group['localhost'], cadre.ssh))

    def test_host_group_add(self):
        import cadre

        dummy_group1 = cadre.HostGroup()
        dummy_group1.add('localhost')
        localhost1 = cadre.ssh('localhost1')
        dummy_group1.add(localhost1)

        self.assertTrue(dummy_group1.has_key('localhost'))
        self.assertTrue(isinstance(dummy_group1['localhost'], cadre.ssh))

        self.assertTrue(dummy_group1.has_key('localhost1'))
        self.assertTrue(isinstance(dummy_group1['localhost1'], cadre.ssh))

        dummy_group2 = cadre.HostGroup()
        localhost = cadre.ssh('localhost')
        dummy_group2.add([localhost, localhost1])

        self.assertTrue(dummy_group2.has_key('localhost'))
        self.assertTrue(isinstance(dummy_group2['localhost'], cadre.ssh))

        self.assertTrue(dummy_group2.has_key('localhost1'))
        self.assertTrue(isinstance(dummy_group2['localhost1'], cadre.ssh))

    def test_host_group_remove(self):
        import cadre

        dummy_group = cadre.HostGroup(['localhost', 'localhost2'])
        del dummy_group['localhost']
        self.assertRaises(KeyError, dummy_group['localhost'])

    def test_host_group_run(self):
        import cadre

        dummy_group = cadre.HostGroup(['localhost', 'localhost2'])
        whoami_result = dummy_group.whoami()
        self.assertEqual(
            whoami_result['localhost'].strip('\n'), 
            whoami_result['localhost1'].strip('\n')
        )

if __name__ == '__main__':

    unittest.main()
