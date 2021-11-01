from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mobi-reader",
    version="0.1.0",
    author="MrLucio",
    description="A simple way to read and convert your mobi files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrLucio/mobi-reader",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.4",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)