from numcodecs.compat import ensure_ndarray

def decode_chunk(rfile, offset, size, dtype, shape, order, chunk_selection, method=None):
        """ We do our own read of chunks and decoding etc """
       
        #fIXME: for the moment, open the file every time ... we might want to do that, or not
        with open(rfile,'rb') as open_file:
            # get the data
            chunk = read_block(open_file, offset, size)
            # make it a numpy array of bytes
            chunk = ensure_ndarray(chunk)
            # convert to the appropriate data type
            chunk = chunk.view(dtype)
            # sort out ordering and convert to the parent hyperslab dimensions
            chunk = chunk.reshape(-1, order='A')
            chunk = chunk.reshape(shape, order=order)

        tmp = chunk[chunk_selection]
        if method:
            return method(tmp)
        else:
            return tmp

def read_block(open_file, offset, size):
        """ Read <size> bytes from <open_file> at <offset>"""
        place = open_file.tell()
        open_file.seek(offset)
        data = open_file.read(size)
        open_file.seek(place)
        return data
