
from antColony import AntColony

if __name__ == '__main__':
    print(*AntColony('testInstances/randomNegativeErr/9.200-80.txt').solve(), sep='\n')
