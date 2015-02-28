import pickle
import subprocess
from datetime import datetime

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

s = "seminar terminal demolition"
array = return_intervals (s, "FightClub/FightClub.mp4")
print array

def get_duration(time_interval):
	start,end = time_interval
	FMT = '%H:%M:%S.%f'
	tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
	return tdelta.total_seconds()

def splice_move (a, f_mov_name):

	command_array = []
	splice_count = 0
	for i in range(0,len(a)):
		splice = a[i]
		f_name = "splice_" + str(i) + ".mp4"
		interval = splice[1]
		duration = get_duration(interval)
		command = ["ffmpeg", "-ss", interval[0], "-i", f_mov_name, "-acodec", "copy",  "-t", str(duration), f_name]
		command_array.append(command)
		# print command_array[i]
		cmd  = (" ").join(command_array[i])
		print cmd

	merge_command = ["mencoder", "-forceidx", "-ovc", "copy", "-oac", "pcm", "-o", "fuck_yea_1.mp4", "splice_0.mp4", "splice_1.mp4"]


	# import os.path
	# print os.path.isfile("FightClub/FightClub.mp4") 

	# print command_array[0]
	# cmd  = (" ").join(command_array[0])
	# print cmd
	# subprocess.call(command_array[0])
	# subprocess.call(command_array[1])
	# subprocess.call(merge_command)

splice_move(array, "FightClub/FightClub.mp4")
# ffmpeg_command1 = ["ffmpeg", "-i", "/home/xincoz/test/connect.webm", "-acodec", "copy", "-ss", "00:00:00", "-t", "00:00:30", "/home/xincoz/test/output1.webm"]
# ffmpeg_command2 = ["ffmpeg", "-i", "/home/xincoz/test/connect.webm", "-acodec", "copy", "-ss", "00:00:30", "-t", "00:00:30", "/home/xincoz/test/output2.webm"]
# ffmpeg_command3 = ["mencoder", "-forceidx", "-ovc", "copy", "-oac", "pcm", "-o", "/home/xincoz/test/output.webm", "/home/xincoz/test/output1.webm", "/home/xincoz/test/output2.webm"]

# ffmpeg -i input.flv -ss 15 -t 60 -acodec copy -vcodec copy output.flv


# ffmpeg -i FightClub.mp4 -acodec copy -ss 02:15:30 -t 00:00:02 outfile_1.mp4
# ffmpeg -i FightClub.mp4 -acodec copy -ss 00:02:26.013 -t 00:00:02.100 outfile_2.mp4
# mencoder -forceidx -ovc copy -oac pcm -o merged_file_1.mp4 outfile_1.mp4 outfile_2.mp4

# ffmpeg -i FightClub.mp4 -ss 15 -t 60 -acodec copy -vcodec copy FightClub2_spliced.mp4

# subprocess.call(ffmpeg_command1)
# subprocess.call(ffmpeg_command2)
# subprocess.Popen(ffmpeg_command3)

