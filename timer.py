import time
import math

class Timer:
    def __init__(self) -> None:
        self.cumulative_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.time_delta = time.time() - self.start_time
        self.cumulative_time += self.time_delta

    def stop_detailed(self, string: str):
        self.stop(string)
        self.seconds_to_dhms(self.time_delta)

    def info(self, string: str):
        print('elapsed time = {:.2f}'.format(self.cumulative_time) + ' seconds in ' + string)
        self.seconds_to_dhms(self.cumulative_time)

    def seconds_to_dhms(self, seconds):
        d_ref = 86400
        h_ref =  3600
        m_ref =    60
        d = math.floor(seconds / d_ref)
        smd = seconds - d*d_ref
        h = math.floor(smd / h_ref)
        smdmh = smd - h*h_ref
        m = math.floor(smdmh / m_ref)
        s = smdmh - m*m_ref
        print('{} days {} hours {} minutes {:.2f} seconds'.format(d, h, m, s))