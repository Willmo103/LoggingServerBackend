from setuptools import setup, find_packages

setup(
    name="logging_api",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["flask", "flask_sqlalchemy"],
)
