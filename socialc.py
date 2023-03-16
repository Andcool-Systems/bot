import numpy as np
import os

def open_file(path):
	if os.path.exists(f"SocialScore{path}.txt") == False:
		sc = np.zeros((100, 2))
		for scc_f in range(99):
			sc[scc_f][1] = 500
	else:
		sc_file = open(f"SocialScore{path}.txt", 'r')
		i = 0
		sc = np.zeros((100, 2))
		for line in sc_file:
			sc[i] = line.split("/")
			i += 1

		sc_file.close()

	return sc

def save_file(path, data):

	sc_file = open(f"SocialScore{path}.txt", 'w')
	i = 0
	for line in range(100):
		sc_file.write(f"{data[i][0]}/{data[i][1]}\n")
		i += 1

	sc_file.close()




def SocialScore(id1, am, chat_id):
	sc = open_file(chat_id)

	finded = False
	for sc_c in range(99):
		if sc[sc_c][0] == id1:
			sc[sc_c][1] += am
			finded = True


	if finded == False:
		for sc_c_n in range(99):
			if sc[sc_c_n][0] == 0:
				sc[sc_c_n][0] = id1
				sc[sc_c_n][1] += am


				break
	save_file(chat_id, sc)

def SocialScore_set(id1, am, chat_id):
	sc = open_file(chat_id)

	finded = False
	for sc_c in range(99):
		if sc[sc_c][0] == id1:
			sc[sc_c][1] = am
			finded = True


	if finded == False:
		for sc_c_n in range(99):
			if sc[sc_c_n][0] == 0:
				sc[sc_c_n][0] = id1
				sc[sc_c_n][1] = am


				break
	save_file(chat_id, sc)

def SocialScore_setp(id1, am, chat_id):
	sc = open_file(chat_id)

	finded = False
	for sc_c in range(99):
		if sc[sc_c][0] == id1:
			sc[sc_c][1] = am
			finded = True


	if finded == False:
		for sc_c_n in range(99):
			if sc[sc_c_n][0] == 0:
				sc[sc_c_n][0] = id1
				sc[sc_c_n][1] = am


				break
	save_file(chat_id, sc)





def show(id1, chat_id):
	sc = open_file(chat_id)

	finded = False
	sc_am = 0
	for sc_c in range(99):
		if sc[sc_c][0] == id1:
			finded = True
			sc_am = sc[sc_c][1]

	if finded == False:
		for sc_c_n in range(99):
			if sc[sc_c_n][0] == 0:
				sc[sc_c_n][0] = id1
				sc_am = sc[sc_c_n][1]
				break
	return sc_am



