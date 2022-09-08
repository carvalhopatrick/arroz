with open('./input/pi-1t-01.txt') as f:
	f.seek(99999999855)
	a = f.readline()
	print(a)