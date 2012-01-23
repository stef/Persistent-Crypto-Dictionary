#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PersistentCryptoDict
#
# (C) 2012- by Stefan Marsiske, <stefan.marsiske@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import with_statement
import hmac, hashlib
from Crypto.Cipher import AES
from contextlib import closing
from base64 import b64encode, b64decode
import sqlite3

class sha512:
    digest_size = 64
    def new(self, inp=''):
        return hashlib.sha512(inp)

CREATE_SQL = "CREATE TABLE if not exists pcd_urlcache (key TEXT PRIMARY KEY, value TEXT);"
class PersistentCryptoDict():
    def __init__(self, filename='pcd.db', salt="3j3,xiDS"):
        self.salt = salt
        self.db = sqlite3.connect(filename)
        # create table if not existing
        cursor = self.db.cursor()
        cursor.executescript(CREATE_SQL)
        self.db.commit()
        # reconnect to the new db
        cursor.close()
        self.db.close()
        self.db = sqlite3.connect(filename)

    def __setitem__(self, key, value):
        # calculate keys
        B, C = self.get_key(key)
        ciphertext = self.encrypt(C, value)
        # store B: base64(aes(C,value))
        self.query_db('INSERT OR REPLACE INTO pcd_urlcache (key, value) VALUES (?, ?)', (B, ciphertext))

    def __getitem__(self,key):
        # calculate keys
        B, C = self.get_key(key)
        value = self.query_db("SELECT value FROM pcd_urlcache WHERE key == ? LIMIT 1", (B,))
        if value:
            return self.decrypt(C, value)

    def query_db(self,query, params=[]):
        with closing(self.db.cursor()) as cursor:
            cursor.execute(query, params)
            self.db.commit()
            return (cursor.fetchone() or [None])[0]

    def get_key(self,key):
        A = hmac.new(self.salt, key, sha512())
        return (A.hexdigest()[:64],
                A.digest()[32:])

    def encrypt(self, C, value):
        # encrypt value with second half of MAC
        bsize=len(C)
        cipher = AES.new(C, AES.MODE_OFB)
        # pad value
        value += chr(0x08) * (-len(value) % bsize)
        return b64encode(''.join([cipher.encrypt(value[i*bsize:(i+1)*bsize])
                                  for i in range(len(value)/bsize)]))

    def decrypt(self, C, value):
        # decode value
        value=b64decode(value)
        cipher = AES.new(C, AES.MODE_OFB)
        bsize=len(C)
        return ''.join([cipher.decrypt(value[i*bsize:(i+1)*bsize])
                        for i in range(len(value)/bsize)]).rstrip(chr(0x08))

if __name__ == "__main__":
    d=PersistentCryptoDict('pcd.db')
    print d
    print d['my key']
    d['my key']='secret value'
    print d['my key']
    d['my key']='top secret value'
    print d['my key']
