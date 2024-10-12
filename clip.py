import asyncio
import platform

# To avoid sending back items that were sent from another device
last_sent_item = None
PLATFORM = platform.system().lower()

# https://stackoverflow.com/a/62517779

async def __get_most_recent_clipboard_item():
    if PLATFORM == "windows":
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "-Command", "Get-Clipboard",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        return stdout.decode().strip()
    elif PLATFORM == "linux":
        proc = await asyncio.create_subprocess_exec(
            "which",
            "termux-clipboard-get",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        if len(stdout.decode().strip()) > 0 and stdout.decode().strip()[0] == "/":
            proc = await asyncio.create_subprocess_exec(
                "termux-clipboard-get",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, _ = await proc.communicate()
            return stdout.decode().strip()
        else:
            pass

        proc = await asyncio.create_subprocess_exec(
            "which",
            "xclip",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        if len(stdout.decode().strip()) > 0 and stdout.decode().strip()[0] == "/":
            proc = await asyncio.create_subprocess_exec(
                "xclip",
                "-sel", "clip", "-o",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, _ = await proc.communicate()
            return stdout.decode().strip()
        else:
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

async def wait_for_new_clipboard_addition():
    global last_sent_item

    last_addition = await __get_most_recent_clipboard_item()

    while True:
        current_addition = await __get_most_recent_clipboard_item()
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
    return await wait_for_new_clipboard_addition()

async def __set_most_recent_clipboard_item(item):
    if PLATFORM == "windows":
        proc = await asyncio.create_subprocess_exec(
            "powershell",
            "Set-Clipboard", "-Value", f"{item}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await proc.communicate()
    elif PLATFORM == "linux":
        proc = await asyncio.create_subprocess_exec(
            "which",
            "termux-clipboard-get",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        if len(stdout.decode().strip()) > 0 and stdout.decode().strip()[0] == "/":
            proc = await asyncio.create_subprocess_exec(
                "termux-clipboard-set",
                f"{item}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            return
        else:
            pass

        proc = await asyncio.create_subprocess_exec(
            "which",
            "xclip",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        if len(stdout.decode().strip()) > 0 and stdout.decode().strip()[0] == "/":
            proc = await asyncio.create_subprocess_exec(
                "echo",
		f"{item}", "|", "xclip", "-sel", "clip", "-i",
		stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            return
        else:
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

    await __set_most_recent_clipboard_item(item)
    last_sent_item = item
