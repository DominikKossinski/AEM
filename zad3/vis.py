import pickle

pickle_in = open("kroA200/NoStyle/ListOfMoves_min_cycle.pkl", "rb")
lom = pickle.load(pickle_in)
lom.visualise(True, "Lom_kroA200", "")
