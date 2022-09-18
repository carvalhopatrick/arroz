from distutils.log import error
import json
import os, time, subprocess
import glob
import searcher
import shutil

DATAFILE = "./control_data.json"
LOGFILE = "./logs/control.log"
IS_CLOUD = False

def log(string):
	with open(LOGFILE, 'a+') as lf:
		print(string, flush=True)
		lf.write(string + '\n')

def json_read(file):
	with open(file, 'r') as jsonfile:
		data = json.load(jsonfile)
	return data

def json_write(data, file):
	with open(file, 'w') as jsonfile:
		json.dump(data, jsonfile)
		jsonfile.truncate()

def main():
	file_number = 0

	while(file_number <= 1000):
		txt_list = []
		# wait for txt to finish download and conversion
		while (len(txt_list) == 0):
			txt_list = glob.glob('./input/*.txt')
			if (len(txt_list) == 0):
				time.sleep(2)
		
		# read data from previous run
		data = json_read(DATAFILE)

		data['file_number'] += 1
		file_number = data['file_number']
		last_digits = data['last_digits']
		input_file = txt_list[0]

		log(f"Starting search in {input_file}")
		# if txt filename differs from expected
		if (input_file != f"pi{file_number}.txt"):
				log(f"ERROR: txt filename is wrong. Expected: pi{file_number}.txt - continuing anyway...")

		# parameters >> start(input_file, file_number, start_idx, end_idx, previous):
		last_digits = searcher.run(input_file=input_file, file_number=file_number,
									start_idx=0, end_idx=-1, previous=last_digits) 

		# escrever no json - last digits e novo i
		data['last_digits'] = str(last_digits)
		json_write(data, DATAFILE)

		# backup palindromes file
		shutil.copyfile("palindromes/palindromes.log", f"palindromes/palindromes{file_number}.log")
		# delete txt file
		# os.remove(input_file) #### TODO

		log(f"Finished search in {input_file}")

if __name__ == '__main__':
	print("Starting controller...\n")
	main()