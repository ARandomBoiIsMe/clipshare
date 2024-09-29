import threading

import config
import connection

CONFIG = config.load_config()
SUBNET_MASK = CONFIG['NETWORK']['SUBNET_MASK']

IP_ADDRESS = connection.get_ip_address()
PORT = connection.get_port()
BROADCAST_ADDRESS = connection.get_broadcast_address(IP_ADDRESS, SUBNET_MASK)

def main():
    threading.Thread(target=connection.listen, args=(IP_ADDRESS, PORT)).start()
    threading.Thread(target=connection.send, args=(BROADCAST_ADDRESS,)).start()

    print("Running. Copy text on this device to send it to other devices running this program...")

if __name__ == '__main__':
    main()