from gurobipy import *
import numpy as np

#Reading the data from the file
with open('Data/data1/TestProb.txt') as f:
    lines = f.readlines()
    
#Reads the firstline
firstLine = lines[0].split()
secondLine = lines[1].split()
# Size of the big bin where the samll items are to be packed
#Reads the size of the big bin(width, height)
size = [int(secondLine[0]),int(secondLine[1])] 

 #Reads the number of items that we need to pack
item_count_original = int(firstLine[0])  

#Reads the individual width and height of items.
length = []
height = []
value = []
minv = []
maxv = []
for i in range(2, item_count_original+2):
    line = lines[i]
    parts = line.split()
    
    #Make a list of the 'widths' of the items
    length.append(int(parts[0]))
    
    #Make a list of the 'heights' of the items
    height.append(int(parts[1]))
    
    #Make a list of the 'values' of the items
    value.append(int(parts[4])) #Make a list of the 'values' of the items
    minv.append(int(parts[2]))
    maxv.append(int(parts[3]))
#for i in range(len(length)):
#    value.append(length[i]*height[i])

#
z = 0
for i in range(item_count_original):
    z += height[i]
    
#Min and Max number of same items allowed for each items
#minmax = []
#for i in range(item_count_original):
#    n = [minv[i], maxv[i]]
#    minmax.append(n)

#list of the item sizes in original problem (width, height)
item_size =[]  
for i in range(item_count_original):
    b =[length[i], height[i]]
    item_size.append(b)
    
#Breakdown of items into 1-D components
item_size_1d = []
for i in range(item_count_original):
    d = item_size[i]
    c = d[1]
    item_size_1d.append(c)
k = 1
lis = []
lis1 = []

lis_1d = [] #list of the items size in 1-dimension where(width if 1 for all items, height)

for i in range(len(item_size_1d)):
    len_x = item_size_1d[i]
    for j in range(len_x):
        lis.append(k)
        
for i in range(len(height)):
    for j in range(height[i]):
        lis1 = [length[i], lis[i]]
        lis_1d.append(lis1)
        

#BreakDown of Values of the items
#BreakDown of Values of the items: We divide the value of the items based on how many parts any
#item is divided.
val_1d = []
for i in range(len(height)):
    d = value[i]/height[i]
    for j in range(height[i]):
        val_1d.append(d)
        
#Now we use column generation to solve this one dimensional problem that gives us the minimum number
#1-D bins where all of our 1-D items are packed. Then the associated value of the individual 
#1-D bins will be calculated based on the number of items and their values. Since we divide the 
#according to how many items we break our 2-D bin to make it 1-D. Just adding the corresponding
#value of the 1-D item will gives us the value of the 1-D bin. 

#After we calculate the value of each bin , since we want to maximize the value of items packed
#into the bin we can solve the Knapsack Problem where the value of the items in the knapsack is 
#maximized.

#Solving it with 1D column generation
L = size[0]
#
#Here the length of the items implies the height of the items in original problem. We divided the big
#bin into equal parts so, along the height we solve it as a 1-D cutting/packing problem using 
#column generation.
length_of_items = []
for i in range(len(lis_1d)):
    d = lis_1d[i]
    v = d[0]
    length_of_items.append(v)
item_count = len(length_of_items)

#Determining the demands of the components of each items. The demand for each
# item is that the all the components of the items are to be packed. 
demand_per_item = []
for i in range(len(item_size)):
    d = item_size[i][1]
    demand_per_item.append(d)
    
    
#Solving the column generation 
#THE MASTER PROBLEM: We start of problem with the known feasible column and the gradually we
# add the promising columns to our master problem and solve it recursively.
M = Model('Master Problem')
s = M.addVars(item_count,name='s',obj=1)
c = M.addConstrs(s[i] >= 1 for i in range(item_count))
M.update()
M.setObjective(sum(s[i] for i in range(item_count)), GRB.MINIMIZE)
M.optimize()
M.update()


#THE PRICING PROBLEM
PP  = Model('Pricing Problem')
pv  = PP.addVars(item_count, obj=-1, vtype=GRB.INTEGER, name='w')
expr = LinExpr([length_of_items[i], pv[i]] for i in range(item_count))
PP.addConstr(expr <= L )
PP.update()

pattern_list = []
PP.Params.OutputFlag=0
for i in range(item_count):
    obj    = {i:-1 for i in range(item_count)}
    obj[i] = - L-1
#   pattern_list.append(items)
    PP.setObjective(pv.prod(obj))
    PP.optimize()
    colmn = []
    for v in PP.getVars():
        colmn.append(v.X)
    pattern_list.append(colmn)

    col = Column()
    for j in range(item_count):        
        col.addTerms(pv[j].X, c[j])
    M.addVar(obj = 1, column = col)
#    pattern_list.append(col)
M.optimize()
#print(*pattern_list, sep = '\n')

