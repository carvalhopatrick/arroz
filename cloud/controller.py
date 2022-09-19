from distutils.log import error
import os, time, subprocess
import glob
import searcher
import shutil
import utils
from datetime import datetime

# TODO: api para informar erros/webserver

LOGFILE = "./logs/control.log"

def log(string):
	with open(LOGFILE, 'a+') as lf:
		print(string, flush=True)
		lf.write(string + '\n')

def main():
	log("Starting Downloader...\n")
	downloader_p = subprocess.Popen(["python3", "downloader.py"])

	data = utils.json_read(utils.DATAFILE)
	file_number_bak = data['file_number']
	last_digits_bak = data['last_digits']
	file_number = file_number_bak
	last_digits = last_digits_bak

	while(file_number <= 1000):
		try:
			pitxt_list = []
			# wait for pitxt to finish download and conversion
			while (len(pitxt_list) == 0):
				pitxt_list = glob.glob('./input/*.pitxt')
				if (len(pitxt_list) == 0):
					time.sleep(2)
			
			# read data from previous run
			data = utils.json_read(utils.DATAFILE)

			file_number_bak = data['file_number']
			last_digits_bak = data['last_digits']
			file_number = file_number_bak
			last_digits = last_digits_bak
			input_file = pitxt_list[0]

			log(f"{file_number}:\tStarting search in {input_file}\t{datetime.now()}")
			start_time = time.time()
			# warn if pitxt filename differs from expected, for any reason
			if (input_file != f"./input/pi{file_number}.pitxt"):
					log(f"{file_number}:\tWARNING: pitxt filename is wrong. Expected: pi{file_number}.pitxt - continuing anyway...")

			# parameters >> start(input_file, file_number, start_idx, end_idx, previous):
			last_digits = searcher.run(input_file=input_file, file_number=file_number,
										start_idx=0, end_idx=-1, previous=last_digits) 
			last_digits = str(last_digits)

			# backup palindromes file
			shutil.copyfile("palindromes/palindromes.log", f"palindromes/palindromes{file_number}.log")

			# update json - last digits and new file_number
			data['last_digits'] = last_digits
			data['file_number'] = file_number+1
			utils.json_write(data, utils.DATAFILE)
			
			# delete pitxt file
			os.remove(input_file) 

			log(f"{file_number}:\tFinished search in {input_file} in {time.time() - start_time}s")
		except:
			log(f'{file_number}:\tERROR: controller loop - resetting json to previous run')
			data['file_number'] = file_number_bak
			data['last_digits'] = last_digits_bak
			utils.json_write(data, utils.DATAFILE)
			time.sleep(2)
			continue


if __name__ == '__main__':
	log("Starting Controller...\n")
	main()
