import unittest
import cadre
from io import StringIO

good_config = u'''
Host project1
    User deploy
    HostName github.com
    IdentityFile ~/.ssh/project1.key

Host project2
    User deploy
    HostName github.com
    IdentityFile ~/.ssh/project2.key

Host project3
    User deploy
    IdentityFile ~/.ssh/project3.key
'''

class TestCadre(unittest.TestCase):
    def test_get_config_hosts(self):
        hosts = cadre._get_config_hosts(StringIO(good_config))
        self.assertEqual(
            set(('project1', 'project2', 'project3')),
            set(hosts),
            '_get_config_hosts did not return the correct hosts'
            )

if __name__ == '__main__':
    unittest.main()