M.Params.OutputFlag = 0
Iter = 0
print('Iteration MasterValue PricingValue')
while M.Status == GRB.OPTIMAL:
    pi = { i : -c[i].Pi for i in range(item_count)}
    PP.setObjective(pv.prod(pi))
    PP.optimize()
    # This should not happen... but better safe than sorry
    if PP.Status != GRB.OPTIMAL:
        raise('Unexpected optimization status')
    
    if PP.ObjVal > -1.0001:
        break
#    pattern_list.append(item_count)
    patt = []
    for v in PP.getVars():
        patt.append(v.X)
    pattern_list.append(patt)

    # Log
#    if Iter % 20 == 0:
#        print('Iteration MasterValue PricingValue')
    print('%8d %12.5g %12.5g' % (Iter, M.ObjVal, PP.ObjVal))
    Iter += 1
    
    # Using solution, build new variable
    col = Column()
    for j in range(item_count):
        col.addTerms(pv[j].X,  c[j])
    M.addVar(obj=1, column=col)
    M.optimize()
#    pattern_list.append(col)
#M.write('final.lp')
rootbound = M.ObjVal
#print(*pattern_list, sep = '\n')

#Calculating the value of patterns: The value of the pattern is the sum of value of individual 1-D
#item that belongs to that column. 
val_patterns = []
for i in range(len(pattern_list)):
    ind_val = np.array(val_1d) * np.array(pattern_list[i])
    val_patterns.append(ind_val)

#Value of each pattern
pattern_val = []
for i in range(len(val_patterns)):
    ind_sum = sum(val_patterns[i])
    pattern_val.append(ind_sum)
# So here, 'pattern_val' gives the value of each patterns we obtained using column generation.

#Sum of the length of the items
len_item = [0]
len_items = []
len_items.append(height[0])
for i in range(1,len(height)):
    c = len_items[i-1] + height[i]
    len_items.append(c)
sum_of_len_items = len_item + len_items
#sum_of_len_items = [0, 2, 3, 6, 7, 10, 13, 14, 19]

#array of items  abc =[0, 0, 1, 2, 2, 2, 3, 4, 4, 4, 5, 5, 5, 6, 7, 7, 7, 7, 7]
abc = []
for i in range(len(height)):
    ab = height[i]
    for j in range(ab):
        abc.append(i)
       
#lent_item = []
#for i in range(item_count_original):
#    lent_item.append(0)

# Here 'pki' represents the number of items 'i' generated by pattern 'k'
pki = []
pk = []    
for i in range(len(pattern_list)):
    lent_item = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for j in range(len(pattern_list[i])):
        if pattern_list[i][j] != 0:
            h = pattern_list[i][j]
            l = abc[j]
            lent_item[l] = h
    pki.append(lent_item)
#
#
# Removing the duplicate items in the list pki
p_k_i = []
for i in pki:
    if i not in p_k_i:
        p_k_i.append(i)
#
## Now since we generated the columns we have to solve a relaxed optimization
## problem so that the value of the items packed is maximized. We consider 
## the relaxation when all components of each items are packed. 
len_patt = len(p_k_i)


##Here 'number_of_items_per_pattern' give the number of element i from each pattern
number_of_items_per_pattern = []
for i in range(item_count_original):
    abcd = []
    for j in range(len_patt):
        abcd.append(p_k_i[j][i])
    number_of_items_per_pattern.append(abcd)
    
#This represent the demand of each patterns, that is the length of each item. 
demand = []
for i in range(len(height)):
    demand.append(height[i])
    
    
M = Model('Maximization Problem')

y = M.addVars(item_count_original, vtype = GRB.INTEGER, name = 'y', obj = value)

x = M.addVars(len_patt, vtype = GRB.CONTINUOUS, name = 'x')

M.update()

for i in range(item_count_original):
    M.addConstr(sum(number_of_items_per_pattern[i][j] * x[j] for j in range(len_patt)) >= demand[i]*y[i])

M.addConstr(sum(x[i] for i in range(len_patt)) == size[1])

for i in range(item_count_original):
    M.addConstr(y[i] >= minv[i])
    M.addConstr(y[i] <= maxv[i])
#M.addConstr(x[2] <= 0)

M.update()
M.modelSense = GRB.MAXIMIZE
 
M.optimize()
#M.write("result.sol")
#Patterns Used.
used_pattern = []
#print('Pattern Used            Pattern Value')  
for i in range(len_patt):
    if (x[i].x) != 0:
        for j in range(int(x[i].x)):
            used_pattern.append(i)
        
#        print('%8d %24f ' % (i, pattern_val[i]))
used_pattern_list = []
for i in range(len(used_pattern)):
    a = p_k_i[used_pattern[i]]
    used_pattern_list.append(a)

v = len(used_pattern_list)
ab = []
for i in range(v):
    #b = np.multiply(used_pattern_list[i],height)
    b = [c*d for c,d in zip(used_pattern_list[i],length)]
    ab.append(b)
n = 0
for i in range(len_patt):
    n += x[i].x
    