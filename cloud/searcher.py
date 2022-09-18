import multiprocessing as mp
import time
from concurrent import futures
from datetime import datetime

MINSIZE = 17						# minimum size of the palindromic prime to be searched
BUFSIZE = 100*10**6					# size (number of digits) of each worker Pi buffer
OVERLAPING = 35						# size of overlaping between Pi buffers
MAX_WORKERS = mp.cpu_count()-1		# max ammount of concurrent workers
MAX_PROCS = 2*MAX_WORKERS			# max ammount of prepared processes in pool (a high amount will waste RAM)
OUTPUT_FILE = "./logs/searcher.log"		# path to output log (with results)
PAL_FILE = "./palindromes/palindromes.log"	# path to palindromes file

class Searcher:
	def __init__(self, pi, idx, file_number):
		self.pi = pi
		self.start_idx = idx
		self.file_number = file_number

		self.log(f"New searcher // st idx: {idx}")

	def log(self, string, pal=False):
		number = str(self.file_number)
		string = f"{number}:\t{string}"

		# mutex to prevent multiple process access at the same time
		with lock:
			with open(OUTPUT_FILE, 'a+') as f:
				f.write(string + '\n')
			# if log is about a palindrome
			if (pal):
				with open(PAL_FILE, 'a+') as fp:
					fp.write(string + '\n')
			print(string, flush=True)

	def is_palindrome(self, idx):
		pi = self.pi
		i = 1

		while (pi[idx-i] == pi[idx+i]):
			i += 1
			if (idx+i >= len(pi) or idx-i < 0):
				if (2*i+1 >= MINSIZE):
					self.log(f"!!!! PALINDROME BREAKS CHUNK LIMIT! idx: {self.start_idx + idx} // i: {i}")
				break
		i -= 1

		if (2*i + 1) >= MINSIZE:
			pal = pi[idx-i : idx+i+1]
			return pal
		else:
			return False

	# searches for palindromes in a string full of pi digits
	def search(self):
		pi = self.pi

		for idx in range(MINSIZE//2, len(pi)-1): # no need to check indexes less than the minimum size we are searching
			pal = self.is_palindrome(idx)
			if (pal):
				self.log(f"palindrome! size: {len(pal)} // center idx: {self.start_idx + idx} // pal: {pal}", True)

		self.log(f"end searcher // st idx: {self.start_idx}")
		return False

def spawn_process(buf, idx, file_number):
	s = Searcher(buf, idx, file_number)
	ret = s.search()
	return ret

def init_pool(main_lock):
	global lock
	lock = main_lock

def get_last_digits(input_file):
	with open(input_file, 'r') as f:
		f.seek(0)
		a = f.seek(0, 2)
		a -= OVERLAPING
		f.seek(a)
		last_digits = f.read(OVERLAPING)
	return last_digits

# previous = last digits from previous file
def run(input_file, file_number, start_idx, end_idx, previous):
	file_number = str(file_number)
	start_time = time.time()
	
	# open local file with pi digits
	with open(input_file, 'r') as f:
		if (end_idx == -1):
			f_limit = f.seek(0, 2)  # seek to end of file
		else:
			f_limit = end_idx
		f_idx = f.seek(start_idx)

		print(f"Starting search in {input_file}")
		print(f"number of digits: {f_limit - start_idx}")
		print(f"number of processes needed: {(f_limit - start_idx) // (BUFSIZE + OVERLAPING)}")
		print(f"simultaneous processes limit: {MAX_WORKERS}")
		print(f"max processes in pool: {MAX_PROCS}")
		print(f"memory requirement: {(MAX_PROCS)*(BUFSIZE) // (1000*1000)} MB\n")
		
		main_lock = mp.Lock()

		with futures.ProcessPoolExecutor(initializer=init_pool, initargs=(main_lock,), max_workers=MAX_WORKERS) as pool:
			procs = set()
			done = set()
			buf = f.read(BUFSIZE)

			previous_len = 0
			if (previous != ''):
				buf = previous + buf
				previous_len = len(previous)

			while (buf != '' and f_idx <= f_limit): 
				# wait until there is avilable space on the pool
				while (len(procs) >= MAX_PROCS):
					done, procs = futures.wait(procs, return_when=futures.FIRST_COMPLETED)

				p = pool.submit(spawn_process, buf, f_idx - previous_len, file_number)
				previous_len = 0
				procs.add(p)

				f_idx += BUFSIZE - OVERLAPING   
				f.seek(f_idx)		# rewinds read pointer to not miss combinations in the next search
				buf = f.read(BUFSIZE)
	
	last_digits = get_last_digits(input_file)
	finish_time = time.time()

	with open(OUTPUT_FILE, 'a+') as of:
		string = f"{file_number}:\trun time: {finish_time} // system time: {datetime.now()}\n{file_number}:\tlast digits: {last_digits}"
		of.write(string + '\n')
		print(string)

	return last_digits


# if ran as standalone script = testing purposes
if __name__ == '__main__':
	last_digits = run(input_file='./input/pi-1b.txt', file_number=22,
									start_idx=0, end_idx=-1, previous='9292992922992') 
	print("!!!!!!!! last digits = " + last_digits)