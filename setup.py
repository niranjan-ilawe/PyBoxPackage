from setuptools import setup

setup(
    name="pybox",
    version="0.3.1",
    description="Python package for Box",
    url="https://github.com/niranjan-ilawe/PyBoxPackage",
    author="niranjan.ilawe",
    author_email="niranjan.ilawe@10xgenomics.com",
    license="MIT",
    packages=["pybox"],
    install_requires=["boxsdk", "keyring", "openpyxl"],
    dependency_links=["http://github.com"],
    zip_safe=False,
)
