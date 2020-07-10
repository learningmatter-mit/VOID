from timeit import default_timer as timer

def time_fn(fn):
    def wrapped(*args, **kwargs):
        start = timer()
        result = fn(*args, **kwargs)
        end = timer()
        print(f"Timing for {fn.__name__}: {end - start}")

        return result
    return wrapped
        
