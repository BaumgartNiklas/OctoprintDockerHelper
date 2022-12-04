import argparse
import sys
import text
from typing import AnyStr, Optional
import controller


def add_optional_args(parser, dest_vendor: Optional[AnyStr] = None, dest_model:  Optional[AnyStr] = None, dest_file:  Optional[AnyStr] = None, dest_docker:  Optional[AnyStr] = None):
    """ Adds optional argument to the parses.
    The optional arguments are for the vendor id, model id (product id), udev rule filepath, docker port.
    The arguments are -v (--vendor), -m (--model), -f (--file) and -d (--docker) respectively
    The added arguments are hidden from the help page.
    If the destination for an argument is None, the corresponding argument is not added to the parser.

    Args:
        parser: parser to add the optional argument to.
        dest_vendor: destination name for the vendor id
        dest_model: destination name for the model id (product id)
        dest_file: destination name for the udev rule filepath
        dest_docker: destination name for the docker port

    Returns:
        Dictionary {arg_vendor, arg_model, arg_file, arg_docker} containing the argument objects of the created arguments.
    """
    args = {}
    if dest_vendor:
        args['arg_vendor'] = parser.add_argument('-v', '--vendor', type=str, metavar=text.vendor_id_metavar, dest=dest_vendor, default=None, help=argparse.SUPPRESS)
    if dest_model:
        args['arg_model'] = parser.add_argument('-m', '--model', type=str, metavar=text.model_id_metavar, dest=dest_model, default=None, help=argparse.SUPPRESS)
    if dest_file:
        args['arg_file'] = parser.add_argument('-f', '--file', type=str, metavar=text.file_metavar, dest=dest_file, default=None, help=argparse.SUPPRESS)
    if dest_docker:
        args['arg_docker'] = parser.add_argument('-d', '--docker', type=int, metavar=text.docker_metavar, dest=dest_docker, default=None, help=argparse.SUPPRESS)
    return args


def show_optional_args(arg_dict: dict, arg_vendor: bool = False, arg_model: bool = False, arg_file: bool = False, arg_docker: bool = False):
    """Function that changes the help parameter of the arguments created by add_optional_args.

    Args:
        arg_dict: dictionary as created by add_optional_args.
        arg_vendor: Show the vendor argument in the help page
        arg_model: Show the model argument in the help page
        arg_file: Show the file argument in the help page
        arg_docker: show the docker argument in the help page
    """
    if arg_vendor and 'arg_vendor' in arg_dict:
        arg_dict['arg_vendor'].help = text.vendor_id_help

    if arg_model and 'arg_model' in arg_dict:
        arg_dict['arg_model'].help = text.model_id_help

    if arg_file and 'arg_file' in arg_dict:
        arg_dict['arg_file'].help = text.file_help

    if arg_docker and 'arg_docker' in arg_dict:
        arg_dict['arg_docker'].help = text.docker_help


