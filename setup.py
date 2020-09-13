from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()


with open("requirements.txt") as f:
    requirements = f.read().strip().split("\n")

with open("requirements_dev.txt") as f:
    test_requirements = f.read().strip().split("\n")

setup(
    name="twindb_table_compare",
    version="3.0.2",
    description=(
        "TwinDB Table Compare reads percona.checksums from the master and slave "
        "and shows what records are difference if there are any inconsistencies."
    ),
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    author="Aleksandr Kuzminsky",
    author_email="aleks@twindb.com",
    url="https://github.com/twindb/twindb-table-compare",
    packages=["twindb_table_compare"],
    package_dir={"twindb_table_compare": "twindb_table_compare"},
    entry_points={
        "console_scripts": ["twindb-table-compare=twindb_table_compare.cli:main"]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords="twindb_table_compare",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
