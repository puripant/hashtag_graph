import sys
from datetime import datetime
import itertools

if len(sys.argv) < 3:
	sys.exit()

#preprocessed list of tuples of tags and time
tweets = [] 

#open input file
with open(sys.argv[1]) as tweets_file:
	for line in tweets_file:
		if line == "\n": #stop before the last line: unicode counter
			break
		
		(text, time_text) =  line.rsplit(" (timestamp: ", maxsplit=1)
		
		#convert to datetime object; remove  ) and \n first
		time = datetime.strptime(time_text[:-2], "%a %b %d %H:%M:%S %z %Y") #e.g. Thu Oct 29 17:51:01 +0000 2015
		
		#find unique hashtags
		tags = set([word for word in text.lower().split() if word.startswith("#")])
		
		tweets.append((tags, time))

#a pointer to maintain 60-second window
tweet_to_remove_idx = 0
	
#keep the graph structure and result
edges = {} #dictionary of edge name (two sorted nodes) to its counter (to make sure when to remove)
nodes = {} #dictionary of node name (hashtag) to its counter (to make sure when to remove)
avg_degrees = []
		
for tweet_idx in range(len(tweets)):
	tags, time = tweets[tweet_idx]
	
	#check old tweets
	for idx in range(tweet_to_remove_idx, tweet_idx):
		old_tags, old_time = tweets[idx]
		if (time - old_time).seconds > 60:
			#decrease edge and node coutners related to old_tags
			if len(tags) > 1:
				for pair in itertools.combinations(old_tags, 2):
					for tag in pair:
						#tag must exist
						nodes[tag] -= 1
						if nodes[tag] == 0:
							del nodes[tag]
					
					reversed_pair = (pair[1], pair[0])
					#pair or reversed_pair must exist
					if pair in edges:
						edges[pair] -= 1
						if edges[pair] == 0:
							del edges[pair]
					else:
						edges[reversed_pair] -= 1
						if edges[reversed_pair] == 0:
							del edges[reversed_pair]
			
			tweet_to_remove_idx += 1
		else:
			break
	
	#check (one) new tweet
	if len(tags) > 1:
		for pair in itertools.combinations(tags, 2):
			#keep track of nodes
			for tag in pair:
				if tag in nodes:
					nodes[tag] += 1
				else:
					nodes[tag] = 1
			
			#keep track of edges
			reversed_pair = (pair[1], pair[0])
			if pair in edges:
				edges[pair] += 1
			elif reversed_pair in edges:
				edges[reversed_pair] += 1
			else:
				edges[pair] = 1
	
	#calculate the average degree; each edge has two nodes i.e. adding two degrees
	avg_degrees.append(2*len(edges)/len(nodes) if len(nodes) > 0 else 0)

#write output
with open(sys.argv[2], "w") as output_file:
	for num in avg_degrees:
		output_file.write("{0:.2f}\n".format(num)) #format degree to 2 decimal places