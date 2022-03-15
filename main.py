from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import asyncio
import json
import re


SetLogLevel(0)

if not os.path.exists("model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    exit (1)

#wf = wave.open(sys.argv[1], "rb")
#if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
#    print ("Audio file must be WAV format mono PCM.")
#    exit (1)


def make_text(filepath):
    wf = wave.open(filepath, 'rb')
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        return
    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    result = str()

    read_block_size = 4000

    while True:
        data = wf.readframes(read_block_size)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
        
            if res['text'] != '':
                result += f" {res['text']}"
                if read_block_size < 200000:
                    print(res['text'] + " \n")
                
                last_n = False
            elif not last_n:
                result += '\n'
                last_n = True

    #print(rec.FinalResult())
    res = json.loads(rec.FinalResult())
    result += f" {res['text']}"

    with open('text.txt', 'w') as fp:
        fp.write('\n'.join(line.strip() for line in re.findall(r'.{1,150}(?:\s+|$)', result)))
