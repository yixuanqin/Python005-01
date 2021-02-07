import queue
import threading
import time
import random
 
class CountDownLatch:
    def __init__(self, count):
        self.count = count
        self.condition = threading.Condition()

    def wait(self):
        try:
            self.condition.acquire()
            while self.count > 0:
                self.condition.wait()
        finally:
            self.condition.release()

    def count_down(self):
        try:
            self.condition.acquire()
            self.count -= 1
            self.condition.notifyAll()
        finally:
            self.condition.release()
 
class DiningPhilosophers(threading.Thread):
    def __init__(self, philosopher_number, left_fork, right_fork, dining_queue, count_latch):
        super().__init__()
        self.philosopher_number = philosopher_number
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.dining_queue = dining_queue
        self.count_latch = count_latch
 
    def eat(self):
        time.sleep(0.01)
        self.dining_queue.put([self.philosopher_number, 0, 3])
 
    def think(self):
        time.sleep(random.random())
 
    def pickLeftFork(self):
        self.dining_queue.put([self.philosopher_number, 1, 1])

    def pickRightFork(self):
        self.dining_queue.put([self.philosopher_number, 2, 1])

    def putLeftFork(self):
        self.left_fork.release()
        self.dining_queue.put([self.philosopher_number, 1, 2])

    def putRightFork(self):
        self.right_fork.release()
        self.dining_queue.put([self.philosopher_number, 2, 2])

    def run(self):
        while True:
            left = self.left_fork.acquire(blocking = False)
            right = self.right_fork.acquire(blocking = False)
            if left and right:
                self.pickLeftFork()
                self.pickRightFork()
                self.eat()
                self.putLeftFork()
                self.putRightFork()
                break
            elif left and not right:
                self.left_fork.release()
            elif right and not left:
                self.right_fork.release()
            else:
                self.think()
        print(str(self.philosopher_number) + ' count_down')
        self.count_latch.count_down()

if __name__ == '__main__':
    dining_queue = queue.Queue()
    fork1 = threading.Lock()
    fork2 = threading.Lock()
    fork3 = threading.Lock()
    fork4 = threading.Lock()
    fork5 = threading.Lock()
    n = 1
    latch = CountDownLatch(5 * n)
    for _ in range(n):
        philosopher0 = DiningPhilosophers(0, fork5, fork1, dining_queue, latch)
        philosopher0.start()
        philosopher1 = DiningPhilosophers(1, fork1, fork2, dining_queue, latch)
        philosopher1.start()
        philosopher2 = DiningPhilosophers(2, fork2, fork3, dining_queue, latch)
        philosopher2.start()
        philosopher3 = DiningPhilosophers(3, fork3, fork4, dining_queue, latch)
        philosopher3.start()
        philosopher4 = DiningPhilosophers(4, fork4, fork5, dining_queue, latch)
        philosopher4.start()
    latch.wait()
    queue_list = []
    for i in range(5 * 5 * n):
        queue_list.append(dining_queue.get())
    print(queue_list)