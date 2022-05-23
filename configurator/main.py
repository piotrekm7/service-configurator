"""Settings class implementation"""

import json
from abc import ABCMeta
from typing import Any
from copy import deepcopy

import yaml

from configurator.fields import Field, ValidationError

_is_base_model_class_defined = False


class SettingsMeta(ABCMeta):
    """
    Alters Settings classes creation.
    """

    def __new__(mcs, name, bases, namespace, **kwargs):
        _fields = {}

        for base in bases:
            if _is_base_model_class_defined and issubclass(base, BaseSettings):
                _fields.update(base._fields)

        for key, item in namespace.items():
            if isinstance(item, Field):
                _fields[key] = item

        namespace = {k: v for k, v in namespace.items() if k not in _fields}
        namespace['_fields'] = _fields
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        return cls


class SettingsError(Exception):
    """
    Thrown when Settings object is used incorrectly,
    i.e. required parameters are missing in config json
    """


class BaseSettings(Field, metaclass=SettingsMeta):
    """
    Base Settings model.
    All user's settings classes should be subclass of it.
    """
    _type = dict

    # Populated by the metaclass, defined here to help IDEs only
    _fields = {}

    def __init__(self, *args, **kwargs):
        """
        Creates a new Settings object.
        Args:
            *args:
            **kwargs:
        """
        super().__init__(*args, **kwargs)
        self.__data = {}
        for k, v in self._fields.items():
            # Embedded settings objects are stored in __data
            if isinstance(v, BaseSettings):
                self.__data[k] = deepcopy(v)
            else:
                self.__data[k] = v.default

    def from_json(self, filename: str) -> None:
        """
        Loads config from json file.
        Args:
            filename: path to json file
        """
        with open(filename) as json_file:
            data = json.load(json_file)
            self.from_dict(data)

    def to_json(self, filename: str) -> None:
        """
        Saves current settings to json file.
        Method can be used on a new object to generate template json.
        Args:
            filename: path to json file
        """
        with open(filename, 'w') as outfile:
            json.dump(self.to_dict(), outfile, indent=4)

    def from_yaml(self, filename: str) -> None:
        """
        Loads config from yaml file.
        Args:
            filename: path to yaml file
        """
        with open(filename) as yaml_file:
            data = yaml.safe_load(yaml_file)
            self.from_dict(data)

    def to_yaml(self, filename: str) -> None:
        """
        Saves current settings to yaml file.
        Method can be used on a new object to generate template yaml.
        Args:
            filename: path to yaml file
        """
        with open(filename, 'w') as outfile:
            yaml.dump(self.to_dict(), outfile)

    def from_dict(self, data: dict, partial_update: bool = False) -> None:
        """
        Updates settings with provided dict.
        All required settings should be present in the dict unless partial_update is True.
        Args:
            data: dictionary with new settings
            partial_update: set True if you don't want to update all required settings
        """
        for k, v in self._fields.items():
            value = data.get(k)
            if value is not None:
                try:
                    value = v.validate(value)
                except ValidationError as ex:
                    raise SettingsError(
                        f'Value {value} for field "{k}" did not pass validation checks: {ex}'
                    ) from ex
                if isinstance(v, BaseSettings):
                    self.__data[k].from_dict(value)
                else:
                    self.__data[k] = value
            else:
                if v.required and not partial_update:
                    raise SettingsError(f'Missing required value: {k}')

    def to_dict(self) -> dict:
        """
        Returns settings in dictionary format.
        Returns:
            dictionary with all the settings as primitive types.
        """
        return {k: (v if not isinstance(v, BaseSettings) else v.to_dict()) for k, v in self.__data.items()}

    def __getattr__(self, name: str) -> Any:
        if name in self._fields:
            return self.__data.get(name)
        else:
            raise AttributeError

    def __setattr__(self, name: str, value: Any) -> Any:
        if name in self._fields:
            if isinstance(self._fields[name], BaseSettings):
                raise AttributeError('Overriding Settings objects is not allowed, use from_dict() method.')
            self.__data[name] = self._fields[name].validate(value)
        else:
            super().__setattr__(name, value)


_is_base_model_class_defined = True
