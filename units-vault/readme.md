# How to install all dependencies?

If you are on Ubuntu, follow the steps:

1. Run `sudo apt-get update`
2. Run `sudo apt-get -y install build-essential`
3. Run `sudo apt-get -y install make`
4. Install the docker following the docs [here](https://docs.docker.com/engine/install/ubuntu/)
5. Install python running `sudo apt-get install python3`
6. Install pip running `sudo apt-get install python3-pip`
7. On dir of this repository, run `make install-linux`

If you are on Windows, follow the steps:

1. Install the [Chocolatey](https://chocolatey.org/)
2. Install the make with the command `choco install make`
3. Install the docker following the docs [here](https://docs.docker.com/desktop/install/windows-install/)
4. Install the python [here](https://www.python.org/downloads/)
5. On dir of this repository, run `make install-win`

# How to start for development?

Just run `make dev`
