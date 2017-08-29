#!/usr/bin/python

# removedupes - a duplicate file remover.
# Made by PoxyDoxy.
# Requires Python 3, Developed on 3.6.2

import sys
import os
import hashlib

folder_to_scan = "4watch_downloads"

def remove_duplicates(dir):
	global total_files
	global scanned_files
	global dupe_count
	global full_dir
	unique = []
	for filename in os.listdir(dir):
		filename = full_dir + filename
		if os.path.isfile(filename):
			filehash = hashlib.md5(open(filename, 'rb').read()).hexdigest()
			if filehash not in unique: 
				unique.append(filehash)
			else: 
				dupe_count += 1
				os.remove(filename)
			scanned_files += 1

			print("\rScanning: %s/%s (%s)" % (scanned_files, total_files, "{0:.0f}%".format(scanned_files / total_files * 100)), end="")

full_dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + folder_to_scan + os.path.sep
total_files = len([name for name in os.listdir(full_dir) if os.path.isfile(full_dir + name)])
dupe_count = 0
scanned_files = 0

print("/----------------------------\\")
print("|   Duplicate File Deleter   |")
print("|            v1              |")
print("\\----------------------------/")

remove_duplicates(full_dir)
if dupe_count >= 1:
	print("\nFiles Scanned: %s." % total_files)
	print("Dupes Deleted: %s." % dupe_count)
else:
	print("\nFiles Scanned: %s." % total_files)
	print("No Dupes Found.")