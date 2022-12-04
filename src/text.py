vendor_id_help = 'includes the specified vendor id in the rule'
vendor_id_metavar = 'vendor_id'

model_id_help = 'includes the specified model id (product id) in the rule'
model_id_metavar = 'model_id/product_id'

docker_help = 'Creates a docker compose config file and adds respective commands to start and stop the container in the rule. The container will provide an octoprint instance on the specified port'
docker_metavar = 'Port'

file_help = 'Filepath of the udev rule file to use'
file_metavar = 'Filepath'

command_add_help = 'Add a udev rule'
command_remove_help = 'Remove a udev rule'
command_device_help = 'Shows a list of all connected devices and their relevant data'
command_rule_help = 'Shows a list of all udev rules and their data'

add_name_help = 'Name to use for the device'
add_name_metavar = 'DeviceName'
add_type_help = 'Device identification Method'
add_type_serial_help = 'identify a device through the use of a serial number'
add_type_path_help = 'identify a device through the usb port (ID_PATH) its connected to (only use if no serial number is available)'
add_type_devpath_help = 'identify a device through the usb port (devpath) its connected to (only use if no serial number is available). This option does not allow for the creation of a docker container.'

add_serial_number_help = 'serial number of the device'
add_path_help = 'path id of the usb device'
add_devpath_help = 'devpath of the usb device'

remove_type_help = 'Remove udev rules'
remove_type_serial_help = 'remove udev rules associated with a serial number'
remove_type_path_help = 'remove udev rules associated with a path id or devpath'
remove_type_name_help = 'remove udev rules associated with a name'

remove_serial_help = 'serial number used in the rule'
remove_path_help = 'path id or devpath used in the rule'
remove_name_help = 'name used in the rule'
