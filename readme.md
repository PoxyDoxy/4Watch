# 4Watch

Give it a list of 4Chan Boards, and Keywords to search for, and you're off to the races.

#### What does it do?
  - Searches Each Board for Threads that contain any of the keywords.
  - Downloads all images/webms/gifs from the Threads found.
  - Loops around every X seconds (0 = disable loop)

#### Works on Windows & Linux.

#### Requirements:
- Python 3 and above (Developed using 3.6.2)

#### How to run it:
1. Edit the file and adjust the Boards/Keywords.
2. Run it on Linux or Windows
```sh
$ python3 4watch.py
```

#### Things to do:
  - move image downloads into seperate folders.

#### Duplicate File Scanner/Remover:
  - removedupes.py is a duplicate file remover
  - it is run the same way as 4watch.py
  - edit the file, adjust the scan directory, and run it with 
```sh
$ python3 removedupes.py
```