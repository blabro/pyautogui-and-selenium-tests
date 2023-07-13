import glob

read_files = glob.glob("C:\\Users\\Comarch\\Documents\\ARB\\BR_ACR_015_R_roboczy\\*.txt")

with open("result.txt", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())

with open("C:\\Users\\Comarch\\Documents\\pythonscripts\\mojeProste\\result.txt", "r+") as f:
    d = f.readlines()
    f.seek(0)
    with open("C:\\Users\\Comarch\\Documents\\pythonscripts\\mojeProste\\result1.txt", "a+") as g:
        for i in d:
            if "CRC244" in i:
                g.write(i)