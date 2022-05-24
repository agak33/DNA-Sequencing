import random

# constants
SIZE = 10       #długość słów
RANDREM = 60    #ilość losowo usuniętych
RANDADD = 70    #ilość losowo dodanych
SPECADD = 15    #ilość dodanych na końcu oligonukleotydów

f = open("input.txt")
out = open("testInstances/custom/output.txt", "w+")
sequence = f.read()
words = []
print(len(sequence))

# split input
for k in range(len(sequence) - SIZE + 1):
    tmp = sequence[k:k + SIZE]
    words.append(tmp)

def operations(result):
    # delete random
    for i in range(RANDREM):
        result.pop(random.randrange((len(result))))

    # add random
    for i in range(RANDADD):
        tmp = ""
        for j in range(SIZE):
            tmp += (random.choice(("A", "C", "T", "G")))
        result.append(tmp)

    # add special
    for i in range(SPECADD):
        x = random.randint(0, 1)
        getter = random.randrange(len(result))
        if x == 0:
            position = 0
        else:
            position = -1
        temper = list(result[getter])

        if temper[position] == 'A':
            temper[position] = 'T'
        elif temper[position] == 'C':
            temper[position] = 'G'
        elif temper[position] == 'T':
            temper[position] = 'A'
        else:
            temper[position] = 'C'

        result.append(''.join(temper))

    # delete same
    d = {}
    for x in result:
        d[x] = 1
    result = list(d.keys())
    random.shuffle(result)
    return result


Donewords = operations(words)
print(len(Donewords))
for i in Donewords:
    out.write(i)
    out.write("\n")
