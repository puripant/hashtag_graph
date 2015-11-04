import sys
import json

if len(sys.argv) < 3:
	sys.exit()

escapes = ["\a", "\b", "\f", "\n", "\r", "\t", "\v"] #"\\", "\'", "\""

tweets = []
unicode_num = 0
#open input file
with open(sys.argv[1]) as tweets_file:
	for line in tweets_file:
		#read each tweet as json
		full_tweet = json.loads(line)
		if "text" in full_tweet:
			text = full_tweet["text"]
			
			#clean up basic escape sequences
			for esc in escapes:
				text = text.replace(esc, "")
				
			#translate the text to bytes then translate back to ascii and ignore all unicodes
			new_text = text.encode().decode("ascii", "ignore")
			if new_text != text:
				unicode_num += 1
			
			tweets.append(new_text + " (timestamp: " + full_tweet["created_at"] + ")")

#write output
with open(sys.argv[2], "w") as output_file:
	for line in tweets:
		output_file.write(line + "\n")
	#write unicode counter
	output_file.write("\n" + str(unicode_num) + " tweets contained unicode.")