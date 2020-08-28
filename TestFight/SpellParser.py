# Parsing a D&D 3.5e spell list
fileLines = []

spellDict = {}

file = open("spells.xml")

spellList = file.readlines()
numLines = len(spellList)

# TODO catch tag not found
def parseXML(line, tag):

    endOfOpeningTag = line.index(">")
    #print(">>>", tag)
    info = None
    try:
        beginningOfClosingTag = line.index("</" + tag)
        info = line[endOfOpeningTag + 1 : beginningOfClosingTag]
    except ValueError:
        pass
    #print(info)
    return info


def printDict():
    newFile = open("test file.csv", "w")
    newFile.write("poop")
    newFile.close()

print("1st poop")

printDict()

# print()

index = 2

parseXML(spellList[2], "name")


while index < 3:    # numSpell
    #print( ">>>>>>>>>", index)
    name = parseXML( spellList[ index ], "name")
    if name is not None: index += 1

    school = parseXML( spellList[ index ], "school")
    if school is not None: index += 1

    level = parseXML( spellList[ index ], "level")
    if level is not None: index += 1

    components = parseXML( spellList[ index ], "components")
    if components is not None: index += 1

    castingtime = parseXML( spellList[ index ], "castingtime")
    if castingtime is not None: index += 1

    spellRange = parseXML( spellList[ index ], "range")
    if spellRange is not None: index += 1

    effect = parseXML( spellList[ index ], "effect")
    if effect is not None: index += 1

    duration = parseXML( spellList[ index ], "duration")
    if duration is not None: index += 1

    save = parseXML( spellList[ index ], "save")
    if save is not None: index += 1

    sr = parseXML( spellList[ index ], "sr")
    if sr is not None: index += 1

    description = parseXML( spellList[ index ], "description")
    if description is not None: index += 1

    shortdescription = parseXML( spellList[ index ], "shortdescription")
    if shortdescription is not None: index += 1

    index += 2

    spellDict[name] = {
        "school" : school,
        "level" : level,
        "components" : components,
        "castingtime" : castingtime,
        "spellRange" : spellRange,
        "effect" : effect,
        "duration" : duration,
        "effect" : effect,
        "duration" : duration,
        "save" : save,
        "sr" : sr,
        "description" : description,
        "shortdescription" : shortdescription
    }

    #print(index)

print()
print(spellDict)
print()

print("last poop")

file.close()


def parseSpell():
    pass

def findSpellLastLine(spellName):
    pass

