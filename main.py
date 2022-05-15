
from antColony import AntColony

if __name__ == '__main__':
    max_len: int = 209
    print(
        *AntColony('testInstances/randomPositiveErr/9.200+80.txt', max_len).solve(),
        sep='\n'
    )
