
# initialize the library's internal state, without polluting the package-wide namespace:
__import__('', globals(), fromlist=['_internal'], level=1)._internal.__initialize_thread__()

