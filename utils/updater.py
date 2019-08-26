# -*- coding: utf-8 -*-

import time


class Updater:
    
    def __init__(self, min_delay=0):
        self.min_delay = min_delay
        self.functions = []
        self.prev_time = time.time()
        self.timer = 0
        
    def reset_timer(self):
        self.total_time = 0
        
    def add(self, function, period=0):
        self.functions.append([function, 0, period])

    def update(self):
        current_time = time.time()
        dt = current_time - self.prev_time
        self.prev_time = current_time
        for function_data in self.functions:
            function_data[1] += dt
            if function_data[1] >= function_data[2]:
                function_data[0](function_data[1])
                function_data[1] = 0
        self.timer += dt
        time.sleep(self.min_delay)