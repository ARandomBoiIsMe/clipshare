import asyncio

import config
import connection

CONFIG = config.load_config()
SUBNET_MASK = CONFIG['NETWORK']['SUBNET_MASK']

IP_ADDRESS = connection.get_ip_address()
PORT = connection.get_port()
BROADCAST_ADDRESS = connection.get_broadcast_address(IP_ADDRESS, SUBNET_MASK)

async def main():
    await asyncio.gather(
        connection.listen(IP_ADDRESS, PORT),
        connection.send(BROADCAST_ADDRESS)
    )

if __name__ == '__main__':
    asyncio.run(main())