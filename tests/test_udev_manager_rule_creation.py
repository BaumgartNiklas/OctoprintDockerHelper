import unittest
import src.udev_manager as rule_creator


class TestUdevRuleCreation(unittest.TestCase):
    def test_create_rule_serial(self):
        result = rule_creator.create_udev_rule_devpath("Printer1", "1234")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{serial}=="1234", SYMLINK+="Printer1"', result)
        result = rule_creator.create_udev_rule_devpath("Printer1", "1234", vendor_id="83kr")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{idVendor}=="83kr", ATTRS{serial}=="1234", SYMLINK+="Printer1"', result)
        result = rule_creator.create_udev_rule_devpath("Printer1", "1234", product_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{idProduct}=="48hs", ATTRS{serial}=="1234", SYMLINK+="Printer1"', result)
        result = rule_creator.create_udev_rule_devpath("Printer1", "1234", vendor_id="83kr", product_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{idVendor}=="83kr", ATTRS{idProduct}=="48hs", ATTRS{serial}=="1234", SYMLINK+="Printer1"', result)

    def test_create_rule_devpath(self):
        result = rule_creator.create_udev_rule_devpath("Printer1", devpath="1.1")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{devpath}=="1.1", SYMLINK+="Printer1"', result)
        result = rule_creator.create_udev_rule_devpath("Printer1", devpath="1.1", vendor_id="83kr")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{idVendor}=="83kr", ATTRS{devpath}=="1.1", SYMLINK+="Printer1"', result)
        result = rule_creator.create_udev_rule_devpath("Printer1", devpath="1.1", product_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{idProduct}=="48hs", ATTRS{devpath}=="1.1", SYMLINK+="Printer1"', result)
        result = rule_creator.create_udev_rule_devpath("Printer1", devpath="1.1", vendor_id="83kr", product_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ATTRS{idVendor}=="83kr", ATTRS{idProduct}=="48hs", ATTRS{devpath}=="1.1", SYMLINK+="Printer1"', result)

    def test_create_rule_no_serial_devpath(self):
        with self.assertRaises(ValueError):
            rule_creator.create_udev_rule_devpath("Printer1", None, None)
        with self.assertRaises(ValueError):
            rule_creator.create_udev_rule_devpath("Printer1", None, None, None, None)
        with self.assertRaises(ValueError):
            rule_creator.create_udev_rule_devpath("Printer1", None, None, "83kr", None)
        with self.assertRaises(ValueError):
            rule_creator.create_udev_rule_devpath("Printer1", None, None, None, "48hs")
        with self.assertRaises(ValueError):
            rule_creator.create_udev_rule_devpath("Printer1", None, None, "83kr", "48hs")

    def test_create_startstop_rule_serial(self):
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", "1234")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_SERIAL}=="1234", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_SERIAL}=="1234", ACTION=="remove", RUN+="stop"', result)
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", "1234", vendor_id="83kr")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_SERIAL}=="1234", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_SERIAL}=="1234", ACTION=="remove", RUN+="stop"', result)
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", "1234", model_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_MODEL_ID}=="48hs", ENV{ID_SERIAL}=="1234", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_MODEL_ID}=="48hs", ENV{ID_SERIAL}=="1234", ACTION=="remove", RUN+="stop"', result)
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", "1234", vendor_id="83kr", model_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_MODEL_ID}=="48hs", ENV{ID_SERIAL}=="1234", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_MODEL_ID}=="48hs", ENV{ID_SERIAL}=="1234", ACTION=="remove", RUN+="stop"', result)

    def test_create_startstop_rule_path(self):
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", path="UsbPath")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_PATH}=="UsbPath", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_PATH}=="UsbPath", ACTION=="remove", RUN+="stop"', result)
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", path="UsbPath", vendor_id="83kr")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_PATH}=="UsbPath", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_PATH}=="UsbPath", ACTION=="remove", RUN+="stop"', result)
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", path="UsbPath", model_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_MODEL_ID}=="48hs", ENV{ID_PATH}=="UsbPath", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_MODEL_ID}=="48hs", ENV{ID_PATH}=="UsbPath", ACTION=="remove", RUN+="stop"', result)
        result = rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", path="UsbPath", vendor_id="83kr", model_id="48hs")
        self.assertEqual('SUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_MODEL_ID}=="48hs", ENV{ID_PATH}=="UsbPath", SYMLINK+="Printer1", ACTION=="add", RUN+="start"\nSUBSYSTEM=="tty", ENV{ID_VENDOR_ID}=="83kr", ENV{ID_MODEL_ID}=="48hs", ENV{ID_PATH}=="UsbPath", ACTION=="remove", RUN+="stop"', result)

    def test_create_startstop_rule_no_serial_devpath(self):
        with self.assertRaises(ValueError):
            rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", None, None)
        with self.assertRaises(ValueError):
            rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", None, None, None, None)
        with self.assertRaises(ValueError):
            rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", None, None, "83kr", None)
        with self.assertRaises(ValueError):
            rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", None, None, None, "48hs")
        with self.assertRaises(ValueError):
            rule_creator.create_startstop_udev_rule("Printer1", "start", "stop", None, None, "83kr", "48hs")


if __name__ == '__main__':
    unittest.main()
