# codenames: code to determine which words will have which colors

import random

words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "one0", "one1", "one2", "one3", "one4", "one5", "one6", "one7", "one8", "one9", "two0", "two1", "two2", "two3", "two4"]
colors = ["B", "Y", "W", "K"]
numOfColors = [9, 8, 7, 1]
print(words)
print(colors)

dupeWords = words.copy()
random.shuffle(dupeWords)


print()
print(dupeWords)

duplicateRandomWords = dupeWords.copy()
print(duplicateRandomWords)

def assignColorSpaces(spaceOptions, numAssignments):
    sample = random.sample(spaceOptions, numAssignments)
    return sample

def removeAssignmentsFromOptions(spaceOptions, assignedSpaces):
    for assignment in assignedSpaces:
        spaceOptions.remove(assignment)



assignmentDict = {}
colorAssignments = dupeWords.copy()

def updateColorAssignmentsFromSample(wordList, assignments, color):
    for assignment in assignments:
        index = wordList.index(assignment)
        # print(index, wordList, assignment)
        colorAssignments[index] = color


for color in colors:
    numOfColor = numOfColors[ colors.index(color) ]
    assignments = assignColorSpaces(duplicateRandomWords, numOfColor)
    assignmentDict[color] = assignments
    updateColorAssignmentsFromSample(dupeWords, assignments, color)
    if colors.index(color) < len(colors) - 1:
        removeAssignmentsFromOptions(duplicateRandomWords, assignments)

print(assignmentDict)
print(colorAssignments)

# //make color list

def updateRowColumn(numRows, numColumns, row, column):
    currentColumn = column % numColumns
    if currentColumn < numColumns - 1:
        return (row, column + 1)
    else:
        return (row + 1, 0)

def makeEmptyTable(numRows, numColumns):
    table = []
    for i in range(numRows):
        newRow = [0] * numColumns
        table.append(newRow)
    return table




def makeTable(numRows, numColumns):
    table = makeEmptyTable(numRows, numColumns)
    currentRow = 0
    currentColumn = 0
    for index in range(len(words)):
        word = dupeWords[index]
        color = colorAssignments[index]
        table[currentRow][currentColumn] = (word, color)
        nextRowColumn = updateRowColumn(numRows, numColumns, currentRow, currentColumn)
        currentRow = nextRowColumn[0]
        currentColumn = nextRowColumn[1]
    return table


print()
table = makeTable(5,5)
for row in table:
    print(row)

print()
print("poop")