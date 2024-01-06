from setuptools import setup, find_packages
from setuptools.command.install import install
import os


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        os.system("logging-api init")


setup(
    name="logging_api",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask", "flask_sqlalchemy", "click", "requests"],
    cmdclass={
        "install": PostInstallCommand,
    },
    entry_points="""
    [console_scripts]
    logging-api=your_package.cli:cli
    logging-api-init=your_package.cli:init
""",
)
