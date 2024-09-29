import time
import platform
import subprocess

# To avoid sending back items that were sent from another device
last_sent_item = None

# https://stackoverflow.com/a/62517779

def __get_most_recent_clipboard_item(sys):
    if sys == "windows":
        return subprocess.run(
            args=["powershell", "Get-Clipboard"],
            capture_output=True,
            text=True
        ).stdout.strip()
    elif sys == "linux":
        # Linux on PC
        try:
            return subprocess.run(
                args=["xclip", "-sel", "clip", "-o"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
        except subprocess.CalledProcessError:
            pass

        # Termux on Android
        try:
            return subprocess.run(
                args=["termux-clipboard-get"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()
        except subprocess.CalledProcessError:
            pass

        raise ValueError(
            "This program cannot work without xclip or termux available on the target device \
            Either use a supported OS, install the needed programs, or open an issue on the repository, \
            asking for support: \
            https://github.com/ARandomBoiIsMe/clipshare/issues"
        )
    else:
        raise ValueError(
            "This OS is not supported. Open an issue on the repository, asking for support: \
            https://github.com/ARandomBoiIsMe/clipshare/issues"
        )

def wait_for_new_clipboard_addition(sys):
    global last_sent_item

    last_addition = __get_most_recent_clipboard_item(sys)

    while True:
        current_addition = __get_most_recent_clipboard_item(sys)
        if current_addition == last_addition:
            time.sleep(0.5)
            continue

        if current_addition == last_sent_item:
            time.sleep(0.5)
            continue

        if type(current_addition) != str:
            time.sleep(0.5)
            continue

        return current_addition

def get_from_clipboard():
    plat = platform.system().lower()

    return wait_for_new_clipboard_addition(plat)

def __set_most_recent_clipboard_item(sys, item):
    if sys == "windows":
        return subprocess.run(
            args=["powershell", "Set-Clipboard", "-Value", item],
            capture_output=True,
            text=True
        )
    elif sys == "linux":
        # Linux on PC
        try:
            return subprocess.run(
                args=["xclip", "-sel", "clip"],
                input=item,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError:
            pass

        # Termux on Android
        try:
            return subprocess.run(
                args=["termux-clipboard-set", item],
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError:
            pass

        raise ValueError(
            "This program cannot work without xclip or termux available on the target device \
            Either use a supported OS, install the needed programs, or open an issue on the repository, \
            asking for support: \
            https://github.com/ARandomBoiIsMe/clipshare/issues"
        )
    else:
        raise ValueError(
            "This OS is not supported. Open an issue on the repository, asking for support: \
            https://github.com/ARandomBoiIsMe/clipshare/issues"
        )

def save_to_clipboard(item):
    global last_sent_item
    plat = platform.system().lower()

    __set_most_recent_clipboard_item(plat, item)
    last_sent_item = item