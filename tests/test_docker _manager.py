import unittest
import src.docker_manager as docker_creator
from unittest.mock import patch, mock_open
from test_data import docker_compose_sample


class MockWrite:
    def __init__(self):
        self.content = ''

    def write_data(self, data):
        self.content += data


class TestDockerCreation(unittest.TestCase):

    def test_create_start_command(self):
        result = docker_creator.create_start_command('filepath')
        self.assertEqual('docker compose -f filepath up -d', result)

    def test_create_stop_command(self):
        result = docker_creator.create_stop_command('filepath')
        self.assertEqual('docker compose -f filepath stop', result)

    def test_write_docker_compose(self):
        file = mock_open(read_data="")
        writer = MockWrite()
        file.return_value.write = writer.write_data

        with patch('builtins.open', file):
            docker_creator.create_docker_compose(5000, "Printer1")
            self.assertEqual(docker_compose_sample, writer.content)

    def test_write_docker_compose_filepath(self):
        file = mock_open(read_data="")
        writer = MockWrite()
        file.return_value.write = writer.write_data

        with patch('builtins.open', file):
            result = docker_creator.create_docker_compose(5000, "Printer1", "custom/file/path")
            self.assertEqual(docker_compose_sample, writer.content)
            file.assert_called_once_with("custom/file/path")
            self.assertEqual(result, "custom/file/path")


if __name__ == '__main__':
    unittest.main()
