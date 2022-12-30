import numpy as np
import os
def add(id1, chat_id):
	if os.path.exists("top" + str(chat_id) + ".npy") == False:
		topl = np.zeros((100, 2))

	else:
		topl = np.load("top" + str(chat_id) + ".npy")

	if not id1 in topl:
		
		for sc_c in range(99):
			if topl[sc_c][0] == 0:
				topl[sc_c][0] = id1
				topl[sc_c][1] += 1
				break

	else:
		for sc_c in range(99):
			if topl[sc_c][0] == id1:
				topl[sc_c][1] += 1


	np.save("top" + str(chat_id) + ".npy", topl)

def sort(chat_id):
	if os.path.exists("top" + str(chat_id) + ".npy") == False:
		topl = np.zeros((100, 2))

	else:
		topl = np.load("top" + str(chat_id) + ".npy")

	for x_s in range(100):
		for x in range(99):
			if topl[x][1] < topl[x + 1][1]:
				topid = round(topl[x][0])
				topsc = round(topl[x][1])

				topl[x][1] = round(topl[x + 1][1])
				topl[x][0] = round(topl[x + 1][0])

				topl[x + 1][1] = topsc
				topl[x + 1][0] = topid
	count = 0
	for x_p in range(5):
		print(round(topl[x_p][0]))
		if topl[x_p][0] != 0:
			count += 1
	

	np.save("top" + str(chat_id) + ".npy", topl)
	return topl, count
	

