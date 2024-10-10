import asyncio
import platform

# To avoid sending back items that were sent from another device
last_sent_item = None

# https://stackoverflow.com/a/62517779

async def __get_most_recent_clipboard_item(sys):
    if sys == "windows":
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "-Command", "Get-Clipboard",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        return stdout.decode().strip()
    elif sys == "linux":
        # Linux on PC
        proc = await asyncio.create_subprocess_exec(
            "xclip",
            "-sel", "clip", "-o",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if stderr:
            pass
        elif stdout:
            return stdout.decode().strip()

        # Termux on Android
        proc = await asyncio.create_subprocess_exec(
            "termux-clipboard-get",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if stderr:
            pass
        elif stdout:
            return stdout.decode().strip()

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

async def wait_for_new_clipboard_addition(sys):
    global last_sent_item

    last_addition = await __get_most_recent_clipboard_item(sys)

    while True:
        current_addition = await __get_most_recent_clipboard_item(sys)
        if current_addition == last_addition:
            await asyncio.sleep(0.5)
            continue

        if current_addition == last_sent_item:
            await asyncio.sleep(0.5)
            continue

        if type(current_addition) != str:
            await asyncio.sleep(0.5)
            continue

        return current_addition

async def get_from_clipboard():
    plat = platform.system().lower()

    return await wait_for_new_clipboard_addition(plat)

async def __set_most_recent_clipboard_item(sys, item):
    if sys == "windows":
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "Set-Clipboard", "-Value", f"{item}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await proc.communicate()
    elif sys == "linux":
        # Linux on PC
        proc = await asyncio.create_subprocess_exec(
            "echo"
            f"{item}", "|", "xclip",
            "-sel", "clip",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()
        if stderr:
            pass

        # Termux on Android
        proc = await asyncio.create_subprocess_exec(
            "termux-clipboard-set",
            f"{item}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()
        if stderr:
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

async def save_to_clipboard(item):
    global last_sent_item
    plat = platform.system().lower()

    await __set_most_recent_clipboard_item(plat, item)
    last_sent_item = item