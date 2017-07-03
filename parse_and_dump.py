from __future__ import division
from nltk.corpus import cmudict
from datetime import datetime
import re
import subprocess
import time
import copy
import pickle
import datetime as wtf_time
import math
import os

#global dick
d = cmudict.dict()
def nsyl(word):
  return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 


#takes in string and returns string without <> tags and without punctuation
def get_language_text(input_string):    
    #remove punctuation
    rep = {"<i>": "", "</i>": ""} 
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], input_string).rstrip().lstrip()
    text = text.lstrip().rstrip()
    string = re.sub(r'[^\w\s]','', text)
    string = string.lstrip().rstrip()
    string = string.lower()
    return string

def parse_interval(i_raw):
	start,end = i_raw.split(" --> ")
	start = start.replace(",",".")
	end = end.replace(",",".")

	return [start,end]


def get_duration(time_interval):
	start,end = time_interval
	FMT = '%H:%M:%S.%f'
	tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
	return tdelta.total_seconds()

def add_time(start, duration):
	FMT = '%H:%M:%S.%f'
	start_time = datetime.strptime(start, FMT)
	new_time = start_time + wtf_time.timedelta(0,duration)
	new_time = datetime.strftime(new_time, FMT)
	return new_time

def weighting_function(n,k=0.00):
	return n * (1 - math.pow(k,(1/n)))

# print weighting_function(0.05,4)
def parse_movieid (s):
	return s.split('.')[0].split('/')[-1]

def onboard(f_sub_name, f_mov_name, memo={}):
	movie_id = parse_movieid(f_mov_name)
	f = open (f_sub_name,'r')
	data = f.read()
	for a in data.split("\r\n\r\n")[1:]:
		if len(a) == 0:
			return
		b = a.split("\r\n")

		phrase = ""
		for i in range (2,len(b)):
			phrase += " " + b[i]
		try:
			time_interval = parse_interval(b[1])
		except:
			continue
		duration = get_duration(time_interval)
		phrase = get_language_text(phrase)

		weighted_sum = 0
		syllable_sum = 0
		word_array = []
		split_phrase = phrase.split(" ")

		flag_inner = 0
		for w in split_phrase:
			try:
				temp_syllable = nsyl(w)[0]
				#weighting function goes in here
				weighted_syllable = weighting_function(temp_syllable)
				word_array.append((w,temp_syllable,weighted_syllable))
				syllable_sum += temp_syllable
				weighted_sum += weighted_syllable
			except:
				flag_inner = 1
				break

		if flag_inner ==1:
			continue


		#calculate the normalized weight, including the function
		for i in range (0,len(word_array)):
			word_tuple = word_array[i]
			word_duration = word_tuple[2]/weighted_sum * duration
			word_array[i] = word_tuple + (word_duration,)

		syl_curr_count = 0
		time_curr = time_interval[0]

		word_end = time_curr
		for i in range(0,len(word_array)):
			w = word_array[i]
			
			word_start = word_end
			#add the word_duration of each word
			word_duration_i = word_array[i][3]
			word_end = add_time(word_start,word_duration_i)
			word_position_normalized = (get_duration([time_interval[0], word_start]))/weighted_sum
 			
			word = w[0]
			word_array[i] = (word, word_start, word_end, w[1])
			# print word_array[i]

			# hash_word = word + "_" + movie_id
			if word in memo:
				temp_array = memo[word]
				temp_array.append((word_start,word_end,word_position_normalized,movie_id))
				temp_array = sorted(temp_array, key = lambda x: x[2],reverse = True)
				# print temp_array
				temp_array_2 = copy.deepcopy(temp_array)
				memo[word] = temp_array
			else:
				memo[word] = [(word_start,word_end,word_position_normalized,movie_id)]

	return


#goal: need some sort of framework to align audio and video
#

def onboard_phonemes(f_sub_name, f_mov_name, memo={}):
	movie_id = parse_movieid(f_mov_name)
	f = open (f_sub_name,'r')
	data = f.read()
	for a in data.split("\r\n\r\n")[1:]:
		if len(a) == 0:
			return
		b = a.split("\r\n")

		phrase = ""
		for i in range (2,len(b)):
			phrase += " " + b[i]
		try:
			time_interval = parse_interval(b[1])
		except:
			continue
		duration = get_duration(time_interval)
		phrase = get_language_text(phrase)

		weighted_sum = 0
		syllable_sum = 0
		word_array = []
		split_phrase = phrase.split(" ")

		flag_inner = 0
		for w in split_phrase:
			try:
				temp_syllable = nsyl(w)[0]
				#weighting function goes in here
				weighted_syllable = weighting_function(temp_syllable)
				word_array.append((w,temp_syllable,weighted_syllable))
				syllable_sum += temp_syllable
				weighted_sum += weighted_syllable
			except:
				flag_inner = 1
				break

		if flag_inner ==1:
			continue


		#calculate the normalized weight, including the function
		for i in range (0,len(word_array)):
			word_tuple = word_array[i]
			word_duration = word_tuple[2]/weighted_sum * duration
			word_array[i] = word_tuple + (word_duration,)

		syl_curr_count = 0
		time_curr = time_interval[0]

		word_end = time_curr
		for i in range(0,len(word_array)):
			w = word_array[i]
			
			word_start = word_end
			#add the word_duration of each word
			word_duration_i = word_array[i][3]
			word_end = add_time(word_start,word_duration_i)
			word_position_normalized = (get_duration([time_interval[0], word_start]))/weighted_sum
 			
			word = w[0]
			word_array[i] = (word, word_start, word_end, w[1])
			# print word_array[i]

			# hash_word = word + "_" + movie_id
			if word in memo:
				temp_array = memo[word]
				temp_array.append((word_start,word_end,word_position_normalized,movie_id))
				temp_array = sorted(temp_array, key = lambda x: x[2],reverse = True)
				# print temp_array
				temp_array_2 = copy.deepcopy(temp_array)
				memo[word] = temp_array
			else:
				memo[word] = [(word_start,word_end,word_position_normalized,movie_id)]

	return

def init(input_videos_txt):
	movie_list_file = open('input_videos.txt','r')
	data = movie_list_file.read()

	memo = {}

	for a in data.split('\n\n'):
		subtitle_path,video_path = a.split('\n')
		onboard(subtitle_path,video_path,memo)
		print video_path + " ----- done"
		# onboard("/Users/yishh/Documents/VuzeDownloads/FightClub/FightClub.srt","/Users/yishh/Documents/VuzeDownloads/FightClub/FightClub.mp4",memo)
		# onboard("/Users/yishh/Documents/VuzeDownloads/pocahontas/pocahontas.srt","/Users/yishh/Documents/VuzeDownloads/pocahontas/pocahontas.srt",memo)
	try:
		os.remove('output_memo.txt')
	except:
		pass

	output = open('output_memo.txt', 'ab+')
	pickle.dump(memo, output)
	output.close()
	print "done initializing output file"

# init('input_videos.txt')


