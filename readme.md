# 4Watch

Give it a list of 4Chan Boards, and Keywords to search for, and you're off to the races.

#### What does it do?
  - Searches Each Board for Threads that contain any of the keywords.
  - Downloads all images/webms/gifs from the Boards found.

#### Requirements:
- Python 3.6.2
- PIP (apt-get install python3-pip)

#### How to run it:
1. Edit the file and adjust the Boards/Keywords.
2. When running for the first time, root is required to access "/usr/local/lib/python/dist-packages/bs4"
```sh
$ sudo python3 4watch.py
```
3. After the first run, root is not required.