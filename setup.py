#!/usr/bin/env python3
"""
Setup script for APZmedia ComfyUI JSON and CSV Utils
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="comfyui-apzmedia-json-utils",
    version="0.1.0",
    author="Pablo Apiolazza",
    author_email="pablo@apzmedia.com",
    description="APZmedia ComfyUI JSON and CSV Utility Nodes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/APZmedia/ComfyUI-APZmedia-JSON-utils",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 