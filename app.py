import asyncio
import base64
import tempfile
from pathlib import Path
import websockets # new
import torchaudio # new 
from speechbrain.inference.speaker import SpeakerRecognition # new

# Set up "verifier" - inferrer by loading local models
# if you got "no audio backend" errors make sure you installed soundfile via pip
verification = SpeakerRecognition.from_hparams(source="pretrained_models/")

# Global var - uID to be replaced with uuid generator
# and testDict an external source (DB)

testDict = {}
uID = 1

# B64 representation of audio -> raw bytes -> waveform
# A temp file will be briefly stored but immediately deleted
def process_wav_bytes(webm_bytes: bytes):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        temp_file.write(webm_bytes)
        temp_file.flush()
        waveform, s_rate = torchaudio.load(temp_file.name)
        print(type(waveform))
        temp_file.close()
        Path.unlink(temp_file.name)
        return waveform

# Basically, cycles through the existing collection of audio
# and runs against the inferrer in pairs...
def searchDict(audio, dict_input):
    global uID
    found = False
    for k, v in dict_input.items():
        score, prediction = verification.verify_batch(v, audio) # main routine - 0.33 seems to be an okay threshold
        if score.item() >= 0.33:
            print('Hello, user {}!'.format(k))
            found = True
            break
    if not found:
        print("Not found {}".format(uID))
        dict_input[uID] = audio
        print('New user {} added!'.format(uID))
        uID += 1

# Processes message received from WS
def sr(message):
    if message:
        print('message received', len(message), type(message))
        try:
            if isinstance(message, str):
                message = base64.b64decode(message)
                audio = process_wav_bytes(bytes(message))
                # print(type(audio))
                searchDict(audio, testDict)
                
        except Exception as e:
            print(e)

async def server(ws:str, path:int):
    #inp = input('Client joined. Greet it. \nType ')
    #await ws.send(inp)
    while True:
        message = await ws.recv()
        print(message)
        sr(message)

if __name__ == "__main__":
    Server = websockets.serve(server, '127.0.0.1', 5678)
    asyncio.get_event_loop().run_until_complete(Server)
    asyncio.get_event_loop().run_forever()

