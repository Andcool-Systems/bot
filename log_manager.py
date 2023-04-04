import pickle as p

def load_data():
    try:
        with open("log.dat", "rb") as f:
            data_list = p.load(f)
    except: data_list = []
    return data_list

def save_data(data):
    with open("log.dat", "wb") as f:
        p.dump(data, f)