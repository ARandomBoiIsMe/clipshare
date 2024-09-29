import struct
import socket
import ipaddress

import clip

def get_ip_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.connect(("8.8.8.8", 80)) # Try to connect to Google's public DNS
        ip = sock.getsockname()[0] # Get IP that would have made that connection from your laptop
    except:
        ip = '127.0.0.1'
    finally:
        sock.close()

    return ip

def get_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 1024

    while True:
        try:
            sock.bind(('0.0.0.0', port))
            return port
        except socket.error as e:
            port += 1

            if port > 1034:
                raise ValueError("program can only listen on ports 1024 to 1034")

            continue
        except Exception as err:
            raise err
        finally:
            sock.close()

def get_broadcast_address(ip_address, subnet_mask):
    interface = ipaddress.IPv4Interface(f"{ip_address}{subnet_mask}")

    network = interface.network
    broadcast_address = str(network.broadcast_address)

    return broadcast_address

def listen(broadcast_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))

    print("Ready to receive data...")

    while True:
        data_size = struct.unpack("L", sock.recv(struct.calcsize("L")))[0]

        received_data = b""
        while len(received_data) < data_size:
            received_data += sock.recvfrom(4096)[0]

        message = received_data.decode()
        clip.save_to_clipboard(message)

        print(f"Received: {message}")

def send(broadcast_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print("Ready to send data...")

    while True:
        message = clip.get_from_clipboard()

        port = 1024
        while True:
            if port > 1034:
                break

            data = message.encode()
            message_size = struct.pack("L", len(data))

            sock.sendto(message_size + data, (broadcast_address, port))
            port += 1

        print(f"Sent: {message}")