import threading
import time
import cv2
import os
import base64
import copy
import parameters
import numpy as np
import simpleaudio as sa

def play_alarm_thread(name, count):
    filename = os.path.dirname(os.path.realpath(__file__)) + '/../resources/scary.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def play_alarm():
    thread = threading.Thread(target=play_alarm_thread, args=("Play alarm thread", 0))
    thread.start()

class Video:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        #self.foreground_mask = None

    def next_frame(self):
        still_going, cv2_frame = self.video.read()

        if still_going:
            frame = cv2_frame
            return frame
        else:
            return None

    def get_sizes(self):
        frame = self.next_frame()
        if frame is not None:
            return frame.shape[0], frame.shape[1]
        else:
            return 0, 0


class FrameProcessor:

    # approximately 0.4 seconds to complete processing

    def __init__(self, frame, last_frame, parent, index):
        self.frame = frame
        self.last_frame = last_frame
        self.parent = parent
        self.thread = threading.Thread(target=self.start_thread, args=("Process thread " + str(index), self))

    @staticmethod
    def start_thread(name, master):
        print(name + " started...")
        blurred = cv2.GaussianBlur(master.frame, parameters.PROCESS_GAUSSIAN_BLUR_SIZE, parameters.PROCESS_GAUSSIAN_SIGMA_X)
        if master.last_frame is not None:
            differential = cv2.absdiff(master.frame, master.last_frame)
        else:
            differential = cv2.absdiff(master.frame, master.frame)

        differential_mask = cv2.inRange(differential, parameters.PROCESS_LOWER_THRESHOLD, parameters.PROCESS_UPPER_THRESHOLD)

        master.parent.video_access.acquire()
        foreground_mask = master.parent.video.background_subtractor.apply(blurred)
        master.parent.video_access.release()

        master.parent.cumulative_access.acquire()
        master.parent.cumulative = np.subtract(master.parent.cumulative, master.parent.cumulative_extraction)
        master.parent.cumulative = np.clip(master.parent.cumulative, a_min=parameters.PROCESS_LOWER_MEMORY, a_max=parameters.PROCESS_UPPER_MEMORY)

        masked_addition_matrix_normal = cv2.bitwise_and(master.parent.cumulative_addition_normal, master.parent.cumulative_addition_normal, mask=differential_mask)
        master.parent.cumulative = np.add(master.parent.cumulative, masked_addition_matrix_normal)

        masked_addition_matrix_foreground = cv2.bitwise_and(master.parent.cumulative_addition_foreground, master.parent.cumulative_addition_foreground, mask=foreground_mask)
        master.parent.cumulative = np.add(master.parent.cumulative, masked_addition_matrix_foreground)

        cumulative_restrained = np.clip(master.parent.cumulative, a_min=0, a_max=255)
        cumulative_restrained = cumulative_restrained.astype(np.uint8)
        master.parent.cumulative_access.release()

        detection_matrix_pure = cv2.bitwise_and(master.frame, master.frame, mask=cumulative_restrained)

        detection_matrix = cv2.filter2D(detection_matrix_pure, -1, kernel=parameters.PROCESS_DETECTION_KERNEL)
        detection_matrix = cv2.divide(detection_matrix, parameters.PROCESS_DETECTION_KERNEL_TOTAL)

        detection_number = np.count_nonzero(detection_matrix)

        master.parent.movement_factor_access.acquire()
        master.parent.movement_factor = detection_number
        master.parent.movement_active = detection_number >= parameters.MOVEMENT_ACTIVE_THRESHOLD
        if master.parent.movement_active:
            master.parent.active_access.acquire()
            if master.parent.active:
                play_alarm()
            master.parent.active_access.release()
        master.parent.movement_factor_access.release()

        master.parent.altered_access.acquire()
        master.parent.altered = detection_matrix_pure
        if master.parent.altered is not None:
            retrieved, buffer = cv2.imencode('.png', master.parent.altered)
            master.parent.altered_base64 = base64.b64encode(buffer)
        master.parent.altered_access.release()

        print(name + " finished...")

    def run(self):
        self.thread.start()


class Worker:
    def __init__(self):
        self.start_time = time.time()

        self.video_access = threading.Condition()
        self.video = Video()
        self.sizes = self.video.get_sizes()

        self.active = False
        self.active_access = threading.Condition()

        self.frame_access = threading.Condition()
        self.frame = None
        self.last_frame = None
        self.frame_base64 = None

        self.altered_access = threading.Condition()
        self.altered = None
        self.altered_base64 = None

        self.movement_factor_access = threading.Condition()
        self.movement_factor = 0
        self.movement_active = False

        self.cumulative_access = threading.Condition()
        self.cumulative = np.zeros((self.sizes[0], self.sizes[1]), np.int16)
        self.cumulative_extraction = np.multiply(np.ones((self.sizes[0], self.sizes[1]), np.int16), parameters.PROCESS_EXTRACTION)
        self.cumulative_addition_normal = np.multiply(np.ones((self.sizes[0], self.sizes[1]), np.int16), parameters.PROCESS_ADDITION_NORMAL)
        self.cumulative_addition_foreground = np.multiply(np.ones((self.sizes[0], self.sizes[1]), np.int16), parameters.PROCESS_ADDITION_FOREGROUND)

        self.self_path = os.path.dirname(os.path.realpath(__file__))
        self.is_running = False
        self.sleep_time = 0.9

        self.thread = threading.Thread(target=self.start_thread, args=("Worker thread", self))

        self.process_index = 0

    @staticmethod
    def start_thread(name, master):
        print(name + " started...")
        while master.is_running:
            master.update()
            time.sleep(master.sleep_time)

    def update(self):
        self.frame_access.acquire()
        self.frame = self.video.next_frame()
        self.frame_base64 = None
        if self.frame is not None:
            frame = copy.copy(self.frame)
            frame = cv2.putText(frame, time.strftime("%b %d %Y %H:%M:%S", time.gmtime(time.time())), (self.sizes[1] - 200, self.sizes[0] - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, 1)
            retrieved, buffer = cv2.imencode('.png', frame)
            self.frame_base64 = base64.b64encode(buffer)

        frame_processor = FrameProcessor(copy.copy(self.frame), copy.copy(self.last_frame), self, self.process_index)
        self.process_index += 1

        self.last_frame = self.frame
        self.frame_access.release()

        frame_processor.run()

    def run(self):
        self.is_running = True
        self.thread.start()
