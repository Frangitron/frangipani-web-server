import numpy as np
from multiprocessing import shared_memory, Process, Lock

# Parent process creates shared memory
dtype = np.dtype([
    ('fader1', 'f4'),      # 4-byte float
    ('fader2', 'f4'),
    ('button1', 'i1'),     # 1-byte int (boolean)
    ('hue', 'f4'),
    ('brightness', 'f4'),
    # ... all your controls
])

shm = shared_memory.SharedMemory(create=True, size=dtype.itemsize)
controls_array = np.ndarray((1,), dtype=dtype, buffer=shm.buf)

# Child process (server) accesses it
shm_child = shared_memory.SharedMemory(name=shm.name)
controls_view = np.ndarray((1,), dtype=dtype, buffer=shm_child.buf)

# Update is extremely fast:
controls_view[0]['fader1'] = 75.0  # Atomic write
