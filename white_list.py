import numpy as np
import os
def add_to_whitelist(id1, chat_id):
	if os.path.exists("whitList" + str(chat_id) + ".npy") == False:
		whiteL = np.zeros((100))

	else:
		whiteL = np.load("whitList" + str(chat_id) + ".npy")

	if not id1 in whiteL:
		done = True
		for sc_c in range(99):
			if whiteL[sc_c] == 0:
				whiteL[sc_c] = id1
				break

	else:
		done = False


	np.save("whitList" + str(chat_id) + ".npy", whiteL)
	return done

def is_in(id1, chat_id):
	if os.path.exists("whitList" + str(chat_id) + ".npy") == False:
		whiteL = np.zeros((100))
	else:
		whiteL = np.load("whitList" + str(chat_id) + ".npy")

	return id1 in whiteL

def remove_from_whitelist(id1, chat_id):
	if os.path.exists("whitList" + str(chat_id) + ".npy") == False:
		whiteL = np.zeros((100))

	else:
		whiteL = np.load("whitList" + str(chat_id) + ".npy")

	if id1 in whiteL:
		done = True
		for sc_c in range(99):
			if whiteL[sc_c] == id1:
				whiteL[sc_c] = 0
				break

	else:
		done = False


	np.save("whitList" + str(chat_id) + ".npy", whiteL)
	return done