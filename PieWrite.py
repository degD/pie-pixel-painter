
# PIE format is a format for storing pixel image data.
# Information about each pixel is stored as a 7-byte data.
# First 2-bytes are x coords, next 2-bytes are y and
# remaining 3-bytes are for the color. Since color is in hex format.

def write_p_data(canvasdata, fb):
    """Write canvas/pixel data to the file that is referred by the fb file buffer.

    Args:
        canvasdata (PPixelCanvas.data list): A list that is consist of tuples, that each tuple represents a pixel.
        Example list [((x1, y1), c1), ((x2, y2), c2), ((x3, y3), c3)]. 
        fb (file buffer): File buffer for the file.
    
    Raise:
        IndexError: Will raise an IndexError if x or y coordinates are greater than a 16-bit number.
    """
    for p_data in canvasdata:
        # Shortly, for each pixel data, converting those information to byte objects and combining them, to write them as binary.
        x = canvasdata[0][0]
        y = canvasdata[0][1]
        c = canvasdata[1]
        
        if abs(x) >= 2**16 or abs(y) >= 2**16:
            raise IndexError('Coordinate out of range. Overflow.')
        
        strhex_x = hex(x)[2:].zfill(4)
        strhex_y = hex(y)[2:].zfill(4)
        strhex_c = c[1:]
        
        x = bytes.fromhex(strhex_x)
        y = bytes.fromhex(strhex_y)
        c = bytes.fromhex(strhex_c)
        
        p_data = x + y + c
        fb.write(p_data)
