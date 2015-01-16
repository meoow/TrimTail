#!/usr/bin/env python2.7

import sys, os

chunksize = 1024

def trunk_tail(infile):
	filesize = os.stat(infile).st_size
	blank = ' ' * (len(str(filesize)) + 1)
	sys.stdout.write('{0}'.format(filesize))
	sys.stdout.flush()

	with open(infile, 'rb') as fh:
		finalpos = filesize
		for cks in (chunksize*500, chunksize*50, chunksize, chunksize/50, 10):
			if finalpos < cks*2:
				continue
			fh.seek(finalpos-cks)
			preblock = fh.read(cks)
			for pos in xrange(finalpos-cks*2, -1, -cks):
				fh.seek(pos)
				currblock = fh.read(cks)
				if preblock != currblock:
					if pos != finalpos - cks * 2:
						finalpos = pos + cks
					break
				sys.stdout.write('\r{0}\r{1}'.format(blank,pos))
				sys.stdout.flush()
	sys.stdout.write('\r{0}\r{1}'.format(blank,finalpos))
	sys.stdout.write('\n')

	if finalpos < filesize:
		with open(infile, 'ab') as wh:
			wh.truncate(finalpos)

if __name__ == '__main__':
	for f in sys.argv[1:]:
		trunk_tail(f)

