import unittest
import src.udev_manager.udev_rulefile_utils as udev_utils
from test_data import udev_rules_data


class TestUdevRuleCreation(unittest.TestCase):

    def test_get_serial_numbers(self):
        result = udev_utils.get_serial_numbers(udev_rules_data)
        self.assertIn("3940855329", result)
        self.assertIn("ryvk87g4", result)
        self.assertIn("kise", result)
        self.assertIn("kpl6", result)
        self.assertEqual(4, len(result))

    def test_get_names(self):
        result = udev_utils.get_names(udev_rules_data)
        self.assertIn("Printer1", result)
        self.assertIn("Printer2", result)
        self.assertIn("Printer3", result)
        self.assertIn("Printer4", result)
        self.assertIn("Printer5", result)
        self.assertIn("Printer6", result)
        self.assertIn("Printer7", result)
        self.assertIn("Printer8", result)
        self.assertEqual(8, len(result))

    def test_get_paths(self):
        result = udev_utils.get_paths(udev_rules_data)
        self.assertIn("1.1", result)
        self.assertIn("1.5", result)
        self.assertIn("UsbPathTo1", result)
        self.assertIn("UsbPathTo2", result)
        self.assertEqual(4, len(result))

    def test_get_device_rules(self):
        result = udev_utils.get_device_rules(udev_rules_data)
        self.assertIn("Printer1", result)
        self.assertEqual(udev_utils.DeviceData(None, '1973', '5927', None, '1.1'), result["Printer1"])
        self.assertIn("Printer2", result)
        self.assertEqual(udev_utils.DeviceData(None, '1973', '5927', '3940855329', None), result["Printer2"])
        self.assertIn("Printer3", result)
        self.assertEqual(udev_utils.DeviceData(None, 'm78', 'ab4g', 'kise', None), result["Printer3"])
        self.assertIn("Printer4", result)
        self.assertEqual(udev_utils.DeviceData(None, None, None, 'kpl6', None), result["Printer4"])
        self.assertIn("Printer5", result)
        self.assertEqual(udev_utils.DeviceData('UsbPathTo1', 'm78', 'ab4g', None, None), result["Printer5"])
        self.assertIn("Printer6", result)
        self.assertEqual(udev_utils.DeviceData('UsbPathTo2', None, None, None, None), result["Printer6"])
        self.assertIn("Printer7", result)
        self.assertEqual(udev_utils.DeviceData(None, None, None, 'ryvk87g4', None), result["Printer7"])
        self.assertIn("Printer8", result)
        self.assertEqual(udev_utils.DeviceData(None, None, None, None, '1.5'), result["Printer8"])
        self.assertEqual(8, len(result.keys()))

    def test_remove_rule_serial(self):
        result = udev_utils.remove_rule_by_serial(udev_rules_data, "3940855329")
        self.assertNotIn("3940855329", result)
        self.assertEqual(14, result.count("\n"))
        result = udev_utils.remove_rule_by_serial(udev_rules_data, "kise")
        self.assertNotIn("kise", result)
        self.assertEqual(13, result.count("\n"))

    def test_remove_rule_serial_not_existent(self):
        result = udev_utils.remove_rule_by_serial(udev_rules_data, "nonExistentSerial")
        self.assertEqual(udev_rules_data, result)

    def test_remove_rule_path(self):
        result = udev_utils.remove_rule_by_path(udev_rules_data, "1.1")
        self.assertNotIn("1.1", result)
        self.assertEqual(14, result.count("\n"))
        result = udev_utils.remove_rule_by_path(udev_rules_data, "UsbPathTo1")
        self.assertNotIn("UsbPathTo1", result)
        self.assertEqual(13, result.count("\n"))

    def test_remove_rule_path_not_existent(self):
        result = udev_utils.remove_rule_by_path(udev_rules_data, "nonExistentPath")
        self.assertEqual(udev_rules_data, result)

    def test_remove_rule_name_path(self):
        result = udev_utils.remove_rule_by_name(udev_rules_data, "Printer1")
        self.assertNotIn("1.1", result)
        self.assertEqual(14, result.count("\n"))
        result = udev_utils.remove_rule_by_name(udev_rules_data, "Printer5")
        self.assertNotIn("UsbPathTo1", result)
        self.assertEqual(13, result.count("\n"))

    def test_remove_rule_name_serial(self):
        result = udev_utils.remove_rule_by_name(udev_rules_data, "Printer2")
        self.assertNotIn("3940855329", result)
        self.assertEqual(14, result.count("\n"))
        result = udev_utils.remove_rule_by_name(udev_rules_data, "Printer3")
        self.assertNotIn("kise", result)
        self.assertEqual(13, result.count("\n"))

    def test_remove_rule_name_not_existent(self):
        result = udev_utils.remove_rule_by_name(udev_rules_data, "nonExistentPrinter")
        self.assertEqual(udev_rules_data, result)


if __name__ == '__main__':
    unittest.main()
