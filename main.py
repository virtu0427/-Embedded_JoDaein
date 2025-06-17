import asyncio
import websockets
import json
import time
import RPi.GPIO as GPIO
import spidev

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trig = 23
echo = 24
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 100000
ldr_channel = 0

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def get_distance():
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2
    return round(distance, 2)

PORT = 8080

async def send_sensor_data(websocket):
    print(f"클라이언트 연결: {websocket.remote_address}")
    try:
        while True:
            distance = get_distance()
            light = readadc(ldr_channel)

            sensor_data = {
                "distance": distance,
                "light": light
            }

            await websocket.send(json.dumps(sensor_data))
            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosed:
        print("연결 종료")

async def main():
    print(f"WebSocket 서버 시작: ws://0.0.0.0:{PORT}")
    async with websockets.serve(send_sensor_data, "0.0.0.0", PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("종료")
        GPIO.cleanup()
