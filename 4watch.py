#!/usr/bin/python

# 4Watch - a 4Chan Board Image Watcher.
# Made by PoxyDoxy.
# Works with the following:
# - 4chan
# Searches for Posts containing the following keywords. 
# Requires Python 3, Developed on 3.6.2

boards = ["wg", "w"]
keywords = ["galaxy","spaceship"]
save_folder_name = "4watch_downloads"

# Should we scan the thread title?
scan_title = 1
# Should we scan the thread description?
scan_description = 1
# Should we scan the stickied/pinned threads?
scan_sticky = 0
# How long to wait for if looping (seconds)
# 0 = disabled, 10 = 10 seconds
loop_wait = 30

# Adjust if you want to scan a different Chan.
catalog_url_format = "https://boards.4chan.org/%s/catalog.json"
thread_url_format = "https://boards.4chan.org/%s/thread/%s"
image_url_format = "https://i.4cdn.org/%s/%s%s"

# Begin Importing
import sys
import time
import json
import os
import urllib.request

def clean_string(string):
	# Clean the String to ensure that words match properly, both with seperators and fullstops.
	string = string.replace(".", " ")
	string = string.replace(",", " ")
	string = string.replace(";", " ")
	string = string.replace(":", " ")
	string = string.replace("+", " ")
	string = string.replace("!", " ")
	string = string.replace("?", " ")
	string = string.replace("[", " ")
	string = string.replace("]", " ")
	string = string.replace("(", " ")
	string = string.replace(")", " ")
	string = string.lower()
	return string

def check_thread(details):
	download = 0

	global threads_scanned
	threads_scanned += 1

	# Scan Title
	try:
		if scan_title == 1:
			for singleword in clean_string(details['sub']).split(' '):
				if singleword in keywords:
					download = 1
	except:
		pass

	# Scan Description
	try:
		if scan_description == 1:
			for singleword in clean_string(details['com']).split(' '):
				if singleword.lower() in keywords:
					download = 1
	except:
		pass

	if download == 1:
		try:
			#download thread
			global threads_to_download
			threads_to_download.append([board, details['no']])
			global threads_matched
			threads_matched += 1
		except:
			pass

def download_url(url_board, filename, filesize, ext):
	global image_url_format
	global save_folder
	global downloaded_image_count
	global failed_image_count
	global processed_image_count
	image_url = image_url_format % (url_board, filename, ext)
	total_path_to_new_file = os.path.normpath("%s%s%s_%s%s" % (save_folder, os.path.sep, filename, filesize, ext))
	if not os.path.isfile(total_path_to_new_file):
		try:
			data = urllib.request.urlretrieve(image_url, total_path_to_new_file)
			downloaded_image_count += 1
		except:
			print("Warning: Unable to get %s" % image_url)
			failed_image_count += 1
			pass
		
	processed_image_count += 1

def fetch_json(url):
	req = urllib.request.Request(url, headers={'User-Agent' : "4Watch Browser"})
	data_raw = urllib.request.urlopen(req)
	data = data_raw.read()
	encoding = data_raw.info().get_content_charset('utf-8')
	parsed_json = json.loads(data.decode(encoding))
	return parsed_json

# Start main
while True:
	print("/---------------\\")
	print("|   4Watch  v1  |")
	print("\---------------|")
	print("/ Boards:", len(boards))
	print("| Keywords:", len(keywords))
	print("\\---------------/")
	print("")

	threads_scanned = 0
	threads_matched = 0
	processed_image_count = 0
	downloaded_image_count = 0
	failed_image_count = 0
	downloadable_image_count = 0
	threads_to_download = []
	images_to_download = []

	# Lower keywords to lowercase in preperation for the search.
	keywords = [element.lower() for element in keywords]

	# Scan Each Boards Content
	for board in boards:

		# prepare url
		this_catalog_url = catalog_url_format % board

		print("Scanning /%s/                  " % board, "\r", end="")

		# Wait 1 second between Catalog Requests because of API rules
		try:
			runtime = time.clock() - start_time
			if runtime < 1:
				#print("sleeping for ", 1 - runtime)
				time.sleep(1 - runtime)
		except:
			pass

		start_time = time.clock()

		# Fetch Catalog containing JSON
		try:
			parsed_json = fetch_json(this_catalog_url)
		except:
			print("Warning: Could not load /%s/" % board)
			continue

		for parts in parsed_json:
			for details in parts['threads']:

				# Check if Sticky. Giggity.
				try:
					if details['sticky'] == 1:
						if scan_sticky == 1:
							check_thread(details)
				except:
					check_thread(details)

	if threads_scanned >= 1: 
		if threads_matched >=1:
			print("Matched:", threads_matched, "/", threads_scanned , " threads (", "{0:.0f}%".format(threads_matched / threads_scanned * 100), ")")
			print()
			print("Downloading %s threads" % threads_matched, end="")

			# Check to see if the downloads folder exists
			save_folder = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + save_folder_name)
			if not os.path.isdir(save_folder):
			    os.makedirs(save_folder)

			# Scan Each Thread URL
			scanned_threads = 0
			for thread in threads_to_download:
				url_board = thread[0]
				url_thread = thread[1]

				thread_url = thread_url_format % (url_board, url_thread)

				print("\rScanning Threads | %s/%s    " % (scanned_threads, threads_matched), "\r", end="")

				# prepare url
				thread_catalog_url = thread_url + ".json"

				# Wait 1 second between Catalog Requests because of API rules
				try:
					runtime = time.clock() - start_time
					if runtime < 1:
						#print("sleeping for ", 1 - runtime)
						time.sleep(1 - runtime)
				except:
					pass

				start_time = time.clock()

				# Fetch Thread Catalog containing JSON
				try:
					parsed_json = fetch_json(thread_catalog_url)
				except:
					print("Warning: Thread %s has 404'd" % url_thread)
					continue

				for message in parsed_json["posts"]:
					if "ext" in message:
						try:
							downloadable_image_count += 1
							images_to_download.append([url_board, message["tim"], message["fsize"], message["ext"]])
						except:
							pass
				scanned_threads += 1

			for image in images_to_download:
				print("\rDownloading | %s threads | %s/%s images (%s)                   \r" % (threads_matched, processed_image_count, downloadable_image_count, "{0:.0f}%".format(processed_image_count / downloadable_image_count * 100)), end="")
				furl = image[0]
				ftime = image[1]
				fsize = image[2]
				fext = image[3]
				download_url(furl, ftime, fsize, fext)

			print("Download Complete (%s files).                                              " % downloaded_image_count)
			if failed_image_count >= 1:
				print("Failed to download %s files.                                              " % failed_image_count)
			print()
		else:
			print("No threads matched.")
	else:
		print("No threads found, Check your Internet?")

	if loop_wait == 0:
		break
	else:
		time_remaining = loop_wait
		while time_remaining >= 1:
			print("\rStarting again in %s seconds.      \r" % time_remaining, end="")
			time.sleep(1)
			time_remaining -= 1
		os.system('cls' if os.name == 'nt' else 'clear')

# code run time diagnostics
# 	start_time = time.clock()
# 	print("{0:.2f}".format(time.clock() - start_time), "seconds")
