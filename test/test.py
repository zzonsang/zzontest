'''
Created on 2012. 1. 30.

@author: kobe
'''
#!/usr/bin/env python

import os
import libtorrent

def make_torrent(path):
    abs_path = os.path.abspath(path)
    fs = libtorrent.file_storage()
    libtorrent.add_files(fs, abs_path)
    ct = libtorrent.create_torrent(fs)
    ct.add_tracker("http://127.0.0.1/announce")
    # set True if private torrent.
    ct.set_priv(True)
    libtorrent.set_piece_hashes(ct, os.path.split(abs_path)[0])
    return ct.generate()

def main():
    t = make_torrent("data.txt")
    with open("test.torrent", "wb") as f:
        f.write(libtorrent.bencode(t))
        f.close()
    
    info = libtorrent.torrent_info(t)
    print "info hash:", info.info_hash()
    for f in info.files():
        print "file: %s (%d bytes)" % (f.path, f.size)

if __name__ == "__main__":
    main()
