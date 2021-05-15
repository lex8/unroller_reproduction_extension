import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('path',  default=None, help='path to your data file')
parser.add_argument('x', default=None, help='x-axis column')
parser.add_argument('y',  default=None, help='y-axis column')
parser.add_argument('line',  default=None, help="value to split lines on (e.x. b in figure 2)")
parser.add_argument('vals',  default=None, help="comma separated values to split data into lines on (e.x. 1,2,3)")
args = parser.parse_args()

df = pd.read_csv(args.path) 
df.columns = df.columns.str.strip()
dfs = [] 
for val in args.vals.split(','):
    dfs.append(df[df[args.line] == int(val)])


counter = 0 
markers = ["s", "o"]
for frame in dfs:
    if (counter == 0): 
        ax = frame.plot.scatter(x = args.x, y = args.y, marker = "x")
    else: 
        frame.plot.scatter(x = args.x, y = args.y, marker = markers[counter - 1], ax = ax)
    counter += 1 
legend = [args.line + "=" + x for x in args.vals.split(',')]
ax.legend(legend)
ax.set_xlabel(args.x)
ax.set_ylabel(args.y)
ax.get_figure().savefig(args.path[: len(args.path) - 3] + "png") 
