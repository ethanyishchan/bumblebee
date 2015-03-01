import pickle
import subprocess
from datetime import datetime
import shlex
import os
import shutil



# read data
output = open('output_memo.txt', 'rb')
memo = pickle.load(output)

def return_intervals(s):
	# words = s.split(" ")
	array = []
	for w in s:
		word = w[0]
		if word in memo:
			rank = w[1]
			try:
				array.append((word,memo[word][rank]))
			except:
				array.append((word,memo[word][0]))
	print array
	return array

def get_duration(time_interval):
	start,end = time_interval
	FMT = '%H:%M:%S.%f'
	tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
	return tdelta.total_seconds()

def splice_move (a, f_mov_name):
	try:
		shutil.rmtree('spliced_videos')
	except:
		pass
	# os.removedirs("")
	os.makedirs("spliced_videos")

	command_array = []
	splice_count = 0
	fnamelist = []
	for i in range(0,len(a)):
		splice = a[i]
		f_name = "spliced_videos/splice_" + str(i) + ".mp4"
		fnamelist.append("file " + f_name)
		interval = splice[1][0:2]
		# print interval
		duration = get_duration(interval)
		# command = ["ffmpeg", "-ss", interval[0], "-i", f_mov_name, "-acodec", "copy",  "-t", str(duration), "-avoid_negative_ts", str(1),f_name]
		command = ["ffmpeg", "-ss", interval[0], "-i", f_mov_name,  "-t", str(duration), f_name]		
		# print command_array[i]
		cmd  = (" ").join(command)
		print cmd

		cmd = "/usr/local/bin/" + cmd
		command_array.append(cmd)

	for c in command_array:
		subprocess.call(c, shell = True)
		# subprocess.call("sleep -50", shell = True)

	#generate a list of filepaths
	f_name_file = open('fnamelist.txt', 'wb')
	f_name_file.write(("\n").join(fnamelist))
	# print fnamelist
	f_name_file.close() 

	try:
		os.remove("output/concat_output.mp4")
	except:
		pass
	concat_cmd = "/usr/local/bin/ffmpeg -f concat -i fnamelist.txt -c copy output/concat_output.mp4"

	subprocess.call(concat_cmd, shell = True)

	subprocess.call("sleep -500", shell = True)
	# subprocess.call("/Applications/VLC.app/Contents/MacOS/VLC output/concat_output.mp4", shell = True)

def wrapper_main(s, f_name):
	splice_move(return_intervals(s),f_name)

# s = "welcome to hack illinois"
s = [("hello",0),("demolition",0),("terrorist",0),("fight",1)]


wrapper_main(s,"/Users/yishh/Documents/VuzeDownloads/FightClub/FightClub.mp4")
# wrapper_main(s,"/Users/yishh/Documents/VuzeDownloads/pocahontas/pocahontas.mp4")
