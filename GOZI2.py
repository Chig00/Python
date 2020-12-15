"""GOZI 2 - Battle of the Warriors

This is a singleplayer game, where the player plays against the computer.

The player and computer summon 3 random warriors each and they command the
warriors to act in battle against each other.

The team that defeats the other wins.

"""

from random import randint, shuffle

global warrior_names

#all warriors in the game code
warrior_names = ["Norman", "Eric", "Lenna", "FiveStar", "Assa", "Kasime",
                 "Pyro", "Gura", "Nimbus", "Maria", "Raijin", "Axim",
                 "Rex", "Ninji"]

class Summoner:
    """Class for the player and computer's attributes."""

    score = 0

    def __init__(self, tag):
        """Give the summoner a tag for player or computer.

        All of the summoner's warriors will share the tag.
        
        The tag is used to identify whether the player will control the warrior
        or the computer will automatically control the warrior.

        """

        self.tag = tag

    def team_build(self, team):
        """Create the summoner's team.

        All warriors on the summoners team will share the summoner's tag.

        The team is then redefined as the objects rather than the string names.

        """

        #eval is used to get the Warrior subclass fromt the string
        self.w0 = eval(team[0])(self.tag)
        self.w1 = eval(team[1])(self.tag)
        self.w2 = eval(team[2])(self.tag)

        #the team is set as the warrior objects rather than the strings
        self.team = [self.w0, self.w1, self.w2]

