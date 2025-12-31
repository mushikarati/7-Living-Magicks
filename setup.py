#!/usr/bin/env python3
"""Setup script for 7 Living Magicks Codex."""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="seven-living-magicks",
    version="1.0.0",
    description="A symbolic framework for interpreting and engineering emergent systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MUSHIKARATI",
    url="https://github.com/mushikarati/7-Living-Magicks",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Researchers",
        "Topic :: Scientific/Engineering :: Symbolic Systems",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="symbolic-systems, recursion, thermodynamics, codex, emergence",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[],  # No external dependencies
    extras_require={
        "dev": ["pytest>=7.0", "black>=22.0", "flake8>=5.0"],
    },
    entry_points={
        "console_scripts": [
            "codex-ultima=codex_ultima:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/mushikarati/7-Living-Magicks/issues",
        "Source": "https://github.com/mushikarati/7-Living-Magicks",
        "DOI": "https://doi.org/10.5281/zenodo.16092500",
    },
)
