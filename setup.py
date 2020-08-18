import os
import io

from setuptools import setup, find_packages


def read(fname):
    with io.open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8") as f:
        return f.read()


setup(
    name="VOID",
    version="1.0.0",
    author="Daniel Schwalbe-Koda",
    email="dskoda@mit.edu",
    url="https://github.com/learningmatter-mit/VOID",
    packages=find_packages("."),
    scripts=["scripts/dock.py",],
    python_requires=">=3.5",
    install_requires=["numpy", "networkx", "pymatgen>=2020.3.2", "scikit-learn"],
    license="MIT",
    description="Voronoi Organic-Inorganic Docker",
    long_description=read("README.md"),
)
