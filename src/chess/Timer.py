from threading import Thread
from time import sleep
from typing import Callable

class Timer(Thread):
    def __init__(self, time:int, tick_func:Callable, complete_func: Callable) -> None:
        super(Timer, self).__init__(daemon=True)
        self.timer = time
        self.paused = False
        self.kill_timer = False
        self.tick_func = tick_func
        self.complete_func = complete_func

    def run(self) -> None: 
        while self.timer >= 1:
            if self.kill_timer:
                break

            if self.paused:
                sleep(0.5)
                continue

            self.timer -= 1
            self.tick_func(self.timer)
            sleep(1)
        else:
            self.complete_func()

    def stopTimer(self) -> None:
        self.paused = True

    def startTimer(self) -> None:
        self.paused = False

    def killTimer(self) -> None:
        self.kill_timer = True
