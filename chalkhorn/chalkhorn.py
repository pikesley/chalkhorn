import sys

from lib.chalkhorn import Chalkhorn

if __name__ == "__main__":
    chalk = Chalkhorn(sys.argv[1:])
    print(chalk)
