import pickle
import subprocess
from datetime import datetime
import shlex
import os
import shutil



# read data
output = open('output_memo.txt', 'rb')
memo = pickle.load(output)

def reverse_hash(hashed):
	word,movie_id = hashed.split('_')
	return word

def return_intervals(s):
	# words = s.split(" ")
	print s
	array = []
	for w in s:
		word = w[0]
		if word in memo:
			rank = w[1]
			try:
				#append the word and its 
				array.append((word,memo[word][rank]))
			except:
				array.append((word,memo[word][0]))
	print array
	return array

def return_movie_id(s):
	# words = s.split(" ")
	array = []
	for w in s:
		word = w[0]
		if word in memo:
			rank = w[1]
			try:
				#appends the word and its rank with the memo interval
				array.append((word,memo[word][rank]))
			except:
				array.append((word,memo[word][0]))
	print array
	return array

# def return_movie_id(s):
# 	return s[2]

def get_duration(time_interval):
	start,end = time_interval
	FMT = '%H:%M:%S.%f'
	tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
	return tdelta.total_seconds()

def splice_move (a):
	try:
		shutil.rmtree('spliced_videos')
	except:
		pass
	# os.removedirs("")
	os.makedirs("spliced_videos")


	command_array = []
	splice_count = 0
	fnamelist = []
	word_duration_array = []
	for i in range(0,len(a)):

		
		splice = a[i]
		f_name = "spliced_videos/splice_" + str(i) + ".mp4"
		fnamelist.append("file " + f_name)
		word = splice[0]
		#this grabs the interval
		interval = splice[1][0:2]
		movie_id_name = splice[1][3]
		movie_id_path = "/Users/yishh/Documents/VuzeDownloads/" + movie_id_name + "/" + movie_id_name + ".mp4"
		# print interval
		duration = get_duration(interval)
		# command = ["ffmpeg", "-ss", interval[0], "-i", f_mov_name, "-acodec", "copy",  "-t", str(duration), "-avoid_negative_ts", str(1),f_name]
		command = ["ffmpeg", "-ss", interval[0], "-i", movie_id_path,  "-t", str(duration), "-vf","scale=854:480", f_name]		
		# print command_array[i]
		cmd  = (" ").join(command)
		print cmd

		word_duration_array.append((word,duration))

		cmd = "/usr/local/bin/" + cmd

		command_array.append(cmd)
		rescale_movie_id_path = "/Users/yishh/Documents/VuzeDownloads/" + movie_id_name + "/" + movie_id_name +"_r" + ".mp4"

	print word_duration_array
	print "word duration array"
	print " "
	# print command_array
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

	# ffmpeg -i video.avi -vf subtitles=subtitle.srt out.avi
	#1) get subtitles


	#2) merge them
	# ffmpeg -i infile.mp4 -f srt -i infile.srt -c:v copy -c:a copy \
  	#-c:s mov_text outfile.mp4


	# subprocess.call("sleep -500", shell = True)
	# open vlc player
	# subprocess.call("/Applications/VLC.app/Contents/MacOS/VLC output/concat_output.mp4", shell = True)

def string_parser(s_array):
	result = []
	for s in s_array:
		result.append((s,0))
	return result


def wrapper_main(s):

	parsed_s = string_parser(s)
	array = return_intervals(s)
	print array 
	# movie_id = return_movie_id(s)
	# print movie_id
	# file_path = "/Users/yishh/Documents/VuzeDownloads/" + movie_id + "/" + movie_id + ".mp4"
	splice_move(array)

# s = "welcome to hack illinois"
s = [("hello",0),("how",0),("are",0),("you",0),("demolition",0),("terrorist",0),("fight",1),("anchor",0),("headmaster",0)]

wrapper_main(s)
# wrapper_main(s,"/Users/yishh/Documents/VuzeDownloads/FightClub/FightClub.mp4")
# wrapper_main(s,"/Users/yishh/Documents/VuzeDownloads/pocahontas/pocahontas.mp4")
