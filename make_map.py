import sys,os

if __name__ == '__main__':
    f = open(os.path.dirname(os.path.abspath(__file__)) + "/Data/Maps/" + "standard.txt", "w+")
    for idx in range(100):
        f.write("{}: Place {}\n".format(idx,idx))
    f.close()
