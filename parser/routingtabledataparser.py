#!/usr/bin/env python2.7

import os
import struct

class RoutingTableDataParser:

    NUMBER_OF_TIMESTAMP_BYTES = 8
    NUMBER_OF_ADDRESS_BYTES = 4
    NUMBER_OF_PHEROMONE_BYTES = 4

    def __init__(self):
        self.single_entry_size = 2 * self.NUMBER_OF_ADDRESS_BYTES + self.NUMBER_OF_PHEROMONE_BYTES

    def read_data_from(self, filename, routing_destination):
        with open(filename, "rb") as self.file:
            self.total_file_size = os.fstat(self.file.fileno()).st_size
            try:
                while(self.file.tell() < self.total_file_size):
                    byte_stream = self._request_next_bytes(self.NUMBER_OF_TIMESTAMP_BYTES + 1)
                    time = self._read_time(byte_stream)
                    nr_of_entries = self._read_nr_of_entries(byte_stream)

                    entries = self._read_entries(nr_of_entries, routing_destination)
                    entries = self._add_missing_entries_from_last_timestamp(entries)
                    self.last_entries = entries
                    yield (time, entries)
            except StopIteration:
                raise RoutingTableDataParserException("Could not parse routing table data of " + filename + ": not enough bytes")

    def _request_next_bytes(self, chunksize):
        while True:
            chunk = self.file.read(chunksize)
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

    def _read_nr_of_entries(self, byte_stream):
        return struct.unpack("B", next(byte_stream))[0]

    def _read_entries(self, nr_of_entries, routing_destination):
        byte_stream = self._request_next_bytes(nr_of_entries * self.single_entry_size)

        entries = {}
        while nr_of_entries > 0:
            destination = self._read_address(byte_stream)
            next_hop = self._read_address(byte_stream)
            pheromone_value = struct.unpack("f", self._read_next_bytes(4, byte_stream))[0]

            if(destination == routing_destination):
                entries[next_hop] = pheromone_value

            nr_of_entries -= 1

        return entries

    def _read_address(self, byte_stream):
        addressInt = struct.unpack("I", self._read_next_bytes(4, byte_stream))[0]
        byte1 = (addressInt >> 24) & 0xFF
        byte2 = (addressInt >> 16) & 0xFF
        byte3 = (addressInt >>  8) & 0xFF
        byte4 = addressInt & 0xFF
        return str(byte1) + "." + str(byte2) + "." + str(byte3) + "." + str(byte4)

    def _add_missing_entries_from_last_timestamp(self, new_entries):
        #TODO
        return new_entries

class RoutingTableDataParserException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
