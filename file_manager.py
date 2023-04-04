import numpy as np
import os

def open(name, chat_id, am):
	return np.zeros(am).reshape(1, am) if not os.path.exists(f"{name}{chat_id}.npy") else np.load(f"{name}{chat_id}.npy", allow_pickle=True)


def save(name, chat_id, list):
	np.save(f"{name}{chat_id}.npy", list)