import traceback
import uuid

import numpy as np
from scipy.io.wavfile import write
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
import librosa
import soundfile as sf

from test.test_ws import get_test_wb_html as twh

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/ws/ws_html")
async def tws():
    return await twh()


@app.websocket("/ws_text")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            print(data)
        except WebSocketDisconnect:
            print(WebSocketDisconnect)
            break
        except Exception as e:
            print(traceback.format_exc())
            break


data = {"client-id-12345": None}
data_number = {"client-id-12345": 1}


@app.websocket("/ws_binary")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    audio_array = None
    wav_file = 1

    while True:
        try:
            client_id = websocket.headers.get('x-client-id')
            message = await websocket.receive_bytes()
            if message:
                sample_rate = 44100
                # 将接收到的二进制数据转换为 numpy 数组

                if data.get(client_id) is None:
                    data[client_id] = np.frombuffer(message, dtype=np.int16)
                else:
                    data[client_id] = np.append(data[client_id], np.frombuffer(message, dtype=np.int16))

                await websocket.send_text("client_id:{} OK".format(client_id))
                print("client_id:{},len:{}".format(client_id, data[client_id].shape[0]))
                if data[client_id].shape[0] > 2 * 44100 * 10:
                    # 保存为 WAV 文件
                    write("received_audio{}.wav".format(data_number.get(client_id, 1)), sample_rate, data[client_id])
                    data[client_id] = None
                    data_number[client_id] = data_number.get(client_id, 1) + 1

                # 读取WAV文件
                # sf.write('stereo_file.wav', np.random.randn(10, 2), 44100, 'PCM_24')
                # sf.write('record.wav', audio_array, samplerate=44100)
        except WebSocketDisconnect:
            print(WebSocketDisconnect)
            break
        except Exception as e:
            print(traceback.format_exc())
            break
