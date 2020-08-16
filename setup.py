from setuptools import setup

setup(
    name="jeedom-flower-spray",
    version="1.0.0",
    description="Jeedom Flower Water Spray",
    url="https://github.com/loko-loko/jeedom-flower-spray.git",
    author="loko-loko",
    author_email="loko-loko@github.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["jeedom_flower_spray"],
    include_package_data=True,
    install_requires=[
        "requests",
        "loguru==0.5.0",
        "PyYAML==5.3.1"
    ],
    entry_points={
        "console_scripts": [
            "jeedom-flower-spray=jeedom_flower_spray.__main__:main",
        ]
    },
)
