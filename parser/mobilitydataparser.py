#!/usr/bin/env python3

import os
import struct

class MobilityDataParser:
    NUMBER_OF_TIMESTAMP_BYTES = 8
    NUMBER_OF_POSITION_BYTES = 8

    def __init__(self):
        self.single_entry_size = 3 * self.NUMBER_OF_POSITION_BYTES

    def read(self, file_name):
        with open(file_name, "rb") as self.file_handle:
            self.total_file_size = os.fstat(self.file_handle.fileno()).st_size
            try:
                while(self.file_handle.tell() < self.total_file_size):
                    byte_stream = self._request_next_bytes(self.NUMBER_OF_TIMESTAMP_BYTES + 1)
                    time = self._read_time(byte_stream)
                    position = self._read_position()
                    self.last_positions = position
                    yield (time, position)
            except StopIteration:
                print("Could not parse mobility trace of " + file_name + ": not enough bytes")
                raise MobilityDataParserException("Could not parse mobility trace of " + file_name + ": not enough bytes")

    def _request_next_bytes(self, chunksize):
        while True:
            chunk = self.file_handle.read(chunksize)
            if chunk:
                for byte in chunk:
                    yield byte
            else:
                break

    def _read_time(self, byte_stream):
        return struct.unpack("q", self._read_next_bytes(self.NUMBER_OF_TIMESTAMP_BYTES, byte_stream))[0]

    def _read_next_bytes(self, nr_of_bytes, byte_stream):
        result = ""
        for i in range(nr_of_bytes):
            result += next(byte_stream)

        return result

    def _read_position(self):
        byte_stream = self._request_next_bytes(self.single_entry_size)

        x = struct.unpack("d", self._read_next_bytes(8, byte_stream))[0]
        y = struct.unpack("d", self._read_next_bytes(8, byte_stream))[0]
        z = struct.unpack("d", self._read_next_bytes(8, byte_stream))[0]

        return [x, y, z]

class MobilityDataParserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


if __name__ == "__main__":
    parser = MobilityDataParser()
    #data = parser.read("/home/frey/Desktop/Projekte/code/ara-sim/simulations/ara/results/ARATEST-0-node0.mtr")
    #data = parser.read("/vol/home-vol1/simulant/frey/Desktop/Projekte/code/ara-sim/simulations/ara/results/ARATEST-0-node0.mtr")
    #data = parser.read("/home/michael/Desktop/Projekte/code/data/trace/EARA0-1-node1.mtr")
    data = parser.read("/tmp/binary_test")
    for d in data:
        print(d)
