from setuptools import setup

setup(
    name="lemonsync",
    version="0.1.12",
    author='LemonStand',
    author_email='chris@lemonstand.com',
    url='http://pypi.python.org/lemonstand/lemonsync',
    download_url='https://github.com/lemonstand/lemonsync',
    packages=['lemonsync'],
    description='LemonSync will listen for changes in the folder you configure, and automatically push updates to your store theme.',
    install_requires=[
        "watchdog >= 0.7.1",
        "requests >= 2.2.1",
        "boto >= 2.27.0",
        "colorama >= 0.3.1",
        'pathtools >=0.1.1'
    ],
	entry_points={
        'console_scripts': [
            'lemonsync = lemonsync.LemonSync:main',
        ]
    },
	license = "MIT",
	platforms = "Posix; MacOS X; Windows",
	classifiers = ["Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Internet",
		"Programming Language :: Python :: 2.7"
    ]
)