import os,pyaudio,math,wave,audioop,sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
std_out = os.dup(2)
f =  os.open('/dev/null',os.O_WRONLY)
os.dup2(f,2)

from collections import deque
from pocketsphinx.pocketsphinx import *

def print2(test):
    os.dup2(std_out, 2)
    print(test)
    os.dup2(f,2)

class SpeechDetector:
    def __init__(self):

        # Конфигурация микрофона
        self.CHUNK = 1024  # CHUNKS - число байт, считываемое каждый раз с микрофона
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1 #кол-во каналов 1-моно 2-стерео
        self.RATE = 16000 #частота
        self.SILENCE_LIMIT = 2
        self.PREV_AUDIO = 2
        self.THRESHOLD = 3500
        self.num_phrases = -1

        # Конфигурируем декодер
        config = Decoder.default_config()
        config.set_string('-hmm', '/home/alex/speech/adapting/ru-ru-adapted')
        config.set_string('-lm', '/home/alex/speech/adapting/ru_kb.lm')
        config.set_string('-dict', '/home/alex/speech/adapting/ru.dic')

        # Создаем декодер
        self.decoder = Decoder(config)

    def setup_mic(self, num_samples=50):
        """ Получает среднюю интенсивность аудиопотока с микрофона
            для того, чтобы определять идет разговор или нет
        """
        print2("Настраиваю микрофон...")
        self.speak(" Настраиваю микрофон ")

        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(self.CHUNK), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)

        print2("Закончили настройку.")
        self.speak(" Закончили настройку ")
        print2(" Средняя интенсивность аудио-потока: " + str(r))

        stream.close()
        p.terminate()

        if r < 3000:
            self.THRESHOLD = 3000
        else:
            self.THRESHOLD = r + 105

    def save_speech(self, data, p):
        #сохраняем аудио-поток в файл

        waveFile = wave.open("File.wav", 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(p.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(data))
        waveFile.close()

        return 'File.wav'

    def decode_phrase(self, wav_file):
        #декодируем из файла в массив н-лучших

        self.decoder.start_utt()
        stream = open(wav_file, "rb")
        while True:
          buf = stream.read(1024)
          if buf:
            self.decoder.process_raw(buf, False, False)
          else:
            break
        self.decoder.end_utt()
        words = []
        [words.append(seg.word) for seg in self.decoder.seg()]
        return [n.hypstr for n in self.decoder.nbest()]

    def speak(self,phrase):
        os.system("echo "" " + phrase + " "" | RHVoice-test -p Irina")

    def run(self):

        #self.setup_mic()
        #Открываем поток

        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        print2("* Микрофон в режиме ожидания ")
        self.speak(" Микрофон в режиме ожидания ")
        audio2send = []
        cur_data = ''  # current chunk of audio data
        rel = int(self.RATE/self.CHUNK)
        slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)

        #Прикрепляем спереди аудио длиной 2сек
        prev_audio = deque(maxlen=self.PREV_AUDIO * rel)
        started = False

        while True:

            cur_data = stream.read(self.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            
            if sum([x > self.THRESHOLD for x in slid_win]) > 0:
                if started == False:
                    print2 (" Начало записи фразы ")
                    started = True
                audio2send.append(cur_data)

            elif started:
                print2 ("Конец записи, идёт распознавание")
                self.speak(" Конец записи, идёт распознавание ")
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                r = self.decode_phrase(filename)
                print2 ("Распознано: " + str(r[0]))
                #phrase = "Вы сказали: " + str(r[0])
                self.speak(phrase)
                # Удаляет файл
                os.remove(filename)
                stream.stop_stream()
                stream.close()
                p.terminate()

                return str(r[0])
                # Reset all
                started = False
                slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
                prev_audio = deque(maxlen=self.PREV_AUDIO * rel)
                audio2send = []
                print2 ("Слушаю ...")
                self.speak(" Слушаю ")
            else:
                prev_audio.append(cur_data)

        print2 ("* Закончили слушать")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    sd = SpeechDetector()
    sd.run()


