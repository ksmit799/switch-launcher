# Switch Launcher ![](https://img.shields.io/badge/release-0.1.0-green.svg) ![](https://img.shields.io/github/issues/Trapdoor-NX/switch-launcher.svg) ![](https://img.shields.io/github/license/Trapdoor-NX/switch-launcher.svg)

Switch Launcher is a desktop GUI application for injecting custom payloads into Tegra X1 devices (specifically, the Nintendo Switch). The specifics of the exploit can be found in several write ups from sources such as ReSwitched, fail0verflow, etc. In short, once the device has been put into RCM mode (we have USB access) we are able to inject arbitrary unsigned code into the bootROM. This opens up the possibility of CFW (Custom Firmware) and Homebrew. Unless you make changes to the Switch's operating system itself (or within its scope), Nintendo will never be the wiser to the fact that you have made use of this exploit.

## Requirements

#### Python 3
Switch Launcher has been developed to work with Python 3 **ONLY**. You can download Python 3 [here](https://www.python.org/downloads/). If you are not a developer however, you can just download a pre-built binary for your respective system from below.

#### Python Requirements
You can install all the requirements that Python itself requires by executing the following command (while at the root of the repo).
```
pip install -r requirements.txt
```

#### Native Requirements
PyUSB requires a backend in order to function properly. These backends are OS specific, install instructions for each OS can be found below.

##### Windows
TODO

##### MacOS
Once you have brew installed (you can install it [here](https://brew.sh)) you can execute the following command.
```
brew install libusb
```

##### Linux
From terminal, you can execute the following command.
```
sudo apt-get install libusb-1.0-0-dev
```

## Pre-built Binaries
Pre-built binaries will be available soon.

## Contributing
When committing, make sure to follow the general commit format "(FILE): (DESCRIPTION)". Try to be as descriptive as possible and make use of the comment system.
