# bumblebee
Replicating Transformer's Bumblebee voice, during HackIllinois 2015


We want to create a novel, new way for people to communicate without speaking. Stephen Hawking has his iconic voice, Anonymous has their Guy Fawkes scrambled voice, we want to present our new way of communicating, through dialogues of movies. Anyone who wants to find a new and exciting way of sending a message will do so through Bumble Speak!

Inspired by Transformer's BumbleBee's speaking through radio broadcasts, we decided to do the same through movie dialogues, you type in a sentence, and we go through our movie database and stitch a collage of words spoken by actors and actresses in films!

Technical Part:
We developed our own word detection algorithm in videos, where we linked subtitle phrases and videos with time stamps. After which, we used nltk (natural language processing tool kit) with cmu's dictionary to count the number of syllables per phrase. 

We first partitioned the phrase interval into words proportional to the number of syllables. As longer syllabled words are not directly proportional to the actual pronounciation length: Example: "Rhinoceros" (5 syllables) as compared to "Bull (1 syllables)" is not 5 times longer in duration, this function weighs the duration down by a factor. Another heuristic used was to rank words closer to the front of the phrases are higher in score because the confidence of their duration interval is higher.
