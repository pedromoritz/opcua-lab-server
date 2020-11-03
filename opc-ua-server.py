import sys
import Adafruit_DHT
import logging
import asyncio

from asyncua import ua, Server
from asyncua.common.methods import uamethod

DHT_DATA_PIN = 25
DHT_READ_TIMEOUT = 2

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
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT_DATA_PIN)

            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
                await var_temperature.write_value(float(temperature))
                await var_humidity.write_value(float(humidity))
            else:
                print('Failed to get DHT11 Reading, trying again in ', DHT_READ_TIMEOUT, 'seconds')

            await asyncio.sleep(DHT_READ_TIMEOUT)

if __name__ == '__main__':
    asyncio.run(main())
