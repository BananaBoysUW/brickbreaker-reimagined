def map_val(inMin, inMax, outMin, outMax, n):
    """maps n from [inMin, inMax] -> [outMin, outMax]"""
    n = max(min(n, inMax), inMin)
    return outMin + ((n - inMin) / (inMax - inMin)) * (outMax - outMin)
