import os
import io

from setuptools import setup, find_packages


def read(fname):
    with io.open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8") as f:
        return f.read()


setup(
    name="moldocker",
    version="1.0.0",
    author="Daniel Schwalbe-Koda",
    email="dskoda@mit.edu",
    url="https://github.com/dskoda/moldocker",
    packages=find_packages("."),
    scripts=[
        "scripts/dock.py",
    ],
    python_requires=">=3.5",
    install_requires=[
        "numpy",
        "pymatgen>=2020.3.2",
    ],
    license="MIT",
    description="Tools to dock molecules to crystal structures",
    long_description=read("README.md"),
)
