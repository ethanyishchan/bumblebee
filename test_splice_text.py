import pickle
import subprocess
from datetime import datetime
import shlex
import os
import shutil



# read data
output = open('output_memo.txt', 'rb')
memo = pickle.load(output)

def return_intervals(s,f_mov_name):
	words = s.split(" ")
	array = []
	for w in words:
		if w in memo:
			#rmb this is only first
			array.append((w,memo[w][0]))

	return array

s = "headquarters organization demolition"
array = return_intervals (s, "FightClub/FightClub.mp4")
print array
print " "

def get_duration(time_interval):
	start,end = time_interval
	FMT = '%H:%M:%S.%f'
	tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
	return tdelta.total_seconds()

def splice_move (a, f_mov_name):

	shutil.rmtree('spliced_videos')
	# os.removedirs("")
	os.makedirs("spliced_videos")

	command_array = []
	splice_count = 0
	fnamelist = []
	for i in range(0,len(a)):
		splice = a[i]
		f_name = "spliced_videos/splice_" + str(i) + ".mp4"
		fnamelist.append("file " + f_name)
		interval = splice[1]
		duration = get_duration(interval)
		# command = ["ffmpeg", "-ss", interval[0], "-i", f_mov_name, "-acodec", "copy",  "-t", str(duration), "-avoid_negative_ts", str(1),f_name]
		command = ["ffmpeg", "-ss", interval[0], "-i", f_mov_name,  "-t", str(duration), f_name]		
		# print command_array[i]
		cmd  = (" ").join(command)
		print cmd
		# print command

		cmd = "/usr/local/bin/" + cmd
		command_array.append(cmd)

	for c in command_array:
		subprocess.call(c, shell = True)

	#generate a list of filepaths
	f_name_file = open('fnamelist.txt', 'wb')
	f_name_file.write( ("\n").join(fnamelist) )
	f_name_file.close() 

	os.remove("output/concat_output.mp4")
	concat_cmd = "/usr/local/bin/ffmpeg -f concat -i fnamelist.txt -c copy output/concat_output.mp4"

	subprocess.call(concat_cmd, shell = True)

	# alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'
	# subprocess.call("alias vlc='/Applications/VLC.app/Contents/MacOS/VLC'", shell = True)
	# subprocess.call("")
	subprocess.call("/Applications/VLC.app/Contents/MacOS/VLC output/concat_output.mp4", shell = True)

splice_move(array, "FightClub/FightClub.mp4")


