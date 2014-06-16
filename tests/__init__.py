# enables PyDev debugger with nose
try:
    import pydevd
    import inspect
    for frame in reversed(inspect.stack()):
        if frame[1].endswith("pydevd.py"):
            pydevd.settrace(suspend=False)
            break
except ImportError:
    pass
