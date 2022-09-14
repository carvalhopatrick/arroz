import time
import math
from concurrent import futures
import sys
import multiprocessing as mp

MINSIZE = 22						# minimum size of the palindromic prime to be searched
BUFSIZE = 100*10**6					# size (number of digits) of each worker Pi buffer
OVERLAPING = 28						# size of overlaping between Pi buffers
MAX_WORKERS = 5						# max ammount of concurrent workers
MAX_PROCS = 2*MAX_WORKERS			# max ammount of prepared processes in pool (a high amount will waste RAM)
START_IDX = 75599978832				# min Pi digit index to search
END_IDX = -1				# max Pi digit index to search (-1 to until end of file)
INPUT_FILE = "D:/pi/pi23.txt"				# path to input file with pi digits
OUTPUT_FILE = "./outputs/run23.log"		# path to output log (with results)

# add last digits from previous file to concatenate with first digits of current run (leave '' for empty)
PREVIOUS_DIGITS = ''

class Searcher:
	def __init__(self, pi, idx):
		self.pi = pi
		self.start_idx = idx
		self.log(f"New searcher // st idx: {idx}")

	def log(self, str):
		with lock:
			with open(OUTPUT_FILE, 'a+') as f:
				f.write(str + '\n')
			print(str, flush=True)

	# checks if number is prime (slow method, but adequate for this use case)
	def is_prime(self, n):
		for i in range(2, int(math.sqrt(n))+1):
			if (n % i) == 0:
				return False
		return True

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

	# searches for palindromes and primes in a string full of pi digits
	def search(self):
		pi = self.pi

		for idx in range(MINSIZE//2, len(pi)-1): # no need to check indexes less than the minimum size we are searching
			pal = self.is_palindrome(idx)
			if (pal):
				self.log(f"palindrome found! size: {len(pal)} // center idx: {self.start_idx + idx} // pal: {pal}")

			# if (self.is_prime(int(''.join(pal)))):
			# 	self.log(f'!!! PRIME PALINDROME FOUND! size: {len(pal)} // idx: {idx} // pal: {pal}')
			# 	return (idx, pal)
			# else:
			# 	self.log(f"palindrome is not prime. idx: {idx}")

		self.log(f"end searcher // st idx: {self.start_idx}")
		return False

def spawn_process(buf, idx):
	s = Searcher(buf, idx)
	ret = s.search()
	return ret

def init_pool(main_lock):
	global lock
	lock = main_lock

def main():
	# open local file with pi digits
	with open(INPUT_FILE, 'r') as f:
		if (END_IDX == -1):
			f_limit = f.seek(0, 2)  # seek to end of file
		else:
			f_limit = END_IDX
		f_idx = f.seek(START_IDX)

		print(f"Starting search in {INPUT_FILE}")
		print(f"number of digits: {f_limit - START_IDX}")
		print(f"number of processes needed: {(f_limit - START_IDX) // (BUFSIZE + OVERLAPING)}")
		print(f"simultaneous processes limit: {MAX_WORKERS}")
		print(f"max processes in pool: {MAX_PROCS}")
		print(f"memory requirement: {(MAX_PROCS)*(BUFSIZE) // (1000*1000)} MB\n")
		
		main_lock = mp.Lock()

		with futures.ProcessPoolExecutor(initializer=init_pool, initargs=(main_lock,), max_workers=MAX_WORKERS) as pool:
			procs = set()
			done = set()
			buf = f.read(BUFSIZE)

			previous_len = 0
			if (PREVIOUS_DIGITS != ''):
				buf = PREVIOUS_DIGITS + buf
				previous_len = len(PREVIOUS_DIGITS)

			while (buf != '' and f_idx <= f_limit): 
				# wait until there is avilable space on the pool
				while (len(procs) >= MAX_PROCS):
					done, procs = futures.wait(procs, return_when=futures.FIRST_COMPLETED)

				p = pool.submit(spawn_process, buf, f_idx - previous_len)
				previous_len = 0
				procs.add(p)

				f_idx += BUFSIZE - OVERLAPING   
				f.seek(f_idx)		# rewinds read pointer to not miss combinations in the next search
				buf = f.read(BUFSIZE)

		return f_idx

if __name__ == '__main__':
	assert BUFSIZE > MINSIZE
	assert MAX_PROCS >= MAX_WORKERS
	if (END_IDX != -1):
		assert END_IDX > START_IDX
	if (PREVIOUS_DIGITS):
		assert START_IDX == 0

	start_time = time.time()
	last_idx = main()
	print(f'searched {last_idx-START_IDX} digits in {(time.time()-start_time):.2f} seconds')
	print(f'last safe index: {last_idx-BUFSIZE-OVERLAPING}')
	sys.stdout.flush()