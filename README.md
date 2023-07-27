# Furaffinity downloader

## _Furaffinity downloader_

[![furaffinity_downloader](https://github.com/bensuperpc/furaffinity_downloader/actions/workflows/base.yml/badge.svg)](https://github.com/bensuperpc/furaffinity_downloader/actions/workflows/base.yml)

## About

This is my script to download all the images from a furaffinity artists/users.

## Features

- [x] FAAPI support
- [x] Download image with json (with tags, type, gender etc...)
- [x] Parrallel download (Pool thread)
- [x] Argument parser
- [x] Download all the images from multiple artists
- [x] Download all the images from file
- [x] Automatic retry on fail
- [ ] Partial update
- [ ] Optimize download speed
- [ ] Auto update

## Tests
- [x] Empty artists list
- [x] Timeout
- [x] Download during 7 days (and 246 Go data)


## Screenshots

## Installation

### Requirements

- [Python 3.10](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
- [Git](https://git-scm.com/)
- [Furaffinity account](https://www.furaffinity.net/) and their A and B cookies (You can get with F12 key)

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

### From arguments

```sh
python furaffinity.py --artists efaru fellfallow # Great artists, i recommend you support them ^^
```

### From file

```sh
cat echo "efaru\nfellfallow" > artists.txt
```

```sh
python furaffinity.py --file artists.txt # One artist per line
```

## Build with

- [FAAPI](https://github.com/FurryCoders/FAAPI)
- [Loguru](https://github.com/Delgan/loguru)
- [Python 3.10](https://www.python.org/)
- [Gnu Make](https://www.gnu.org/software/make/)
- [Github Actions](https://docs.github.com/en/actions)

## Important

I am not responsible for the use that may be made of this software.

## License

[License](LICENSE)

