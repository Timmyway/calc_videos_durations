#### Scenario
- Suppose that you have a folder (and potentially with subfolders) with tons of video.
- So you would like to know the duration of each video files.
- This script will give you the duration for each single video, then it will make an html report of tracked files.

#### Dependencies
- You will have to install MediaInfo
pip install pymediainfo
[Pymediainfo on PyPy](https://pypi.org/project/pymediainfo/)
- python >= 3.6

#### How to use
- After installing dependencies, launch calc_video_durations.py
- For convenience, you can use the lenvid_example.bat to setup a batch command on windows.
Step 1: modify lenvid_example.bat, then change path-to-your-python-folder\ and path-to-calc-video-duration-on-your-computer\ to fit your case.
Step 2: Add this .bat file to your system environnement, so it can be called everywhere by command line.
