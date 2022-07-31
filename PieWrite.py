
# PIE format is a format for storing pixel image data.
# Information about each pixel is stored as a 7-byte data.
# First 2-bytes are x coords, next 2-bytes are y and
# remaining 3-bytes are for the color.

def write_p_data(x, y, color, fb):
    strhex_x = hex(x)[2:].zfill(4)
    strhex_y = hex(y)[2:].zfill(4)
    strhex_c = color[1:]
    
    x = bytes.fromhex(strhex_x)
    y = bytes.fromhex(strhex_y)
    c = bytes.fromhex(strhex_c)
    
    p_data = x + y + c
    fb.write(p_data)
