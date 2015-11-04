#!/usr/bin/env bash

python3 ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
python3 ./src/average_degree.py ./tweet_output/ft1.txt ./tweet_output/ft2.txt