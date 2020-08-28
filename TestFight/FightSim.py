import random
import math
from operator import attrgetter

#TODO: implement movement later

class Character:



    def __init__(self, name, level=1, health=24, str=10, dex=10, con=10, int=10, wis=10, char=10, armor=10, speed=30):
        self.name = name
        self.level = level
        self.health = health
        self.currentHealth = health
        self.isConscious = True
        self.proficiency = 2
        self.strength = str
        self.dexterity = dex
        self.constitution = con
        self.intelligence = int
        self.wisdom = wis
        self.charisma = char
        self.armor = armor
        self.speed = speed
        self.initiative = 0
        self.attacks = {}
        self.initAttacks()
        self.damageDished = 0

    def __str__(self):
        return ""+self.name + " (hp:" + str(self.currentHealth) + ")"

    def initAttacks(self):
        damageMod = str(calcAbilityMod(self.strength))
        unarmed = Attack("unarmed", damage="1d4+"+ damageMod)
        self.attacks["unarmed"] = unarmed

    def getStrongestAttack(self):
        strongestAttack = self.attacks["unarmed"]
        mostDamage = calculateExpectedRollTotal(strongestAttack.damage)
        #print(strongestAttack)
        for attackName, attackDetails in self.attacks.items():
            attDmg = calculateExpectedRollTotal(attackDetails.damage)
            if attDmg > mostDamage:
                strongestAttack = attackDetails
                mostDamage = attDmg
        return strongestAttack

    def attack(self):
        #attack = random.choice( list(self.attacks) )
        strongAttack = self.getStrongestAttack()

        return strongAttack

    def doesAttatckHitTarget(self, target, attack):
        attackRollNatural = random.randint(1,20)
        #TODO
        #attackAbility = attack.ability
        #attackAbilityScore = self.attackAbility
        attackAbilityMod = 2 #calcAbilityMod(attackAbilityScore)
        proficiencyBonus = self.proficiency
        attackRollDirty = attackRollNatural + attackAbilityMod + proficiencyBonus
        if attackRollNatural == 20:
            return "critical hit"
        targetArmor = target.armor
        if attackRollDirty >= targetArmor:
            return "hit"
        return "miss"

    def attackTarget(self, target):
        chosenAttack = self.attack()
        attackResult = self.doesAttatckHitTarget(target, chosenAttack)
        if attackResult == "miss": #TODO May need to edit to add
            return 0, "none"
        isCrit = attackResult=="critical hit"
        damageDice = chosenAttack.damage
        damage = rollDiceCommand(damageDice, isCrit)
        target.currentHealth -= damage
        if target.currentHealth < 1:
            target.isConscious = False
        self.damageDished += damage
        return damage, chosenAttack.damageType

    def rollInitiative(self):
        self.initiative = rollDice(1, 20, calcAbilityMod( self.dexterity ) )


class Attack:

    def __init__(self, name, ability = "strength", damage = "1d4", damageType = "bludgeoning"):
        self.name = name
        self.ability = ability
        self.damage = damage
        self.damageType = damageType

    def __str__(self):
        return ""+self.name + ": " + self.damage +" "+ self.damageType


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
        self.team1Alive = team1.copy()
        self.team2Alive = team2.copy()
        self.setInitiativeOrder()

    def rollInitiative(self, characters):
        for character in characters:
            character.rollInitiative()

    def setInitiativeOrder(self):
        characters = self.team1 + self.team2
        self.rollInitiative(characters)
        self.initiativeOrder = sorted(characters, key=attrgetter('initiative'))
        self.initiativeOrder.reverse()

    def teamStatusRoundUpdate(self):
        self.isTeam1Alive = False
        self.isTeam2Alive = False
        for character in self.team1Alive:
            if character.isConscious:
                self.isTeam1Alive = True
                break
            else:
                self.team1Alive.remove(character)
                if character in self.initiativeOrder:
                    self.initiativeOrder.remove(character)
        if not self.isTeam1Alive:
            self.results = "Team 2 Wins"
            return
        for character in self.team2Alive:
            if character.isConscious:
                self.isTeam2Alive = True
                break
            else:
                self.team2Alive.remove(character)
                if character in self.initiativeOrder:
                    self.initiativeOrder.remove(character)
        if not self.isTeam2Alive:
            self.results = "Team 1 Wins"
        for character in self.initiativeOrder:
            if not character.isConscious:
                self.initiativeOrder.remove(character)


    def getFoe(self, character):
        if character in self.team1Alive:
            return random.choice(self.team2Alive)
        else:
            return random.choice(self.team1Alive)


    def initiate(self):
        while (self.isTeam1Alive and self.isTeam2Alive):
            print("___________BEGINNING ROUND", self.roundNumber, "___________")
            #for char in self.initiativeOrder:
            #    print(char, end=", ")
            #print()
            for character in self.initiativeOrder:
                if (character.currentHealth > 0):
                    foe = self.getFoe(character)
                    damageAndType = character.attackTarget(foe)
                    damage = damageAndType[0]
                    damageType = damageAndType[1]
                    if damage > 0:
                        if foe.currentHealth > 0:
                            print(character, "dealt", damage, damageType, "to", foe)
                        else:
                            #print()
                            #self.initiativeOrder.remove(foe)
                            #print(len(self.initiativeOrder), "init order")
                            if foe in self.team1Alive:
                                self.team1Alive.remove(foe)
                            else:
                                self.team2Alive.remove(foe)
                            foe.isConscious = False
                            print(character, "Killed (", damage, damageType, ")", foe)
                    else:
                        print(character, "missed", foe)
                else:
                    print(character, "is dead-zo, as of this round")

                if len(self.team1Alive) == 0 or len(self.team2Alive) == 0:
                    break
            self.roundNumber += 1
            self.teamStatusRoundUpdate()
            #print(len(self.team1Alive), "\t", len(self.team2Alive))
            print()
        print(self.results)


