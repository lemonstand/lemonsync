from setuptools import setup

setup(
    name="LemonSync",
    version="0.1.0",
    author='LemonStand',
    author_email='chris@lemonstand.com',
    packages=['LemonSync', 'LemonSync.tests'],
    scripts=['bin/LemonSync'],
    license='LICENSE',
    description='LemonSync will listen for changes in the folder you configure, and automatically push updates to your store theme.',
    install_requires=[
        "watchdog >= 0.7.1",
        "requests >= 2.2.1",
        "boto >= 2.27.0"
    ]
)