def get_args():
    """ Creates the arguments for the command line interface

    Returns:
        Dictionary with the values of the arguments as given by the user/caller
    """
    parser = argparse.ArgumentParser()
    # hidden optional parameters (to support them in any position even with the use of subparsers)
    add_optional_args(parser, 'vendor', 'model', 'file', 'docker')

    # first argument (action to execute) {devices, rules, add, remove)
    subparser = parser.add_subparsers(help='Commands', dest='command')
    subparser.add_parser('devices', help=text.command_device_help)
    rule_parser = subparser.add_parser('rules', help=text.command_rule_help)
    add_parser = subparser.add_parser('add', help=text.command_add_help)
    remove_parser = subparser.add_parser("remove", help=text.command_remove_help)

    # rule action (display current rules)
    optional_args = add_optional_args(rule_parser, dest_file='file2')
    show_optional_args(optional_args, arg_file=True)

    # add action (add udev rule) {serial, path, devpath)
    optional_args = add_optional_args(add_parser, 'vendor2', 'model2', 'file2', 'docker2')
    show_optional_args(optional_args, True, True, True, False)
    add_parser.add_argument('name', type=str, metavar=text.add_name_metavar, help=text.add_name_help)
    add_type_parser = add_parser.add_subparsers(help=text.add_type_help, dest='add_type')
    add_parser_serial = add_type_parser.add_parser('serial', help=text.add_type_serial_help)
    add_parser_path = add_type_parser.add_parser('path', help=text.add_type_path_help)
    add_parser_devpath = add_type_parser.add_parser('devpath', help=text.add_type_devpath_help)

    # add action serial
    optional_args = add_optional_args(add_parser_serial, 'vendor3', 'model3', 'file3', 'docker3')
    show_optional_args(optional_args, True, True, True, True)
    add_parser_serial.add_argument('serial number', type=str, help=text.add_serial_number_help)

    # add action path
    optional_args = add_optional_args(add_parser_path, 'vendor3', 'model3', 'file3', 'docker3')
    show_optional_args(optional_args, True, True, True, True)
    add_parser_path.add_argument('path', type=str, help=text.add_path_help)

    # add action devpath
    optional_args = add_optional_args(add_parser_devpath, 'vendor3', 'model3', 'file3')
    show_optional_args(optional_args, True, True, True)
    add_parser_devpath.add_argument('devpath', type=str, help=text.add_devpath_help)

    # remove action (remove udev rule) {serial, path/devpath, name}
    optional_args = add_optional_args(remove_parser, dest_file='file2')
    show_optional_args(optional_args, arg_file=True)
    remove_type_parser = remove_parser.add_subparsers(help=text.remove_type_help, dest='remove_type')
    remove_serial_parser = remove_type_parser.add_parser('serial', help=text.remove_type_serial_help)
    remove_path_parser = remove_type_parser.add_parser('path', help=text.remove_type_path_help)
    remove_name_parser = remove_type_parser.add_parser('name', help=text.remove_type_name_help)

    # remove action serial
    optional_args = add_optional_args(remove_serial_parser, dest_file='file2')
    show_optional_args(optional_args, arg_file=True)
    remove_serial_parser.add_argument("serial number", type=str, help=text.remove_serial_help)

    # remove action path
    optional_args = add_optional_args(remove_path_parser, dest_file='file2')
    show_optional_args(optional_args, arg_file=True)
    remove_path_parser.add_argument("path/devpath", type=str, help=text.remove_path_help)

    # remove action name
    optional_args = add_optional_args(remove_name_parser, dest_file='file2')
    show_optional_args(optional_args, arg_file=True)
    remove_name_parser.add_argument('name', type=str, help=text.remove_name_help)

    arg_dict = vars(parser.parse_args())
    if not arg_dict.get('command'):
        parser.print_help()
        sys.exit()
    return arg_dict


def process_args(args):
    """Processes the arguments given by get_args and calls the corresponding functions in the controller module

    Args:
        args: args as returned by get_args
    """
    file = args.get('file') or args.get('file2') or args.get('file3')
    if not file:
        file = '/etc/udev/rules.d/99-serial.rules'
    command = args["command"]

    if command == 'devices':
        controller.print_devices()
        sys.exit()

    if command == 'rules':
        controller.print_rules(file)
        sys.exit()

    if command == 'add':
        name = args.get('name')
        vendor = args.get('vendor') or args.get('vendor2') or args.get('vendor3')
        model = args.get('model') or args.get('model2') or args.get('model3')
        docker = args.get('docker') or args.get('docker2') or args.get('docker3')
        serial = args.get('serial number', None)
        path = args.get('path', None)
        devpath = args.get('devpath', None)

        if args.get('add_type') == 'devpath' and docker:
            print('Docker is not supported when using devpath')
            sys.exit()

        if docker:
            controller.add_rule_docker(file, docker, name, vendor, model, path, serial)
        else:
            controller.add_rule(file, name, vendor, model, devpath, path, serial)
        sys.exit()

    if command == 'remove':
        file = args.get('file') or args.get('file2')
        serial = args.get('serial number', None)
        path = args.get('path/devpath', None)
        name = args.get('name', None)
        controller.remove_rule(file, name, path, serial)
        sys.exit()

    sys.exit()


if __name__ == "__main__":
    arguments = get_args()
    process_args(arguments)
