import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write

sample_rate = 44100  # 采样率（1秒钟的字节数据量）
audio_value = 0.02  # 300
energy_value = 0.01  # 100
speak_interval = 1024 * 2 * 10  # 大概半秒的接收数据量
DATA = {
    "received_data": np.array([]),
    "window_size": speak_interval,
}


class SentenceLogic:
    def __init__(self):
        self.s_time = 0
        self.flag = False  # 判断是否为分句
        self.index = 1

    def calc_audio_energy(self):
        _max = None
        self.index += 1
        if len(DATA["received_data"]) >= speak_interval:  # 等待大于0.5秒的数据做处理
            r_d = DATA["received_data"][-DATA.get("window_size"):]
            diff = np.abs(np.diff(r_d))
            _max = np.max(diff)  # 最大的声音参量值
            # threshold_value = np.median(diff)
            if _max < audio_value:
                self.flag = True
            else:
                self.s_time += 1
                self.flag = False
        if self.flag:  # 说明可以返回句子
            if not self.s_time:  # 说明第一个数据为 静音数据，无实用数据，丢弃
                DATA["received_data"] = np.array([])
                self.flag = False
                return None
            self.s_time = 0
            return True  # 有实用数据
        return None

    def forecast_sentence(self, data):
        # print(data)
        DATA["received_data"] = np.append(DATA["received_data"], data)
        if self.calc_audio_energy():
            r = DATA["received_data"]
            DATA["received_data"] = np.array([])
            return r
        return []
