# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 08:53:55 2020

@author: Bennett
"""
import random
"""
Dreidel rules:
    nun-nothing
    gimel- take all
    hay- take one (sometimes take half)
    shin- give one
"""
outcome=["nun","gimel","hay","shin"]
winstate=False
pot=0

class Player:
    def __init__(self,name,hand):
        self.name=name
        self.hand=hand
        self.active=True
        self.winner=False
        
    def spin(self):
        global pot
        #print(self.name+" is spinning")
        side=random.randint(0,3)
        #print("#### "+outcome[side]+" ####")
        if side==1:
            self.hand+=pot
            pot-=pot
            #print(self.name+" takes all")
        if side==2:
            if pot>0:
                self.hand+=1
                pot-=1
                #print(self.name+" takes 1")
            else:
                #print("nothing in pot to take")
                pass
        if side==3:
            self.hand-=1
            pot+=1
            #print(self.name+" gives 1")
        if side==0:
            #print(self.name+" loses turn")
            pass
            
    def checkloser(self):
        global losers
        global winstate
        if self.hand<=0:
            print(self.name + " has lost")
            self.active=False                        
        else:
            #print(self.name+ " has "+str(self.hand))
            pass
            
p1=Player("Adam",20)
p2=Player("Bill",20)
p3=Player("Charlie",20)
p4=Player("Dave",20)

players=[p1,p2,p3,p4]


games=100
wintotals={p1.name:0,p2.name:0,p3.name:0,p4.name:0}
for game in range(games):
    
    rounds=0
    winstate=False
            
    while not winstate:
        losers=0
        for player in players:
            #print("\npot has {}\n".format(str(pot)))
            if player.active:
                player.spin()
                player.checkloser()
            if not player.active:
                losers+=1
               
            if losers>=3:
                winstate=True
                break            
        rounds+=1
                            
    print("\nNumber of rounds: "+str(rounds))
    for player in players:
        if player.hand>0:
            print(player.name + " wins")
            wintotals[player.name]+=1
        player.active=True
        player.hand=10
    print(wintotals)
    #input()
    
        
        
        
        



        