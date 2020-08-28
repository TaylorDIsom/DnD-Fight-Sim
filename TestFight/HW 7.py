import scipy.optimize
import pulp
from pulp import LpMaximize, LpMinimize, LpProblem,LpBinary, lpSum, LpVariable
import pandas as pd

'''
# dietFile = open()

objFunct = [-1, -2] #coeff for variables x and y
leftIneq = [[2,1],
            [-4,5],
            [1,-2]]
rightIneq = [[20],
             [10],
             [2]]
leftEq = [[-1,5]]
rightEq = [15]

bounds = [(0, float("inf")),
          (0, float("inf"))]

optimization = scipy.optimize.linprog(c = objFunct,
                                      A_ub=leftIneq,
                                      b_ub=rightIneq,
                                      A_eq=leftEq,
                                      b_eq=rightEq,
                                      bounds=bounds,
                                      method="revised simplex")

print(optimization)
print("poop")

pulpModel = LpProblem(name="problem", sense=LpMaximize)
x = LpVariable(name="x", lowBound=0)
y = LpVariable(name="y", lowBound=0)
objective = 2 * x + 4 * y

constraint = 2 * x + 4 * y >= 8
pulpModel += (2 * x + y <= 20, "red_constraint")
pulpModel += (4 * x - 5 * y >= -10, "blue_constraint")
pulpModel += (-x + 2 * y >= -2, "yellow_constraint")
pulpModel += (-x + 5 * y == 15, "green_constraint")

pulpModel += x + 2 * y

status = pulpModel.solve()

print("\n", pulpModel)
print("\n", pulpModel.status, pulpModel.variables(), pulpModel.variables())

for var in pulpModel.variables():
    print(var.value())
'''

df = pd.read_excel("diet.xls")
# print(df.head())
# print(dietData)


cols = df.columns
dietDF = df[0:64]
dietList = dietDF.values.tolist()

foods = [ f[0] for f in dietList ]
prices = [ f[1] for f in dietList ]
servs = [ f[2] for f in dietList ]
calors = [ f[3] for f in dietList ]
chols = [ f[4] for f in dietList ]
fats = [ f[5] for f in dietList ]
sods = [ f[6] for f in dietList ]
carbs = [ f[7] for f in dietList ]
fibs = [ f[8] for f in dietList ]
prots = [ f[9] for f in dietList ]
vitas = [ f[10] for f in dietList ]
vitcs = [ f[11] for f in dietList ]
calcis = [ f[12] for f in dietList ]
irons = [ f[13] for f in dietList ]

nutriList = [calors,chols,fats,sods,carbs,fibs,prots,vitas,vitcs,calcis,irons]

constraintNames = cols[3:].values.tolist()
constraintMin = df[65:66].values.tolist()
constraintMax = df[66:67].values.tolist()
mins = constraintMin[0][3:]
maxs = constraintMax[0][3:]

# print(constraintNames)
# print()
# print(mins)
print()

problem = LpProblem("Diet Problem", LpMinimize)

foodVariableList = []
for food in foods:
    var = LpVariable(food, 0)
    foodVariableList.append(var)

foodBinVariableList = []
for food in foods:
    var = LpVariable(food+"Bin", 0, 1, LpBinary)
    foodBinVariableList.append(var)


# creating the objective function
objFunct = 0
for index in range(len(foodVariableList)):
    objFunct += (foodVariableList[index] * prices[index])

problem += objFunct, "Total food costs"


# make constraints for nutrition
def makeConstraint(label, foodVarList, foodList, min, max):
    constraint = 0
    for index in range(len(foodList)):
        constraint += (foodVarList[index] * foodList[index])

    minConstraint = constraint >= min, label+" min constraint"
    maxConstraint = constraint <= max, label+" max constraint"
    return minConstraint, maxConstraint


for index in range(len(nutriList)):
    minCon, maxCon = makeConstraint(constraintNames[index], foodVariableList, nutriList[index], mins[index], maxs[index])
    problem += minCon
    problem += maxCon


for index in range(len(foodVariableList)):
    foodVar = foodVariableList[index]
    foodBin = foodBinVariableList[index]
    foodName = foods[index]
    problem += foodVar >= foodBin * 0.1, "Min amount const "+foodName
    problem += foodVar <= 100000 * foodBin

celBin = foodBinVariableList[2]
celVar = foodVariableList[2]

broBin = foodBinVariableList[0]
broVar = foodVariableList[0]

problem += celBin + broBin <= 1

# problem += celVar * celBin == celVar
# problem += broVar * broBin >= broVar

pork = foodBinVariableList[50]
egg1 = foodBinVariableList[28]
egg2 = foodBinVariableList[29]
turk = foodBinVariableList[30]
beef =  foodBinVariableList[31]
problem += pork + egg1 + egg2 +turk + beef >= 3


# print(problem)
problem.solve()

for var in problem.variables():
    print(var.name, var.varValue)



