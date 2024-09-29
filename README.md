# clipshare

A program for sharing data between clipboards on multiple devices.

## Configuration

### Windows

None. Just make sure you have [python](https://www.python.org/downloads/) installed before running the program.

### Linux

Install the `xclip` program to allow access to the clipboard:

```
sudo apt install xclip
```

Make sure you have [python](https://www.python.org/downloads/) installed before running the program.

### Android

- Download and install [Termux](https://termux.dev/en/)
- Download and install [Termux:API](https://f-droid.org/packages/com.termux.api/)
- Install the `termux-api` package:

```
pkg install termux-api
```

- Install Python:

```
pkg install python
```

## Usage

Run the program on all devices where you want to share clipboard data:

```
python main.py
```

Once the program is running on all devices, you can copy text or other data on one device. This data will be available to paste on any other connected device running `clipshare`.

## Supported devices:

- Android
- Windows
- Linux