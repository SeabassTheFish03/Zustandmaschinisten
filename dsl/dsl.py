def readFile(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        # What command are we doing?
        if line.startswith("LOAD"):
            pass
