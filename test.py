# sensor_server.py

import asyncio
import json
import random
import websockets

# 포트 번호
PORT = 8080

# 클라이언트에 가상의 센서 데이터를 보내는 함수
async def simulate_sensor(websocket, path):  # ← 반드시 이 두 인자 필요!
    print(f"🔌 클라이언트 연결됨: {path}")
    try:
        while True:
            # 랜덤 센서 값 생성
            data = {
                "distance": round(random.uniform(20, 100), 2),
                "light": random.randint(200, 1023)
            }
            # 클라이언트에 전송
            await websocket.send(json.dumps(data))
            await asyncio.sleep(0.1)
    except websockets.exceptions.ConnectionClosed:
        print("❌ 연결 종료됨")

# 메인 이벤트 루프
async def main():
    print(f"🌐 WebSocket 서버 실행 중: ws://localhost:{PORT}")
    async with websockets.serve(simulate_sensor, "0.0.0.0", PORT):
        await asyncio.Future()  # 종료 방지용 무한 대기

# 프로그램 실행
if __name__ == "__main__":
    asyncio.run(main())
