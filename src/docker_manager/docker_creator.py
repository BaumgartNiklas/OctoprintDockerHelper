from typing import AnyStr, TextIO, Optional
import os


def write_docker_compose(port: int, device: AnyStr, file_object: TextIO):
    """Writes an octoprint docker compose configuration to the given file object

    Args:
        port: port under which octoprint should be accessible
        device: device name (name in /dev) of the 3d printer for octoprint to connect to
        file_object: file object to write to
    """
    file_object.write("version: '2.4'\n"
                      f"name: {device}\n\n"
                      "services:\n"
                      "  octoprint:\n"
                      "    image: octoprint/octoprint\n"
                      "    restart: unless-stopped\n"
                      "    ports:\n"
                      f"      - {port}:80\n"
                      "    devices:\n"
                      f"      - /dev/{device}:/dev/ttyUSB0\n"
                      "    volumes:\n"
                      "      - octoprint:/octoprint\n\n"
                      "volumes:\n"
                      "  octoprint:\n")


def create_start_command(filepath_compose: AnyStr) -> AnyStr:
    """Creates a start(up) command for a docker compose file

    Args:
        filepath_compose: filepath of the docker-compose.yml to start

    Returns:
        docker compose up command for the specified file
    """
    return f"docker compose -f {filepath_compose} up -d"


def create_stop_command(filepath_compose: AnyStr) -> AnyStr:
    """Creates a stop command for a docker compose file

    Args:
        filepath_compose: filepath of the docker-compose.yml to stop

    Returns:
        docker compose stop command for the specified file
    """
    return f"docker compose -f {filepath_compose} stop"


def create_docker_compose(port: int, device: AnyStr, filepath: Optional[AnyStr] = None) -> AnyStr:
    """Creates a new docker compose file for an octoprint instance
    If no filepath is specified, a file called docker-compose.device_name.yml will be created
    under src/docker_manager/docker_files/.

    Args:
        port: port under which the octoprint container should be accessible
        device: device name (name in /dev) of the 3d printer for octoprint to connect to
        filepath: filepath to save the file to.

    Returns:
        absolute file path of the newly created file
    """
    if filepath is None:
        directory = os.path.dirname(os.path.abspath(__file__))

        docker_file_dir = os.path.join(directory, "docker_files")
        if not os.path.isdir(docker_file_dir):
            os.mkdir(docker_file_dir)

        filepath = os.path.join(directory, "docker_files", f"docker-compose.{device}.yml")

    with open(filepath) as file:
        write_docker_compose(port, device, file)

    return filepath
