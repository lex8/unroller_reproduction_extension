import random

l = []

with open("routing_tables/complex/complex1.csv", "r") as f:
  l = f.readlines()
  l = [( int(i.split(":")[0]), i) for i in l]

with open("topologies/complex.csv", "w") as f:
  l.sort(key=lambda x:x[0])
  print(l)
  for i in range(len(l)):
    f.write(l[i][1])
    #f.write(str(random.randint(1, 30)) + ", " + str(random.randint(1, 30)) + "\n")
  f.close()

