import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('path',  default=None, help='path to your data file')
args = parser.parse_args()

df = pd.read_csv(args.path) 
df.columns = df.columns.str.strip()
dfs = [] 
#split on b 
grouped = df.groupby(df.b)
for bVal in df['b'].unique(): 
    dfs.append(grouped.get_group(bVal))

#Hops vs Loop Vals for each B, split on b (there are 9 loop vals)
bCount = 2
for frame in dfs:
    dfsIn = [] 
    #split on b 
    grouped = frame.groupby(frame.B)
    for before in frame['B'].unique(): 
        dfsIn.append(grouped.get_group(before))
    counter = 0 
    markers = ['tab:blue','tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:cyan',  'tab:olive']
    before = 1
    for frameB in dfsIn:
        if (counter == 0): 
            ax = frameB.plot.scatter(x = 'LoopVal', y = 'Hops', color = markers[counter], label=before)
        else: 
            frameB.plot.scatter(x =  'LoopVal', y = 'Hops', color = markers[counter], ax = ax, label=before)
        counter += 1 
        before +=1
    ax.legend(title="Hops before Loop")
    ax.set_xlabel("Loop Length")
    ax.set_ylabel("Hops")
    ax.get_figure().savefig("_".join(args.path.split("_")[0:4]) +"_Plots/" + str(bCount) + "_" +  args.path[: len(args.path) - 3] + "png") 
    bCount += 1
