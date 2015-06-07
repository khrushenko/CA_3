import json
from mock import *
import unittest

import web_server
import file_server

__author__ = 'master'


class Test(unittest.TestCase):
    @patch('file_server.read')
    def test_read(self, read_function):
        val = {"name": "Lab1", "about": "About something", "state": "Completed"}
        mock = Mock()
        mock.return_value = val
        read_function.return_value = mock.return_value
        res = web_server.bottle_read()
        self.assertEqual(res, json.dumps(val))

    # Testing file server
    def test_file_server_create(self):
        self.assertEqual(file_server.result_OK,
                         file_server.add('Lab for test'))
        self.assertEqual(file_server.error_file_exists,
                         file_server.add('Lab for test'))

    def test_file_server_read(self):
        assert file_server.read()

    def test_file_server_delete(self):
        self.assertEquals(file_server.result_OK,
                          file_server.delete('Lab for test'))
        self.assertEquals(file_server.error_no_file,
                          file_server.delete('Lab for test'))

    def test_file_server_update(self):
        name1 = 'Some lab for test'
        name2 = 'Some lab for test 2'
        file_server.add(name1)
        file_server.add(name2)
        self.assertEqual(file_server.result_OK,
                         file_server.update(name1, 'about', 'About something'))
        self.assertEqual(file_server.error_file_exists,
                         file_server.update(name1, 'name', name2))
        file_server.delete(name1)
        file_server.delete(name2)


if __name__ == '__main__':
    unittest.main()