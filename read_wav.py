import librosa
import soundfile as sf
import numpy as np
from scipy.io.wavfile import write
from sentence import SentenceLogic

sample_rate = 44100
def read_wav():
    data, samplerate = sf.read('test_audio3.wav')
    # 查看数据维度和一些基础信息
    print("Data shape:", samplerate, data.shape)  # 若是立体声，则 shape 为 (n_samples, 2)
    print("First 10 audio samples:", data[:10])
    print("Max audio data:{}  Min data:{}".format(np.max(data), np.min(data)))
    # 读取前 10000 帧
    # data, samplerate = sf.read(file_path, stop=10000)
    # print("Partial Audio Data:", data)
    return data


if __name__ == '__main__':
    read_time = 0
    read_size = 1024
    d = read_wav()
    index = 1
    sl = SentenceLogic()
    for _d in range((len(d) // read_size)):
        se = sl.forecast_sentence(d[_d * read_size:_d * read_size + read_size])
        if len(se):
            print("{},se:{}".format(index, len(se)))
            if index == 2:
                print(list(se))
            # write("r_audio{}.wav".format(index), sample_rate, se)
            sf.write('ee_record_{}.wav'.format(index), se, samplerate=44100)
            index += 1
