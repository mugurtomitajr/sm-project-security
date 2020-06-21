import numpy as np

PROCESS_GAUSSIAN_BLUR_SIZE = (5, 5)
PROCESS_GAUSSIAN_SIGMA_X = 0

PROCESS_DIFFERENTIAL_THRESHOLD = 10

PROCESS_LOWER_THRESHOLD = np.array([PROCESS_DIFFERENTIAL_THRESHOLD, PROCESS_DIFFERENTIAL_THRESHOLD, PROCESS_DIFFERENTIAL_THRESHOLD], dtype="uint8")
PROCESS_UPPER_THRESHOLD = np.array([255, 255, 255], dtype="uint8")

PROCESS_UPPER_MEMORY = 255
PROCESS_LOWER_MEMORY = -3

PROCESS_EXTRACTION = 2
PROCESS_ADDITION_NORMAL = 1
PROCESS_ADDITION_FOREGROUND = 2

PROCESS_DETECTION_KERNEL = np.array([[1, 1, 1, 1, 1, 1, 1, 1],
                                    [1, 2, 2, 2, 2, 2, 2, 1],
                                    [1, 2, 3, 3, 3, 3, 2, 1],
                                    [1, 2, 3, 4, 4, 3, 2, 1],
                                    [1, 2, 3, 4, 4, 3, 2, 1],
                                    [1, 2, 3, 3, 3, 3, 2, 1],
                                    [1, 2, 2, 2, 2, 2, 2, 1],
                                    [1, 1, 1, 1, 1, 1, 1, 1]], np.uint8)

PROCESS_DETECTION_KERNEL_TOTAL = 0
for i in PROCESS_DETECTION_KERNEL:
    for j in i:
        PROCESS_DETECTION_KERNEL_TOTAL += j
PROCESS_DETECTION_KERNEL_TOTAL *= 1.5

MOVEMENT_ACTIVE_THRESHOLD = 10000

