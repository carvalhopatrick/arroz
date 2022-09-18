from distutils.log import error
import json
import os, time, subprocess
import glob
import searcher

DATAFILE = "./control_data.json"
LOGFILE = "./logs/control.log"
IS_CLOUD = False

def main():
	txt_list = []
	file_number = 0

	while(file_number <= 1000):
		# wait for txt to finish download nad conversion
		while (len(txt_list) == 0):
			txt_list = glob.glob('./input/*.txt')
			time.sleep(2)
		
		# read data from previous run
		with open(DATAFILE, 'r') as jsonfile:
			data = json.load(jsonfile)

		data['file_number'] += 1
		input_file = txt_list[0]

		with open(LOGFILE, 'a+') as lf:
			str = f"Starting search in {input_file}"
			print(str, flush=True)
			lf.write(str)
			# if txt filename differs from expected
			if (input_file != f"pi{data['file_number']}.txt"):
				str = f"ERROR: txt filename is wrong. Expected: pi{data['file_number']}.txt"
				str + "\ncontinuing anyway..."
				print(str, flush=True)
				lf.write(str)
		# parameters >> start(input_file, file_number, start_idx, end_idx, previous):
		# last_digits = searcher.start(input_file=input_file, file_number=file_number,
										# start_idx=0, end_idx=-1, last_digits=data['last_digits']) 

		# escrever no json - last digits e novo i
		data['last_digits'] = 222222
		with open(DATAFILE, 'w') as jsonfile:
			json.dump(data, jsonfile)
			jsonfile.truncate()

		# backup palindromes file
		subprocess.run(f"cp palindromes/palindromes.txt palindromes/palindromes{data['file_number']}.txt")
		# delete txt file
		os.remove(input_file)

		with open(LOGFILE, 'a+') as lf:
			str = f"Finished search in {input_file}"
			print(str, flush=True)
			lf.write(str)

if __name__ == '__main__':
	print("Starting controller...\n")
	main()