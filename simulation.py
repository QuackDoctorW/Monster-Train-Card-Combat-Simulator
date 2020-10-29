
class Creature:
    def __init__(self, cname = "abc", ismons = True, att = 0, hp = 0, arm = 0, sts =  None):
        self.name = cname
        self.damage = att
        self.health = hp
        self.maxhealth = hp
        self.armor = arm
        self.isMonster = ismons
        self.state = _Status() if sts == None else sts
        
    def modify_stacks(self, stacktype, chgvalue):
        self.state.modify_status(stacktype, chgvalue)
        
    def modify_decay(self, stacktype, newvalue):
        self.state.reset_decay(stacktype, newvalue)
    
    def get_stacks(self,stacktype):
        return self.state.status_dict[stacktype][0]
        
    def __repr__(self):
        return "%s (%s,%s+%s) %s" % (self.name, self.damage, self.health, self.armor, self.state)
    
class _Status:
    def __init__(self):
        self.status_dict = {'mstrike':[0,0], "daze": [0,1], "rage":[0,1], "relentless": [0,0], "sweep": [0,0], \
                            "spike": [0,0], "quick": [0,0], "sap": [0,1], "regen": [0,1] } #type: [currentstack,decay]
        
    def modify_status(self, statustype, chgvalue): 
        self.status_dict[statustype][0] += chgvalue
        
    def reset_decay(self, statustype, newvalue):
        self.status_dict[statustype][1] = newvalue
    
    def __repr__(self):
        return str({a:b[0] for a,b in self.status_dict.items() if b[0] != 0})

class Floor:
    def __init__ (self): #in order from front to back
        self.monsters = []
        self.angels = []
         
    def addcreature(self,creature:Creature):
        if creature.isMonster:
            self.monsters.append(creature)
        else:
            self.angels.append(creature)
    
    def battle(self):
        print("battle begins", self)
        #la lapinchatte a mangé Brendan Angles, uwu~
        for monster in self.monsters[::]: #quick monsters
            if monster.get_stacks("quick") > 0:
                for _ in range(self._attack_times(monster)):
                    if monster.health <= 0:
                        break 
                    self.attack(monster, self.angels)
        for angel in self.angels[::]:   #in attack, angel may be deleted when looping angels, so copying the list             
            for _ in range(self._attack_times(angel)):
                if angel.health <= 0: #sometimes it is died before making all attacks from passive damage
                    break
                self.attack(angel,self.monsters)
        for monster in self.monsters[::]: #same as above
            if monster.get_stacks("quick") == 0:
                for _ in range(self._attack_times(monster)):
                    if monster.health <= 0:
                        break 
                    self.attack(monster, self.angels)
        #after battle results
        self.eob_calc()
        #fight again for relentless
        print("aww, it's over", self)
        if self.monsters:
            for angel in self.angels:
                if angel.get_stacks("relentless") == 1:
                        print("they fight again!!!")
                        self.battle()

    def _attack_times(self, attacker):
        times = 1+attacker.get_stacks('mstrike') 
        if attacker.get_stacks("daze")!= 0: 
            print(attacker, "is dazed!")
            return 0
        else:
            return times
        
    def attack(self, attacker, enemylist):
        if enemylist == []: #see if there are enemies to attack
            print(attacker, " attacked no one, all died :(")
            return None
        damage = attacker.damage + attacker.get_stacks("rage")*2 - attacker.get_stacks("sap")*2 #see if attacker will attack
        if damage <= 0:
            return None
        if attacker.get_stacks("sweep") == 1: #select list of single enemy/enemies due to sweep
            enemies_to_fight = enemylist
        else:
            enemies_to_fight = enemylist[:1]     
        for enemy in enemies_to_fight: #fight each enemy
            self._after_damage_healtharmor(damage, enemy)
            print(attacker, " attacked ", enemy)
            if enemy.get_stacks("spike") > 0: #recalc health for self for spike
                self._after_damage_healtharmor(enemy.get_stacks("spike"), attacker)
                print ("ouch, spikes")
        #Cheak health of enemy/attacker
        for enemy in enemylist[::]: #making duplist to make sure every enemy is checked
            if enemy.health <= 0:
                print(attacker, " killed " ,enemy)
                enemylist.remove(enemy)
        if attacker.health <= 0:
            print(attacker, " died due to spikes.")
            if attacker.isMonster:
                self.monsters.remove(attacker)
            else:
                self.angels.remove(attacker)
                
    def _after_damage_healtharmor(self, damage, defender):
            defender.health -= max(0, damage - defender.armor)
            defender.armor = max(0, defender.armor - damage) 

    
    def eob_calc(self):
        for creature in self.monsters + self.angels:
            #regen 
            if creature.get_stacks("regen") >0:
                creature.health = min(creature.health + creature.get_stacks("regen"), creature.maxhealth)
                print(creature, " healed!")
            #decay
            for status, value in creature.state.status_dict.items():
                value[0] = max(0, value[0] - value[1]) #stacks decaying
    
    def __str__(self):
        return str(self.monsters) + "fu" + str(self.angels)


    
    
'''    
scary = Creature(9001,1,0)
meow = Creature(1,9002,11)
meow.modify_stacks("mstrike", 3)
tadah = Creature(10.2, 10.5)
tadah.modify_stacks("daze", 1)

fight = Floor()
fight.addmonster(scary)
fight.addmonster(meow)
fight.addangel(tadah)
fight.battle()
'''


#log1
stewy = Creature("stewy",True,5,8)
hornbreaker = Creature("hornbreaker",True,6,6,0)
hornbreaker.modify_stacks("regen", 3)
hornbreaker.modify_stacks("mstrike", 1)
hornbreaker.modify_stacks("quick", 1)
badguy1 = Creature("badeguy1", False, 1,1,4)
badguy1.modify_stacks("daze",1)
badguy2 = Creature("badguy2", False, 1,1,10)
badguy2.modify_stacks("daze",1)
badguy3 = Creature("badguy3", False, 1,1,10)
badguy3.modify_stacks("daze",1)
badguy3.modify_stacks("sweep",1)
badguy3.modify_stacks("spike", 2)
badguy4 = Creature("mr.wolf", False, 1,10,10)
badguy4.modify_stacks("daze",1)
badguy4.modify_stacks("rage",5)
badguy4.modify_stacks("relentless",1)
badguy4.modify_stacks("sap",2)
fight = Floor()
abc = [stewy, hornbreaker, badguy1, badguy2, badguy3, badguy4]
for i in abc:
    fight.addcreature(i)
fight.battle()

    
        
        
    

    
    