class Warrior:
    """Base class for all common warrior attributes."""

    #all warriors start alive and uncharged
    alive = True
    charge = 0

    def __init__(self, tag):
        """Tag the warrior with the summoner's tag.

        The tag will ensure that the correct summoner controls the warrior.

        """

        self.tag = tag

    def turn(self, player, computer):
        """Choose a course of action for the warrior.

        If the warrior is tagged "p", then the player chooses the course of
        action and can additionally choose the check the warriors' stats.
        If the warrior is tagged "c", the the computer automatically chooses
        to attack or (if there is sufficient charge) use the special.

        """

        #defeated warriors can no longer battle
        if self.alive == False: return
        
        #indicates the warrior having a turn
        print("It is ", self.name, "'s turn!", sep = "")
        
        if self.tag == "p":
            #loop used to get correct input and to ensure an attack or special
            #is performed by the warrior
            while True:
                #input is used for player-summoned warriors
                print("Choose a move for ", self.name, "!", sep = "")
                if self.charge >= self.cost: print("Your special is ready!")
                choice = input("Attack (a), special (s), or check stats (c)? ")

                if choice == "a":
                    if self.attack(player, computer):
                        break

                elif choice == "s":
                    if self.special(player, computer):
                        break

                elif choice == "c": all_stats(player, computer)

                else: print("Sorry, I didn't understand that.")

        else:
            #chooses the warrior with the lowest health to be the target
            opponents = sorted(player.team, key = lambda w: w.power, reverse = True)
            opponents.sort(key = lambda w: w.health)
            
            target = self.target_set(opponents)

            if self.charge >= self.cost:
                if self.special_save(target):
                    self.attack(player, computer, target)
                else:
                    self.special(player, computer, target)
            else: self.attack(player, computer, target)

    def attack(self, player, computer, target = None):
        """Attack an opponent.

        The computer will automatically attack a predetermined target.
        The player will choose their target within the function via input().

        """

        if self.tag == "p":
            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                #target is set here for code shortening
                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        #the damage dealt is determined randomly after target determination
        damage = int(self.power * randint(80, 120) / 100)

        #an attack will deal damage and charge the giver and taker
        target.health -= damage
        target.charge += 1
        self.charge += 1

        print(self.name, "used", self.attack_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

    def special_check(self):
        """Check if the warrior has enough charge to perform a special."""

        if self.charge < self.cost:
            print("You don't have enough charge to perform your special.")
            return True

    def stats(self):
        """Print the warrior's full stats."""

        print(self.name,
              "\n" + self.desc,
              
              "\n\nHealth:", self.health,
              "\nCharge:", self.charge,
              "\nPower:", self.power,
              "\nSpeed:", self.speed,
              
              "\n\nAttack:", self.attack_name,
              "\nSpecial:", self.special_name,
              "\nDescription:", self.special_desc,
              "\nCost:", self.cost)

    def special_save(self, target):
        """Check if the computer should save its special.

        If a computer controlled warrior has enough charge to use their
        special, but the special would be wasted in doing so,
        the special is 'saved' and a regular attack is used instead.

        Warriors that will save their special are the ones that their special
        simply boosts their damage output and nothing else.

        Warriors that deal splash damage will be unaffected as they
        have multiple targets.

        Warriors that have a utility effect will be unaffected, as the utility
        will still be beneficial

        """

        if target.health <= self.power * 0.8 and self.special_type == "attack":
            return True

    def target_set(self, opponents):
        """Choose a target for the computer.

        The target will chosen using an algorithm.

        If one of the opponents is pre-ascension Eizo, that opponent will be
        targetted above all others

        The target with the lowest health will be attacked usually.
        If there is a health tie, then the opponent with the greater power
        is prioritised.

        """

        for warrior in opponents:
            if warrior.alive == True:
                return warrior

class Norman(Warrior):
    """Warrior subclass for Norman's specific attributes."""

    name = "Norman"
    desc = "Skilled Swordsman"

    health = 1000
    power = 100
    speed = 100
    cost = 3

    attack_name = "Sword Slash"
    special_name = "Blade Blitz"
    special_desc = ("Norman rushes to the opponent and slashes at them"
                    " relentlessly with triple his usual power!")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(3 * self.power * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

class Eric(Warrior):
    """Warrior subclass for Eric's specific attributes."""

    name = "Eric"
    desc = "Radiant Hero"

    health = 1200
    power = 140
    speed = 70
    cost = 5

    attack_name = "Ragnell"
    special_name = "Aether"
    special_desc = ("Eric imbues his blade with power to attack with double"
                    " power and heal himself of half the damage dealt!")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(2 * self.power * randint(80, 120) / 100)
        if target.health - damage < 0: heal = int(target.health / 2)
        else: heal = int(damage / 2)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")
        print(self.name, "healed", heal, "health!")

        return True

class Lenna(Warrior):
    """Warrior subclass for Lenna's specific attributes."""

    name = "Lenna"
    desc = "Lady of the Cosmos"

    health = 950
    power = 110
    speed = 110
    cost = 5

    attack_name = "Cosmic Blade"
    special_name = "Astral Blade"
    special_desc = ("Lenna uses her powers over the cosmos to boost her power"
                    " fivefold!")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(5 * self.power * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

class FiveStar(Warrior):
    """Warrior subclass for FiveStar's specific attributes."""

    name = "FiveStar"
    desc = "Lord of the Stars"

    health = 800
    power = 120
    speed = 120
    cost = 4

    attack_name = "Star Slice"
    special_name = "Star Storm"
    special_desc = ("FiveStar summons massive stars from the skies to attack"
                    " all of his opponents with 50% extra power!")
    
    special_type = "splash"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                choice = input("Perform your special? (y/n) ")

                if choice == "y": break
                elif choice == "n": return
                else: print("Please choose a living warrior to attack.")

        damage0 = int(1.5 * self.power * randint(80, 120) / 100)
        damage1 = int(1.5 * self.power * randint(80, 120) / 100)
        damage2 = int(1.5 * self.power * randint(80, 120) / 100)

        self.charge -= self.cost

        if self.tag == "p": summoner = computer
        else: summoner = player

        damage_no = 0

        #all warriors on the opposing team are attacked
        for warrior in summoner.team:
            if warrior.alive == True:
                damage = eval("damage" + str(damage_no))
                warrior.health -= damage
                warrior.charge += 1
                print(self.name, "used", self.special_name, "on", warrior.name,
                      "and dealt", damage, "damage!")
            damage_no += 1

        return True
        
class Assa(Warrior):
    """Warrior subclass for Assa's specific attributes."""

    name = "Assa"
    desc = "Master Assassin"

    health = 750
    power = 75
    speed = 150
    cost = 1

    attack_name = "Needler"
    special_name = "Poison Needles"
    special_desc = ("Assa dips her needles into a special poison that"
                    " increases her power by 20% of the opponent's"
                    " health.")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int((self.power + target.health * 0.2) * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

class Pyro(Warrior):
    """Warrior subclass for Pyro's specific attributes."""

    name = "Pyro"
    desc = "Blazing Warrior"

    health = 1000
    power = 150
    speed = 50
    cost = 5

    attack_name = "Flamethrower"
    special_name = "Inferno"
    special_desc = ("Pyro uses his flames to torch all of the opponents"
                    " with 50% extra power!")
    
    special_type = "splash"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            while True:
                choice = input("Perform your special? (y/n) ")

                if choice == "y": break
                elif choice == "n": return
                else: print("Please choose a living warrior to attack.")

        damage0 = int(1.5 * self.power * randint(80, 120) / 100)
        damage1 = int(1.5 * self.power * randint(80, 120) / 100)
        damage2 = int(1.5 * self.power * randint(80, 120) / 100)

        self.charge -= self.cost

        if self.tag == "p": summoner = computer
        else: summoner = player

        damage_no = 0

        for warrior in summoner.team:
            if warrior.alive == True:
                damage = eval("damage" + str(damage_no))
                warrior.health -= damage
                warrior.charge += 1
                print(self.name, "used", self.special_name, "on", warrior.name,
                      "and dealt", damage, "damage!")
            damage_no += 1

        return True

class Gura(Warrior):
    """Warrior subclass for Gura's specific attributes."""

    name = "Gura"
    desc = "Hammer Knight"

    health = 1500
    power = 125
    speed = 25
    cost = 3

    attack_name = "Hammer Smash"
    special_name = "Hammer Quake"
    special_desc = ("Gura uses her massive hammer and smashes the ground with"
                    " force! The opponent is attacked with double power!")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(2 * self.power * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

class Nimbus(Warrior):
    """Warrior subclass for Nimbus' specific attributes."""

    name = "Nimbus"
    desc = "Warrior of the Storm"

    health = 600
    power = 150
    speed = 150
    cost = 2

    attack_name = "Gale Force"
    special_name = "Hurricane"
    special_desc = ("Nimbus summons a massive hurricane to attack all of"
                    " his opponents with full power!")
    
    special_type = "splash"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            while True:
                choice = input("Perform your special? (y/n) ")

                if choice == "y": break
                elif choice == "n": return
                else: print("Please choose a living warrior to attack.")

        damage0 = int(self.power * randint(80, 120) / 100)
        damage1 = int(self.power * randint(80, 120) / 100)
        damage2 = int(self.power * randint(80, 120) / 100)

        self.charge -= self.cost

        if self.tag == "p": summoner = computer
        else: summoner = player

        damage_no = 0

        for warrior in summoner.team:
            if warrior.alive == True:
                damage = eval("damage" + str(damage_no))
                warrior.health -= damage
                warrior.charge += 1
                print(self.name, "used", self.special_name, "on", warrior.name,
                      "and dealt", damage, "damage!")
            damage_no += 1

        return True

class Maria(Warrior):
    """Warrior subclass for Maria's specific attributes."""

    name = "Maria"
    desc = "Fire Mage"

    health = 600
    power = 200
    speed = 80
    cost = 3

    attack_name = "Bolganone"
    special_name = "Immolate"
    special_desc = ("Maria focuses her flames into a powerful beam and takes"
                    " aim at the opponents heart! The attack has 150% extra"
                    " power!")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(2.5 * self.power * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

class Raijin(Warrior):
    """Warrior subclass for Raijin's specific attributes."""

    name = "Raijin"
    desc = "Lightning Warrior"

    health = 500
    power = 175
    speed = 175
    cost = 3

    attack_name = "Thunder's Fist"
    special_name = "Lightning Chain Combo"
    special_desc = ("Raijin charges up his body with electricity and attacks"
                    " the opponent with 2.5x power in a combo over in a"
                    " flash!")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(2.5 * self.power * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage0
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True
        
class Axim(Warrior):
    """Warrior subclass for Axim's specific attributes."""

    name = "Axim"
    desc = "Shadow Knight"

    health = 1300
    power = 130
    speed = 13
    cost = 3

    attack_name = "Alondite"
    special_name = "New Moon"
    special_desc = ("Axim uses the power of darkness to deplete the opponent's"
                    " health! The power of this attack is boosted by 30% of"
                    " the opponent's health.")
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int((self.power + target.health * 0.3) * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

class Rex(Warrior):
    """Warrior subclass for Rex's specific attributes."""

    name = "Rex"
    desc = "King of the Realm"

    health = 1400
    power = 100
    speed = 20
    cost = 4

    attack_name = "Royal Blade"
    special_name = "Shielded Strike"
    special_desc = ("Rex uses his shield to protect himself and his allies"
                    " during his attack! All warriors on Rex's team have their"
                    " health boosted with half of Rex's power, while Rex"
                    " attacks with full power!")
    
    special_type = "attack/utility"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(self.power * randint(80, 120) / 100)
        shield1 = int(0.5 * self.power * randint(80, 120) / 100)
        shield2 = int(0.5 * self.power * randint(80, 120) / 100)
        shield3 = int(0.5 * self.power * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        if self.tag == "p": summoner = player
        else: summoner = computer

        shield_no = 0

        for warrior in summoner.team:
            if warrior.alive == True:
                shield = eval("shield" + str(shield_no))
                warrior.health += shield
                warrior.charge += 1
                print(self.name, "used", self.special_name, "on", warrior.name,
                      "and shielded", shield, "health!")
            shield_no += 1

        return True

class Ninji(Warrior):
    """Warrior subclass for Ninji's specific attributes."""

    name = "Ninji"
    desc = "Sneaky Ninja"

    health = 900
    power = 100
    speed = 200
    cost = 3

    attack_name = "Shuriken"
    special_name = "Katana"
    special_desc = "Ninji draws his katana and slashes with 150% extra power!"
    
    special_type = "attack"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            #loop for useable input
            while True:
                print("Attack", computer.w0.name, "(1),", computer.w1.name,
                      "(2),", computer.w2.name, "(3), or cancel (c)? ",
                      end = "")
                choice = input()

                if choice == "1" and computer.w0.alive == True:
                    target = computer.w0
                elif choice == "2" and computer.w1.alive == True:
                    target = computer.w1
                elif choice == "3" and computer.w2.alive == True:
                    target = computer.w2

                elif choice == "c": return

                else: print("Please choose a living warrior to attack.")

                if target: break

        damage = int(2.5 * self.power * randint(80, 120) / 100)

        #the special will drain the user's charge instead of charging it
        target.health -= damage
        target.charge += 1
        self.charge -= self.cost

        print(self.name, "used", self.special_name, "on", target.name,
              "and dealt", damage, "damage!")

        return True

class Kasime(Warrior):
    """Warrior subclass for Kasime's specific attributes."""

    name = "Kasime"
    desc = "Psychic Power"

    health = 1200
    power = 80
    speed = 40
    cost = 2

    attack_name = "Mind Pulse"
    special_name = "Chaos Control"
    special_desc = ("Kasime uses his psychic powers to force all of the"
                    " opponents to attack themselves with their own power!")
    
    special_type = "splash"

    def special(self, player, computer, target = None):
        """Perform the warrior's special."""

        if self.special_check():
            return

        if self.tag == "p":
            print(self.special_name,
                  "\n" + self.special_desc)

            while True:
                choice = input("Perform your special? (y/n) ")

                if choice == "y": break
                elif choice == "n": return
                else: print("Please choose a living warrior to attack.")

        self.charge -= self.cost

        if self.tag == "p": summoner = computer
        else: summoner = player

        for warrior in summoner.team:
            if warrior.alive == True:
                damage = int(warrior.power * randint(80, 120) /100)
                warrior.health -= damage
                warrior.charge += 1
                print(self.name, "used", self.special_name, "on", warrior.name,
                      "and dealt", damage, "damage!")

        return True

def summon(available_warriors):
    """Summon 6 warriors at random from the list of available warriors."""

    #the warriors to be used in the round are picked from the available
    #warriors and those warriors are deleted from the available warriors with
    #the use of the pop() method
    warriors = []

    while len(warriors) < 6:
        warriors.append(available_warriors.pop())

    return warriors, available_warriors

def order_set(warriors):
    """Return a list of warriors is decending speed order."""

    #warriors are shuffled to break speed ties fairly
    shuffle(warriors)

    #warriors are sorted by the sort() method
    warriors.sort(key = lambda w: w.speed, reverse =  True)

    return warriors

def defeat_check(warriors):
    """Check if a warriors had recently been defeated.

    If a warrior had recently been defeated, then its alive attribute becomes
    False and the defeat is announced.

    """

    for warrior in warriors:
        if warrior.health <= 0 and warrior.alive == True:
            warrior.health = 0
            warrior.charge = 0
            warrior.alive = False
            print(warrior.name, "has been defeated!")

def end_check(player, computer):
    """Check if a team has been defeated.

    If a team has been defeated, the 'end phase' begins.

    """

    #counts to 2 summoners
    count = 0

    while count < 2:
        #counts up to 3 defeats for a single team before returning True
        defeats = 0

        #checks for the player first, then the computer
        if count == 0: summoner = player
        else: summoner = computer
        
        for warrior in summoner.team:
            if warrior.alive == False:
                defeats += 1

        if defeats == 3:
            return True

        count += 1

def all_stats(player, computer):
    """Display all of the warriors' stats.

    If it is desired, a warrior's stats may be viewed in more depth by
    inputting the warriors number.

    """

    #all basic stats are displayed
    print(player.w0.name,
          "\nHealth:", player.w0.health,
          "\nCharge:", player.w0.charge,
          "\n\n" + player.w1.name,
          "\nHealth:", player.w1.health,
          "\nCharge:", player.w1.charge,
          "\n\n" + player.w2.name,
          "\nHealth:", player.w2.health,
          "\nCharge:", player.w2.charge,
          "\n\n" + computer.w0.name,
          "\nHealth:", computer.w0.health,
          "\nCharge:", computer.w0.charge,
          "\n\n" + computer.w1.name,
          "\nHealth:", computer.w1.health,
          "\nCharge:", computer.w1.charge,
          "\n\n" + computer.w2.name,
          "\nHealth:", computer.w2.health,
          "\nCharge:", computer.w2.charge)

    while True:
        print("View", player.w0.name, "(1),", player.w1.name, "(2),",
              player.w2.name, "(3),", computer.w0.name, "(4),",
              computer.w1.name, "(5),", computer.w2.name, "(6),"
              " or cancel (c)? ", end = "")
        choice = input()

        if choice == "1": player.w0.stats()
        elif choice == "2": player.w1.stats()
        elif choice == "3": player.w2.stats()
        elif choice == "4": computer.w0.stats()
        elif choice == "5": computer.w1.stats()
        elif choice == "6": computer.w2.stats()

        elif choice == "c": return

        else: print("Sorry, I didn't understand that.")

def win_check(player, computer):
    """Check who won the game."""

    #counts to 2 summoners
    count = 0
    points = []

    while count < 2:
        #counts the survivors
        survivors = 0

        #checks for the player first, then the computer
        if count == 0: summoner = player
        else: summoner = computer
        
        for warrior in summoner.team:
            if warrior.alive == True:
                survivors += 1

        points.append(survivors)

        count += 1

    return points

def main():
    """Start a new game of GOZI 2."""

    player = Summoner("p")
    computer = Summoner("c")

    #the available warriors will be filled in the main loop
    available_warriors = []

    #main loop
    while True:
        #a depleted list of available warriors will refresh the list
        #the warriors are shuffled in advance for game speed
        if len(available_warriors) < 6: available_warriors = warrior_names[:]
        shuffle(available_warriors)

        #6 warriors are picked for battle
        warriors = summon(available_warriors)

        #the remaining available warriors are stored
        available_warriors = warriors[1]

        #the warriors list is redefined for readability
        warriors = warriors[0]

        #the warriors for the player and computer are announced
        print("You summoned ", warriors[0], ", ", warriors[1],
              ", and ", warriors[2], "!"
              
              "\nThe computer summoned ", warriors[3], ", ", warriors[4],
              ", and ", warriors[5], "!",
              
              sep = "")

        #warriors are assigned to the player and computer
        player.team_build([warriors[0], warriors[1], warriors[2]])
        computer.team_build([warriors[3], warriors[4], warriors[5]])

        #the warriors list is redefined again to use the warrior objects
        warriors = [player.w0, player.w1, player.w2,
                    computer.w0, computer.w1, computer.w2]

        #end varaible set to False until the end of a battle
        end = False

        while True:
            #the order is determined by the order of warriors
            #the order is set by order_set()
            warriors = order_set(warriors)

            for warrior in warriors:
                warrior.turn(player, computer)
                defeat_check(warriors)
                if end_check(player, computer):
                    end = True
                    break

            if end:
                break

        #end phase
        points = win_check(player, computer)

        #only the winner gets points
        if points[0]:
            print("You win!"
                  "\nYou got", points[0], "points!")

        else:
            print("You lose..."
                  "\nThe computer got", points[1], "points...")

        #scores are added up
        player.score += points[0]
        computer.score += points[1]

        #scores are displayed
        print("Player:", player.score,
              "\nComputer:", computer.score)

        #the game starts over again (loop)

if __name__ == "__main__": main()
