
def strip_underscore(item):
    """Returns  a string stripped of a leading or tailing underscore."""
    if item.startswith('_'):
        return item[1:]
    if item.endswith('_'):
        return item[:-1]
    return item
