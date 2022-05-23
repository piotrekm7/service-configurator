"""Setup script"""
import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='service-configurator',
    version='1.0.0',
    url='https://github.com/piotrekm7/service-configurator',
    license='MIT',
    author='Piotr Muras',
    author_email='piotrekm7@gmail.com',
    description='A package for storing service config and secrets',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=['configurator'],
    python_requires='>=3.8.1',
    install_requires=['pyyaml>=6.0.0']
)
