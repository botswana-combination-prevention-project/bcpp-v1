

def td_to_string(td):
    """Converts seconds into string of hours, minutes, seconds."""
    s = td.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{0}:{1}:{2}'.format(hours, minutes, seconds)
