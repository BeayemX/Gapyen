# Game Architecture Network Layer (ganet)
#
# Copyright (c) 2014 Roman Divotkey, Univ. of Applied Sciences Upper Austria. 
# All rights reserved.
#
# This file is subject to the terms and conditions defined in file
# 'LICENSE', which is part of this source code package.
#
# THIS CODE IS PROVIDED AS EDUCATIONAL MATERIAL AND NOT INTENDED TO ADDRESS
# ALL REAL WORLD PROBLEMS AND ISSUES IN DETAIL.

import struct

class RawMessageBuilder(object):

    STRING_TERMINATOR = ':'

    def __init__(self):
        self.reset()

    def reset(self):
        self._msg = str('#')
        self.pos = 0

    def write_string(self, s):
        self._msg += "%s%s" % (s, self.STRING_TERMINATOR)

    def write_int(self, value):
        self._msg += struct.pack('!i', value)

    def write_float(self, value):
        self._msg += struct.pack('!d', value)

    def write_bool(self, value):
        if value:
            self._msg += 't'
        else:
            self._msg += 'f'

    def get_message(self):
        return str(self._msg)

class VanillaMessageBuilder(object):

    TERMINATOR = ':'

    def __init__(self):
        self.reset()

    def reset(self):
        self._msg = str()
        self.pos = 0

    def _prolog(self):
        if self._msg:
            self._msg += self.TERMINATOR

    def write_string(self, s):
        self._prolog()
        self._msg += str(s)

    def write_int(self, value):
        self._prolog()
        self._msg += "%d" % value

    def write_float(self, value):
        self._prolog()
        self._msg += "%f" % value

    def write_bool(self, value):
        self._prolog()
        if value:
            self._msg += 'true'
        else:
            self._msg += 'false'

    def get_message(self):
        return str(self._msg)

class DecoderMode(object):

    def __init__(self, context):
        self.context = context

    def read_string(self):
        if self.context._pos >= len(self.context._msg):
            raise Exception('message out of data')
        idx = self.context._msg.find(self.context.STRING_TERMINATOR,
                                     self.context._pos)
        if idx < 0:
            s = self.context._msg[self.context._pos:]
            self.context._pos = len(self.context._msg)
            return s

        s = self.context._msg[self.context._pos:idx]
        self.context._pos = idx + 1
        return s    

class RawMode(DecoderMode):

    def __init__(self, context):
        DecoderMode.__init__(self, context)

    def _read(self, fmt, size):
        idx = self.context._pos
        result = struct.unpack(fmt, self.context._msg[idx:idx + size])
        self.context._pos += size
        return result[0]
        
    def read_float(self):
        return self._read('!d', 8)

    def read_int(self):
        return self._read('!i', 4)

    def read_bool(self):
        v = self.context._msg[self.context._pos]
        if v == 't':
            result = True
        else:
            result = False
        self.context._pos += 1

        return result

class VanillaMode(DecoderMode):

    def __init__(self, context):
        DecoderMode.__init__(self, context)

    def read_float(self):
        return float(self.read_string())

    def read_int(self):
        return int(self.read_string())

    def read_bool(self):
        value = self.read_string()
        return value == 'true'
    
class MessageDecoder(object):

    STRING_TERMINATOR = ':'

    def __init__(self, msg = None):
        self.mode = None
        if msg:
            self.reset(msg)

    def reset(self, msg):
        self._msg = str(msg)
        if msg and msg[0] == '#':
            self._pos = 1
            self._mode = RawMode(self)
        else:
            self._pos = 0
            self._mode = VanillaMode(self)

    def create_encoder(self):
        if self.is_raw():
            return RawMessageBuilder()
        else:
            return VanillaMessageBuilder()

    def is_raw(self):
        return isinstance(self._mode, RawMode) 
            
    def read_string(self):
        return self._mode.read_string()

    def read_float(self):
        return self._mode.read_float()

    def read_int(self):
        return self._mode.read_int()

    def read_bool(self):
        return self._mode.read_bool()
