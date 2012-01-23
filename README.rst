Persistent Crypto Dictionary
****************************

This class implements a persistent dictionary using sqlite3 and
encrypts the keys and the values of the dictionary in a way, that
makes it very hard to bruteforce either the key or the values in the
db.

example usage::
   >>> from pcd import PersistentCryptoDict
   >>> d=PersistentCryptoDict()
   >>> print d
   <pcd.PersistentCryptoDict instance at 0x8dcb54c>
   >>> print d['my key']
   None
   >>> d['my key']='secret value'
   >>> print d['my key']
   secret value
   >>> d['my key']='top secret value'
   >>> print d['my key']
   top secret value

Crypto
======

The key and the value in the dict is transformed according to the
following algorithm (credit: dnet):

Setting values
++++++++++++++
1. we calculate they keyhash - a hmac-sha512(salt,key)
2. we split the key in half, the first half as a hexdigest (ascii),
   the second we keep as a binary
3. we use the second binary half from step 2 of the keyhash to encrypt
   the value
4. we use the ascii keyhash from step 2 as a key to the database, and
   the value is the encrypted result from step 3.

Getting values
++++++++++++++
1. we calculate they keyhash - a hmac-sha512(salt,key)
2. we split the key in half, the first half as a hexdigest (ascii),
   the second we keep as a binary
3. we query the database using the ascii keyhash from step 2 as a key
4. we use the second binary half from step 2 of the keyhash to decrypt
   the value

The database contains only the following pairs of data:

  (hmac-sha512(key, salt).hexdigest()[:64],                # key
  aes256-ofb(hmac-sha512(key, salt).digest()[32:], value)) # value

we diligently obey Schneier's law:
https://www.schneier.com/blog/archives/2011/04/schneiers_law.html, and
thus we would consider the task to retrieve any meaningful data
without huge rainbow tables from such a database a futile task. :)
