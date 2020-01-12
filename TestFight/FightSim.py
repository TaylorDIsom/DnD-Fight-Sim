import random

class Character:
    name = "butt"
    health = 100
    attacks = {}



    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.health = 99
        self.initAttacks()


    def initAttacks(self):
        poke = Attack("poke", "4d4")
        self.attacks["poke"] = poke

    def attack(self):
        attack = random.choice( list(self.attacks) )
        return self.attacks.get(attack)



class Attack:

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


def rollDiceCommand(command):
    hasMod = "+" in command
    dIndex = command.index("d")
    numTimesToRoll = int( command[ : dIndex] )
    if hasMod:
        modIndex = command.index("+")
        dice = int( command[ dIndex + 1 : modIndex ] )
        modifier = int( command[modIndex + 1:] )
        # print("mod index")
        # print(modIndex)
        pass
    else:
        dice = int( command[dIndex + 1:] )
        modifier = 0
    # print(numTimesToRoll, dice, modifier)
    return rollDice(numTimesToRoll, dice, modifier)


def rollDice(numTimesToRoll, dice, modifier = 0):
    sum = 0
    for i in range(numTimesToRoll):
        die = random.randint(1,dice)
        sum += die
        # print(die)
    sum += modifier
    return sum

def calcAbilityMod(score):
    mod = (score - 10) // 2
    return mod

print()
print( calcAbilityMod(7) )
print()


p = Character("peeee", 7)
print(p.health, p.attack() )
print(p)
print()
print( rollDiceCommand("4d4+1"))
print()
print( rollDice(4,4) )

