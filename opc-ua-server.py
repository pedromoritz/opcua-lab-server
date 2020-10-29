import sys
import Adafruit_DHT
import logging
import asyncio

from asyncua import ua, Server
from asyncua.common.methods import uamethod

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')

@uamethod
def func(parent, value):
    return value * 2

async def main():
    server = Server()
    await server.init()
    server.set_endpoint('opc.tcp://192.168.0.100:4840/opcua/')
    server.set_server_name("OPC-UA Server")

    uri = 'http://devnetiot.com/opcua/'
    idx = await server.register_namespace(uri)

    obj_plc = await server.nodes.objects.add_object(idx, 'PLC')
    var_temperature = await obj_plc.add_variable(idx, 'temperature', 0)
    var_humidity = await obj_plc.add_variable(idx, 'humidity', 0)

    _logger.info('Starting server!')
    async with server:
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 25)
            _logger.info(temperature)
            await var_temperature.write_value(float(temperature))
            await var_humidity.write_value(float(humidity))
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
