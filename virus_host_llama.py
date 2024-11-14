import time
import random
#import pandas as pd
import ollama
import string
import random
import re
from multiprocessing import Pool
#from concurrent.futures import ProcessPoolExecutor
from alive_progress import alive_bar #for progress bar

# Divide the questions into chunks 
# Code to yield successive n-sized chunks from l. 
def divide_chunks(l, n):  
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
  

# Random string generator for filenames
def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

#Function to query ollama and store output in a file
def ollama_response(prompts_list):
	output_file = "output_"+id_generator()+".txt"
	print(len(prompts_list))
	with alive_bar(len(prompts_list)) as bar:
		for question in prompts_list:
			question_edit = re.sub('[.]', ' only output names nothing else.', question, count=1) 
			#print(question_edit)
			random.seed(26)
			response = ollama.generate(model='llama3', prompt=question_edit)
			#print(response['response'])
			f = open(output_file, "a")
			f.write(question_edit+"\n\n\n\n\n"+response['response']+"\n\n\n\n\n\n\n\n\n\n")
			f.close()
			bar()
			time.sleep(5)

if __name__ == '__main__':
	# Read questions from a text file
	with open('/Users/sj1212/Documents/virus_questions.txt', 'r') as f:
        	questions = [line.strip() for line in f.readlines()]	
	
	nques=len(questions)
	print(nques)

	# Divide questions into chunks 
	n = 2000
	x = list(divide_chunks(questions, n))
	print("Length of x: "+str(len(x)))
	y = x
	print("Length of y: "+str(len(y)))
	#print(y[1])
	
	with Pool(len(y)) as p:
		p.map(ollama_response,y)
