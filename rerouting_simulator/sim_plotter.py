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
    markers = ['#658cbb','#03012d', '#758da3', '#840000']
    before = 1
    for frameB in dfsIn:
        if (counter == 0): 
            ax = frameB.plot(x = 'LoopVal', y = 'Hops', color = markers[counter], label=before, linestyle="-", marker='o')
       
        else: 
            frameB.plot(x =  'LoopVal', y = 'Hops', color = markers[counter], ax = ax, label=before, linestyle="-", marker='o')
           
        counter += 1 
        before +=1
    ax.legend(title="Hops before Loop")

    ax.set_xlabel("Loop Length")
    ax.set_ylabel("Hops")
    ax.get_figure().savefig("_".join(args.path.split("_")[0:4]) +"_Plots/" + str(bCount) + "_" +  args.path[: len(args.path) - 3] + "png") 
    bCount += 1
