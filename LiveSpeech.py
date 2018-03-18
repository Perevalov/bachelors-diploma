import os
from os import path
from pocketsphinx import LiveSpeech, get_model_path

MODELDIR = "model/ru"

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.abspath(path.join(MODELDIR, '')),
    lm=os.path.abspath(path.join(MODELDIR, 'ru.lm')),
    dic=os.path.abspath(path.join(MODELDIR, 'ru.dic '))
)

for phrase in speech:
    print(phrase)