def rollDiceCommand(command, isCrit = False):
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
    return rollDice(numTimesToRoll, dice, modifier, isCrit)

def rollDice(numTimesToRoll, dice, modifier = 0, isCrit = False):
    sum = 0
    for i in range(numTimesToRoll):
        die = random.randint(1,dice)
        sum += die
        # print(die)
    if isCrit:
        sum += sum
        print("CRITICAL HIT!!!")
    sum += modifier
    return sum

def calculateExpectedRollTotal(command):
    hasMod = "+" in command
    dIndex = command.index("d")
    numTimesToRoll = int( command[ : dIndex] )
    if hasMod:
        modIndex = command.index("+")
        dice = int( command[ dIndex + 1 : modIndex ] )
        modifier = int( command[modIndex + 1:] )
        pass
    else:
        dice = int( command[dIndex + 1:] )
        modifier = 0
    sum = 0
    for i in range(1, dice + 1):
        sum += i
    average = sum / dice
    expectedTotal = average * numTimesToRoll + modifier
    return math.ceil(expectedTotal)


def calcAbilityMod(score):
    mod = (score - 10) // 2
    return mod

def printDict(dict):
    for key, value in dict.items():
        print(key, value)

print()


zuko = Character("zuko", 3, 30, 12, 15,13,12,13,8, 13)
nessa = Character("nessa", 3, 35, 14, 8, 14, 10,15,13, 18)
lexi = Character("lexi", 3, 30, 12, 14, 14, 10, 14, 13, 14)
kirby = Character("kirby", 3, 29, 8,16,12,15,10,14, 15)

shortSword = Attack("Sword Slash", damage="1d6+3")
zuko.attacks["Short Sword"] = shortSword
nessa.attacks["war hammer"] = shortSword
lexi.attacks["Short Sword"] = shortSword
kirby.attacks["rapier"] = shortSword


print()


p1 = Character("fighter1")
p2 = Character("fighter2")
p3 = Character("fighter3")
p4 = Character("fighter4")

pen = Character("pen", 1,33,14,11,13,18,14,12,16)
penPoss = Character("pen possessed", 1,30,14,13,12,18,14,12,16)
constr1 = Character("con1", 1,30,18,11,14,6,8,5,16)
constr2 = Character("con2", 1,30,18,11,14,6,8,5,16)
constr3 = Character("con3", 1,30,18,11,14,6,8,5,16)

# print(p, p.health, p.attack() )
# ( printDict( p.attacks) )
# print()
# print( rollDiceCommand("4d4+1"))
# print()
# print( rollDice(4,4) )


t1 = [zuko, nessa, lexi, kirby]

t2 = [constr1, constr2, constr3, pen, penPoss]

fight = Fight(t1, t2)
# p.currentHealth = 0
# fight.updateTeamStatus()
# print(fight.isTeam1Alive, fight.isTeam2Alive, fight.initiativeOrder)
print("Initiative Order")
for char in fight.initiativeOrder:
    print(char)

print()
#fight.initiate()
print()

#for char in (t1 + t2):
#    print(char, char.damageDished)

letters = ['b','r','n','m','g','s','t','d','c ','h']
print(sorted(letters))

"""
mirror
string
stitch



"""