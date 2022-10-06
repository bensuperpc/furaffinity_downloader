# Furaffinity downloader

## _Furaffinity downloader_

[![furaffinity_downloader](https://github.com/bensuperpc/furaffinity_downloader/actions/workflows/base.yml/badge.svg)](https://github.com/bensuperpc/furaffinity_downloader/actions/workflows/base.yml)

## About

This is my script to download all the images from a furaffinity user.

## Features

- [x] FAAPI support
- [x] Parrallel download
- [x] Argument parser
- [x] Download all the images from multiple artists
- [ ] Auto update

## Screenshots

## Installation

### Requirements

- [Python 3.10](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
- [Git](https://git-scm.com/)
- [Furaffinity account](https://www.furaffinity.net/) and their A and B cookies

### Clone and config

Clone this repository to your local machine using:

```sh
git clone --recurse-submodules --remote-submodules https://github.com/bensuperpc/furaffinity_downloader.git
```

Go to the folder

```sh
cd furaffinity_downloader
```

Install the requirements:

```sh
make install
```

Set the environment variables:

```sh
echo "COOKIE_A=<Your A cookie>" >> .env
```

```sh
echo "COOKIE_B=<Your B cookie>" >> .env
```

Now, the `.env` file should look like this:

```sh
COOKIE_A=45fd5sf4-f545-88f7-sdf9-e7gfhh8f7h2h
COOKIE_B=sfsfsff5-4f5s-3dfd-5df5-1v5b4d4b8aet
```

_Is not my real tokens :D_

## Usage

```sh
python furaffinity.py --artists efaru fellfallow --jobs 32
```

## Build with

- [FAAPI](https://github.com/FurryCoders/FAAPI)
- [Loguru](https://github.com/Delgan/loguru)
- [Python 3.10](https://www.python.org/)
- [Gnu Make](https://www.gnu.org/software/make/)
- [Github Actions](https://docs.github.com/en/actions)

## License

[License](LICENSE)
