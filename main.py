
from antColony import AntColony

if __name__ == '__main__':
    print(*AntColony('testInstances/randomNegativeErr/9.200-80.txt').solve(), sep='\n')
    #print(*AntColony('testInstances/edgesPositiveErr/9.200+20.txt').solve(), sep='\n')
