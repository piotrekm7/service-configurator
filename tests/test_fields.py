"""Test settings fields"""

from unittest import TestCase
from configurator import ValidationError, Integer, PositiveInteger, Email, String, Url


class TestField(TestCase):
    """Test base field class"""

    def test_type_checking(self):
        """Test if field type is checked during validation"""
        integer = Integer()
        string = String()
        self.assertEqual(2, integer.validate(2))
        self.assertEqual('2', string.validate('2'))

        with self.assertRaises(ValidationError):
            integer.validate('2')
        with self.assertRaises(ValidationError):
            integer.validate('2')


class TestPositiveInteger(TestCase):
    """Test positive integer class"""

    def test_validation(self):
        """Test positive integer validation throws exception if provided non positive number"""
        p_int = PositiveInteger()
        self.assertEqual(2, p_int.validate(2))
        with self.assertRaises(ValidationError):
            p_int.validate(-2)
        with self.assertRaises(ValidationError):
            p_int.validate(0)


class TestEmail(TestCase):
    """Test email class"""

    def test_validation(self):
        """Test email validation"""
        valid_email = 'test@example.com'
        invalid_email = 'test@example'
        email = Email()

        self.assertEqual(valid_email, email.validate(valid_email))
        with self.assertRaises(ValidationError):
            email.validate(invalid_email)


class TestUrl(TestCase):
    """Test url class"""

    def test_validation(self):
        """Test url validation"""
        valid_url = 'http://www.example.com/'
        ip = 'http://192.168.0.10:5400'
        url = Url()
        self.assertEqual(valid_url, url.validate(valid_url))
        self.assertEqual(ip, url.validate(ip))

        with self.assertRaises(ValidationError):
            url.validate('www.example.com')  # missing http
        with self.assertRaises(ValidationError):
            url.validate('http://www.example')  # missing domain
