from setuptools import setup, find_packages

setup(
    name="soulprint",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "sqlalchemy"
    ],
    entry_points={
        "console_scripts": [
            "soulprint-cli = soulprint.cli:main"
        ]
    }
)
