from __future__ import division
from nltk.corpus import cmudict
from datetime import datetime
import re
import subprocess
import time
import copy
import pickle
import datetime as wtf_time

# import Cpickle as pickle

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

def onboard(f_sub_name, f_mov_name, memo={}):
	# memo = {}
	# print memo
	f = open (f_sub_name,'r')
	data = f.read()
	for a in data.split("\r\n\r\n"):
		if len(a) == 0:
			return
		b = a.split("\r\n")
		phrase = ""
		for i in range (2,len(b)):
			phrase += " " + b[i]

		time_interval = parse_interval(b[1])
		duration = get_duration(time_interval)
		phrase = get_language_text(phrase)
		
		syllable_sum = 0
		word_array = []
		split_phrase = phrase.split(" ")
		for w in split_phrase:
			try:
				temp_syllable = nsyl(w)[0]
				word_array.append((w,temp_syllable))
				syllable_sum += temp_syllable
			except:
				continue
		if syllable_sum == 0:
			continue
		

		if "nutcase" in phrase:
			print "fuck"
			print phrase
			print word_array
			return

		syl_interval = duration/syllable_sum
		syl_curr_count = 0
		time_curr = time_interval[0]
		# word_end = time_curr

		word_end = time_curr
		for i in range(0,len(word_array)):
			w = word_array[i]
			
			word_start = word_end

			syl_curr_count += w[1]
			added_time_intervals = syl_curr_count * syl_interval
			word_end = add_time(time_interval[0], added_time_intervals)


			# print w
			# print "syl sum: ", syllable_sum
			# print "syl_curr_count: ", syl_curr_count
			# print "interval size: ", syl_interval
			# print "added time intervals: ", added_time_intervals
			# print "wordstart: ", word_start
			# print "word end: ", word_end		

			word = w[0]
			word_array[i] = (word, word_start, word_end)
			
			# print len(memo.keys())

			if word == "nutcase":
				print time_interval[0]
				print word_start, word_end
				return



			if word in memo:
				# print word
				temp_array = memo[word]
				temp_array.append((word_start,word_end))
				# print temp_array
				# break
				temp_array_2 = copy.deepcopy(temp_array)
				memo[word] = temp_array
			else:
				memo[word] = [(word_start,word_end)]
		# print memo
		# print time_interval, duration, word_array, syllable_sum
	# print memo
	return

memo = {}
onboard("FightClub/FightClub.srt","FightClub/FightClub.mp4",memo)

output = open('output_memo.txt', 'ab+')
data = {'a': [1, 2, 3],}

pickle.dump(memo, output)
output.close()

# read data
# output = open('output.txt', 'rb')
# obj_dict = pickle.load(output)

# print memo

