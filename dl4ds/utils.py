import numpy as np
import tensorflow as tf
from datetime import datetime


def set_gpu_memory_growth(verbose=True):
    physical_devices = list_devices(verbose=verbose) 
    for gpu in physical_devices:
        tf.config.experimental.set_memory_growth(gpu, True)
    print(physical_devices)


def list_devices(which='physical', gpu=True, verbose=True):
    if gpu:
        dev = 'GPU'
    else:
        dev = 'CPU'
    if which == 'physical':
        devices = tf.config.list_physical_devices(dev)
    elif which == 'logical':
        devices = tf.config.list_logical_devices(dev)
    if verbose:
        print(devices)
    return devices


def set_visible_gpu(indices=(0)):
    physical_devices = list_devices('physical')
    tf.config.set_visible_devices(physical_devices[indices], 'GPU') 
    print(list_devices('logical'))


class Timing():
    """ 
    """
    sep = '-' * 80

    def __init__(self, verbose=True):
        """ 
        Timing utility class.

        Parameters
        ----------
        verbose : bool
            Verbosity.

        """
        self.verbose = verbose
        self.running_time = None
        self.checktimes = list()
        self.starting_time = datetime.now()
        self.starting_time_fmt = self.starting_time.strftime("%Y-%m-%d %H:%M:%S")
        if self.verbose:
            print(self.sep)
            print(f"Starting time: {self.starting_time_fmt}")
            print(self.sep)
        
    def runtime(self):
        """ 
        """
        self.running_time = str(datetime.now() - self.starting_time)
        if self.verbose:
            print(self.sep)
            print(f"Final running time: {self.running_time}")
            print(self.sep)
    
    def checktime(self):
        """
        """
        checktime = str(datetime.now() - self.starting_time)
        self.checktimes.append(checktime)
        if self.verbose:
            print(self.sep)
            print(f"Timing: {checktime}")
            print(self.sep)


def crop_image(array, size, yx=None, position=False, get_copy=False):
    """
    Return an square cropped version of a 2D ndarray.
    
    Parameters
    ----------
    array : 2d numpy ndarray
        Input image.
    size : int
        Size of the cropped image.
    yx : tuple of int or None, optional
        Y,X coordinate of the center of the cropped image. If None then a random
        position will be chosen.
    position : bool, optional
        If set to True return also the coordinates of the bottom-left vertex.
    
    Returns
    -------
    cropped_array : numpy ndarray
        Cropped ndarray. By default a view is returned, unless ``get_copy``
        is True. 
    y, x : int
        [position=True] Y,X coordinates.
    """
    array_size_y = array.shape[0]
    array_size_x = array.shape[1]
    
    if array.ndim != 2:
        raise TypeError('Input array is not a 2d array.')
    if not isinstance(size, int):
        raise TypeError('`Size` must be integer')
    if size >= array_size_y or size >= array_size_x: 
        msg = "`Size` is equal to or bigger than the initial frame size"
        raise ValueError(msg)

    wing = int(size / 2)
    if yx is not None and isinstance(yx, tuple):
        y, x = yx
    else:
        # random location
        y = np.random.randint(wing + 1, array_size_y - wing - 1)
        x = np.random.randint(wing + 1, array_size_x - wing - 1)

    y0, y1 = int(y - wing), int(y + wing)
    x0, x1 = int(x - wing), int(x + wing)

    if y0 < 0 or x0 < 0 or y1 > array_size_y or x1 > array_size_x:
        raise RuntimeError(f'Cropped image cannot be obtained with size={size}, y={y}, x={x}')

    if get_copy:
        cropped_array = array[y0: y1, x0: x1].copy()
    else:
        cropped_array = array[y0: y1, x0: x1]

    if position:
        return cropped_array, y, x
    else:
        return cropped_array