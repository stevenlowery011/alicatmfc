import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alicatmfc",
    version="0.0.2",
    author="Steven Lowery",
    author_email="steven.lowery011@gmail.com",
    description="A package for controlling Alicat mass flow controllers with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stevenlowery011/alicatmfc",
    packages=setuptools.find_packages(),
	install_requires=['pyserial'],
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
