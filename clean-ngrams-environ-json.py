#!/usr/bin/python
import sys
import re
import pprint
import json

if len(sys.argv) is not 3:   
	print "USAGE: {0} input_filename output_filename.json".format(sys.argv[0])
	print "input should be google ngrams data"
	print "       format: ngram year match_count vol_count (tab-separated)"
	quit()

input_filename = sys.argv[1]
output_filename = sys.argv[2]

input_dict = {}
fields = []

with open(input_filename, 'r') as f:
	l = f.readline()
	while l:

		# load the fields 
		fields = l.split('\t')
		if len(fields) is not 4:
			print "ERROR: wrong number of fields ({1}) in line: {0}".format(l, len(fields))
			quit()
		token = fields[0].lower() # convert to all lower-case
		year = fields[1]
		match_count = int(fields[2])
		volume_count = int(fields[3])

		# here is where the cleaning takes place, throwing away punctuation, numbers, misspellings, p.o.s. at ends of words
		# note that order of attempts to match is very important
		# re.match matches only at the beginning of the token/line
		if re.match('environmentally', token):
			token = 'environmentally'
		elif re.match('environmentalizing', token):
			token = 'environmentalizing'
		elif re.match('environmentalization', token):
			token = 'environmentalization'
		elif re.match('environmentalistic', token):
			token = 'environmentalistic'
		elif re.match('environmentalist', token):
			token = 'environmentalist'
		elif (re.match('environmentalism', token) or re.match('environmentaiism', token) or re.match('environmcntalism', token) 
			or re.match('environmemalism', token)):
			token = 'environmentalism'
		elif (re.match('environmental', token) or re.match('environmenal', token) or re.match('environmenial', token) 
			or re.match('environemtnal', token) or re.match('environmnetal', token) or re.match('environmentat', token) 
			or re.match('environlental', token) or re.match('environemtal', token) or re.match('environmenral', token) 
			or re.match('environaental', token) or re.match('environmnetal', token) or re.match('environmenral', token) 
			or re.match('environemtal', token) or re.match('environnental', token) or re.match('environomental', token) 
			or re.match('environemental', token) or re.match('environemntal', token) or re.match('environental', token) 
			or re.match('environinental', token) or re.match('environmantal', token) or re.match('environmemtal', token) 
			or re.match('environmenlal', token) or re.match('environmeutal', token) or re.match('environmmental', token)
			or re.match('environmnental', token) or re.match('environmntal', token)):
			token = 'environmental'
		elif (re.match('environments', token) or re.match('environmenis', token) or re.match('environmenls', token) 
			or re.match('environrnents', token) or re.match('environaents', token) or re.match('environements', token) 
			or re.match('environemnts', token) or re.match('environents', token) or re.match('environmems', token)):
			token = 'environments'
		elif (re.match('environment', token) or re.match('environmenf', token) or re.match('environmnet', token) or re.match('environmet', token)
			or re.match('environrnent', token) or re.match('environmcnt', token) or re.match('environoment', token) 
			or re.match('environrnent', token) or re.match('environmont', token) or re.match('environaent', token) 
			or re.match('environemnt', token) or re.match('environemt', token) or re.match('environemtn', token) 
			or re.match('environinent', token) or re.match('environmemt', token) or re.match('environmenl', token) 
			or re.match('environmerit', token) or re.match('environmert', token) or re.match('environmeut', token) 
			or re.match('environmment', token) or re.match('environmnent', token) or re.match('environmnt', token) 
			or re.match('environmsnt', token) or re.match('environmant', token)):
			token = 'environment'


		# add to dictionary
		if input_dict.get(token):
			if input_dict[token].get(year):
				input_dict[token][year]['match_count'] += match_count
				input_dict[token][year]['volume_count'] += volume_count
			else:
				input_dict[token][year] = {'match_count':match_count, 'volume_count':volume_count}
		else:
			input_dict[token] = {}
			input_dict[token][year] = {'match_count':match_count, 'volume_count':volume_count}

		# read next line from file
		l = f.readline()


# print dict to stdout  with pretty formatting
# pprint.pprint(input_dict)

#output dict as json
try:
	with open(output_filename, 'w') as f:
		f.write(json.dumps(input_dict))
except:
	print "ERROR: exception while writing output file {0}".format(output_filename)


