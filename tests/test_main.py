"""Test Settings classes"""

from unittest import TestCase
from configurator import BaseSettings, SettingsError, Integer, String, ValidationError

# for testing field's default argument
default_int = 12


class MySettings(BaseSettings):
    """Simple settings class"""
    var1 = Integer()
    var2 = Integer(required=False, default=default_int)


class MySettings2(BaseSettings):
    """Settings with embedded settings"""
    var1 = Integer()
    my_settings = MySettings()


class MySettings3(MySettings):
    """Settings with inheritance"""
    var3 = String()


class AdditionalMemberSettings(BaseSettings):
    """Settings with additional non-field class member"""
    var = Integer()
    multiplier = 2

    def multiply(self):
        """Returns var multiplied by multiplier"""
        return self.var * self.multiplier


class SettingsTest(TestCase):
    """Test settings classes"""

    def test_default_argument(self):
        """Test setting default field value"""
        settings = MySettings()
        self.assertEqual(default_int, settings.var2)

    def test_partial_update(self):
        """Test partial update option"""
        settings = MySettings()
        with self.assertRaises(SettingsError):
            settings.from_dict({'var2': 2})

        settings.from_dict({'var2': 2}, partial_update=True)
        self.assertEqual(2, settings.var2)

    def test_embedded_settings(self):
        """Test class with embedded settings"""
        settings = MySettings2()
        data = {'var1': 1, 'my_settings': {'var1': 2, 'var2': 3}}
        settings.from_dict(data)
        self.assertEqual(data, settings.to_dict())

    def test_settings_inheritance(self):
        """Test settings inheritance"""
        settings = MySettings3()
        self.assertEqual(default_int, settings.var2)

    def test_setters(self):
        """Test setting values for fields"""
        settings = MySettings2()
        settings.var1 = 10
        with self.assertRaises(AttributeError):
            settings.my_settings = MySettings()

    def test_validation(self):
        """Test fields validation"""
        settings = MySettings()
        with self.assertRaises(ValidationError):
            settings.var1 = 'not_a_number'
        with self.assertRaises(SettingsError):
            settings.from_dict({'var1': 'str'})

    def test_json(self):
        """Test writing and reading settings from json file"""
        data = {'var1': 1, 'var2': 2}
        filepath = 'tests/test.json'

        settings = MySettings()
        settings.from_dict(data)
        settings.to_json(filepath)

        settings2 = MySettings()
        settings2.from_json(filepath)

        self.assertEqual(data, settings2.to_dict())

    def test_yaml(self):
        """Test writing and reading settings from yaml file"""
        data = {'var1': 1, 'var2': 2}
        filepath = 'tests/test.yaml'

        settings = MySettings()
        settings.from_dict(data)
        settings.to_yaml(filepath)

        settings2 = MySettings()
        settings2.from_yaml(filepath)

        self.assertEqual(data, settings2.to_dict())

    def test_additional_class_member(self):
        """Test settings with additional non-field values"""
        settings = AdditionalMemberSettings()
        settings.var = 5
        self.assertEqual(10, settings.multiply())
