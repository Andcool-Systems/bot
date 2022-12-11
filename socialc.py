import numpy as np
import os
def SocialScore(id1, am, chat_id):
	if os.path.exists("SocialScore" + str(chat_id) + ".npy") == False:
		sc = np.zeros((3, 100))
		for sc_c_f in range(99):
			sc[1][sc_c_f] = 500

	else:
		sc = np.load("SocialScore" + str(chat_id) + ".npy")
	finded = False
	for sc_c in range(99):
		if sc[0][sc_c] == id1:
			sc[1][sc_c] += am
			finded = True


	if finded == False:
		for sc_c_n in range(99):
			if sc[0][sc_c_n] == 0:
				sc[0][sc_c_n] = id1
				sc[1][sc_c] += am


				break
	np.save("SocialScore" + str(chat_id) + ".npy", sc)

def SocialScore_set(id1, am, chat_id):
	if os.path.exists("SocialScore" + str(chat_id) + ".npy") == False:
		sc = np.zeros((3, 100))
		for sc_c_f in range(99):
			sc[1][sc_c_f] = 500

	else:
		sc = np.load("SocialScore" + str(chat_id) + ".npy")
	finded = False
	for sc_c in range(99):
		if sc[0][sc_c] == id1:
			sc[1][sc_c] = am
			finded = True


	if finded == False:
		for sc_c_n in range(99):
			if sc[0][sc_c_n] == 0:
				sc[0][sc_c_n] = id1
				sc[1][sc_c] = am


				break
	np.save("SocialScore" + str(chat_id) + ".npy", sc)

def SocialScore_setp(id1, am, chat_id):
	if os.path.exists("SocialScore" + str(chat_id) + ".npy") == False:
		sc = np.zeros((3, 100))
		for sc_c_f in range(99):
			sc[1][sc_c_f] = 500

	else:
		sc = np.load("SocialScore" + str(chat_id) + ".npy")
	finded = False
	for sc_c in range(99):
		if sc[0][sc_c] == id1:
			sc[2][sc_c] = am
			finded = True


	if finded == False:
		for sc_c_n in range(99):
			if sc[0][sc_c_n] == 0:
				sc[0][sc_c_n] = id1
				sc[2][sc_c] = am


				break
	np.save("SocialScore" + str(chat_id) + ".npy", sc)


def SocialScore_erase(id1, chat_id):
	if os.path.exists("SocialScore" + str(chat_id) + ".npy") == False:
		sc = np.zeros((3, 100))
		for sc_c_f in range(99):
			sc[1][sc_c_f] = 500

	else:
		sc = np.load("SocialScore" + str(chat_id) + ".npy")
	
	for sc_c in range(100):
		if sc[0][sc_c] == id1:
			sc[0][sc_c] = 0
			sc[1][sc_c] = 500
			sc[2][sc_c] = 0








	np.save("SocialScore" + str(chat_id) + ".npy", sc)


def show(id1, chat_id):
	if os.path.exists("SocialScore" + str(chat_id) + ".npy") == False:
		sc = np.zeros((3, 100))
		for sc_c_f in range(99):
			sc[1][sc_c_f] = 500

	else:
		sc = np.load("SocialScore" + str(chat_id) + ".npy")
	finded = False
	sc_am = 0
	for sc_c in range(99):
		if sc[0][sc_c] == id1:
			finded = True
			sc_am = sc[1][sc_c]

	if finded == False:
		for sc_c_n in range(99):
			if sc[0][sc_c_n] == 0:
				sc[0][sc_c_n] = id1
				sc_am = str(sc[1][sc_c])
				break
	return sc_am



