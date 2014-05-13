from setuptools import setup

setup(
    name="LemonSync",
    version="0.1.6",
    author='LemonStand',
    author_email='chris@lemonstand.com',
    download_url='https://github.com/lemonstand/LemonSync',
    packages=['LemonSync'],
    license='LICENSE',
    description='LemonSync will listen for changes in the folder you configure, and automatically push updates to your store theme.',
    install_requires=[
        "watchdog >= 0.7.1",
        "requests >= 2.2.1",
        "boto >= 2.27.0"
    ],
	entry_points={
        'console_scripts': [
            'lemonsync = LemonSync.LemonSync:main',
        ]
    }
)