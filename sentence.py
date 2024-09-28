import numpy as np
from scipy.io import wavfile
from scipy.io.wavfile import write

sample_rate = 44100  # 采样率（1秒钟的字节数据量）
threshold = 200  # 声音的最小阈值
energy_value = 0.01  # 100
speak_interval = 1024 * 2 * 10  # 大概半秒的接收数据量(1024个数据（2048个字节约）0.023秒的数据)

DATA = {
    "received_data": np.array([], dtype=np.int16),
    "window_size": speak_interval,
}


class SentenceLogic:
    def __init__(self):
        self.s_time = 0
        self.flag = False  # 判断是否为分句
        self.index = 1
        self.median_energy_window_index = 0
        self.median_energy_window_size = 4
        self.median_energy_window = [0, 0, 0, 0]

    def calc_audio_energy(self):
        _max = None
        self.index += 1
        if len(DATA["received_data"]) >= speak_interval:  # 等待大于0.5秒的数据做处理
            r_d = DATA["received_data"][-DATA.get("window_size"):]
            diff = np.abs(np.diff(r_d))
            _max = np.max(diff)  # 最大的声音差量值
            mean_energy = np.mean(diff)  # 平均声音差（平均能量）
            if self.median_energy_window_index >= self.median_energy_window_size:
                self.median_energy_window_index = 0
            self.median_energy_window[self.median_energy_window_index] = mean_energy
            self.median_energy_window_index += 1
            if _max < (sum(self.median_energy_window) / len(self.median_energy_window)) + threshold:
                self.flag = True
            else:
                self.s_time += 1
                self.flag = False
        if self.flag:  # 说明可以返回句子
            if not self.s_time:  # 说明第一个数据为 静音数据，无实用数据，丢弃
                DATA["received_data"] = np.array([], dtype=np.int16)
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
            DATA["received_data"] = np.array([], dtype=np.int16)
            return r
        return np.array([])
