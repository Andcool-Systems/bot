import numpy as np
import os
import file_manager

def add(id1, chat_id):
	topl = file_manager.open("top", chat_id, 2)

	if not id1 in topl: topl = np.append(topl, [[id1, 1]], axis = 0)

	else:
		for sc_c in range(len(topl)):
			if topl[sc_c][0] == id1:
				topl[sc_c][1] += 1


	file_manager.save("top", chat_id, topl)

def sort(chat_id):
	topl = file_manager.open("top", chat_id, 2)

	for x_s in range(len(topl)):
		for x in range(len(topl) - 1):
			if topl[x][1] < topl[x + 1][1]:
				topid = round(topl[x][0])
				topsc = round(topl[x][1])

				topl[x][1] = round(topl[x + 1][1])
				topl[x][0] = round(topl[x + 1][0])

				topl[x + 1][1] = topsc
				topl[x + 1][0] = topid
	count = 0
	for x_p in range(len(topl)):
		print(round(topl[x_p][0]))
		if topl[x_p][0] != 0:
			count += 1
	

	file_manager.save("top", chat_id, topl)
	return topl, count
	

