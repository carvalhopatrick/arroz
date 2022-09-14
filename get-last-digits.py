with open('D:/pi/pi23.txt') as f:
	f.seek(0)
	print("start: ", f.read(50))
	a = f.seek(0, 2)
	a -= 50
	f.seek(a)
	print("end: ", f.read(50))
	print("end index: ", a)