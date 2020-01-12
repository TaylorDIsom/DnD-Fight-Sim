import random
from operator import attrgetter

#TODO: implement movement later

class Character:
    attacks = {}



    def __init__(self, name, level=1, health=24, str=10, dex=10, con=10, int=10, wis=10, char=10, armor=10, speed=30):
        self.name = name
        self.level = level
        self.health = health
        self.currentHealth = health
        self.strength = str
        self.dexterity = dex
        self.constitution = con
        self.intelligence = int
        self.wisdom = wis
        self.charisma = char
        self.armor = armor
        self.speed = speed
        self.initiative = 0
        self.initAttacks()

    def __str__(self):
        return ""+self.name + " (hp:" + str(self.currentHealth) + ")"

    def initAttacks(self):
        poke = Attack("poke", "4d4")
        self.attacks["poke"] = poke

    def attack(self):
        attack = random.choice( list(self.attacks) )
        return self.attacks.get(attack)

    def attackTarget(self, target):
        chosenAttack = self.attack()
        damageDice = chosenAttack.damage
        damage = rollDiceCommand(damageDice)
        target.currentHealth -= damage
        return damage

    def rollInitiative(self):
        self.initiative = rollDice(1, 20, calcAbilityMod( self.dexterity ) )
        print(self.initiative, "init")


class Attack:

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

    def __str__(self):
        return ""+self.name + ": " + self.damage


class Fight:
    initiativeOrder = []
    charTurn = None
    roundNumber = 1
    isTeam1Alive = True
    isTeam2Alive = True
    results = None


    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.setInitiativeOrder()

    def rollInitiative(self, characters):
        for character in characters:
            character.rollInitiative()

    def setInitiativeOrder(self):
        characters = self.team1 + self.team2
        self.rollInitiative(characters)
        self.initiativeOrder = sorted(characters, key=attrgetter('initiative'))
        self.initiativeOrder.reverse()

    def updateTeamStatus(self):
        self.isTeam1Alive = False
        self.isTeam2Alive = False
        for character in self.team1:
            if character.currentHealth > 0:
                self.isTeam1Alive = True
                break
        if not self.isTeam1Alive:
            self.results = "Team 2 Wins"
            return
        for character in self.team2:
            if character.currentHealth > 0:
                self.isTeam2Alive = True
                break
        if not self.isTeam2Alive:
            self.results = "Team 1 Wins"

    def getFoe(self, character):
        if character in self.team1:
            return random.choice(self.team2)
        else:
            return random.choice(self.team1)

    def fight(self):
        while (self.isTeam1Alive and self.isTeam2Alive):
            print("___________BEGINNING ROUND", self.roundNumber, "___________")
            for character in self.initiativeOrder:
                if (character.currentHealth > 0):
                    foe = self.getFoe(character)
                    damage = character.attackTarget(foe)
                    print(character, "dealt", damage, "to", foe)
            self.roundNumber += 1
            print()
            self.updateTeamStatus()
        print(self.results)


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

def printDict(dict):
    for key, value in dict.items():
        print(key, value)


print()
print( calcAbilityMod(7) )
print()


p = Character("fighter1")
p2 = Character("fighter2")
print(p, p.health, p.attack() )
( printDict( p.attacks) )
print()
print( rollDiceCommand("4d4+1"))
print()
print( rollDice(4,4) )


t1 = [p]
t2 = [p2]
fight = Fight(t1, t2)
# p.currentHealth = 0
fight.updateTeamStatus()
print(fight.isTeam1Alive, fight.isTeam2Alive, fight.initiativeOrder)
print()
for char in fight.initiativeOrder:
    print(char)

print()
fight.fight()
print()

