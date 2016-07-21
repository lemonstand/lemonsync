# Install Python 2.7.12 (will include necessary tools like virtualenv and pip) 

brew install python

git clone git@github.com:lemonstand/lemonsync.git

# Create new virtualenv

virtualenv lemonsync

cd lemonsync

# Activate the virtual environment

source bin/activate

# Install the dev version of pyInstaller

git clone https://github.com/pyinstaller/pyinstaller.git

cd pyinstaller

sudo python setup.py install

cd ..

pip install requests boto watchdog colorama

# In case pyInstaller was previously run

sudo rm -rf build dist

# Will create a binary in dist/

sudo pyinstaller runner --onefile

deactivate

# Rename the built binary

mv runner lemonsync

# Optional: uninstall the version of Python installed by Homebrew in the first step

brew uninstall python
