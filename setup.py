from setuptools import setup

setup(
    name="jeedom-flower-watering",
    version="1.0.0",
    description="Watering using Jeedom and get moisture level from Mi Flower Exporter",
    url="https://github.com/loko-loko/jeedom-flower-watering.git",
    author="loko-loko",
    author_email="loko-loko@github.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["jeedom_flower_watering"],
    include_package_data=True,
    install_requires=[
        "requests",
        "loguru==0.5.0",
        "PyYAML==5.4"
    ],
    entry_points={
        "console_scripts": [
            "jeedom-flower-watering=jeedom_flower_watering.__main__:main",
        ]
    },
)
