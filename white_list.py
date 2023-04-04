import numpy as np
import os
import file_manager

def add_to_whitelist(id1, chat_id):
	whiteL = file_manager.open("whitList", chat_id, 1)

	if not id1 in whiteL:
		done = True
		whiteL = np.append(whiteL, [[id1]], axis = 0)

	else:
		done = False

	file_manager.save("whitList", chat_id, whiteL)
	return done

def is_in(id1, chat_id):
	whiteL = file_manager.open("whitList", chat_id, 1)

	return id1 in whiteL

def remove_from_whitelist(id1, chat_id):
	whiteL = file_manager.open("whitList", chat_id, 1)

	if id1 in whiteL:
		done = True
		for sc_c in range(len(whiteL)):
			if whiteL[sc_c][0] == id1:
				whiteL[sc_c][0] = 0
				break

	else:
		done = False

	file_manager.save("whitList", chat_id, whiteL)
	return done