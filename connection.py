import socket
import asyncio
import ipaddress

import clip

def get_ip_address():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.connect(("8.8.8.8", 80)) # Try to connect to Google's public DNS
            ip = sock.getsockname()[0] # Get IP that would have made that connection from your laptop
        except:
            ip = '127.0.0.1'

        return ip

def get_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        port = 1024

        while True:
            try:
                sock.bind(('0.0.0.0', port))
                return port
            except socket.error as e:
                port += 1

                if port > 1034:
                    raise ValueError("Program can only listen on ports 1024 to 1034")

                continue
            except Exception as err:
                raise err

def get_broadcast_address(ip_address, subnet_mask):
    interface = ipaddress.IPv4Interface(f"{ip_address}{subnet_mask}")

    network = interface.network
    broadcast_address = str(network.broadcast_address)

    return broadcast_address

async def listen(ip_address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65507)
        sock.bind(('0.0.0.0', port))
        sock.setblocking(False)

        print("Ready to receive data...")

        loop = asyncio.get_event_loop()
        while True:
            try:
                received_data, addr = await loop.sock_recvfrom(sock, 65507)

                if addr[0] == '127.0.0.1' or addr[0] == ip_address:
                    continue

                message = received_data.decode()

                await clip.save_to_clipboard(message)
                print(f"Received: {message}")
            except OSError as e:
                print(f"Error receiving data: {e}")
                continue

async def send(broadcast_address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65507)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.setblocking(False)

        print("Ready to send data...")

        loop = asyncio.get_event_loop()
        while True:
            message = await clip.get_from_clipboard()

            data = message.encode()

            for port in range(1024, 1035):
                await loop.sock_sendto(sock, data, (broadcast_address, port))

            print(f"Sent: {message}")