from os import system, name
from random import shuffle, choice

suits = ["♥", "♦", "♣", "♠"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

#Get suit of card
def getSuit(card):
    for suit in suits:
        if suit in card:
            return suit
    return None

#Get rank of card
def getRank(card):
    return card.replace(getSuit(card),"")

#Get highest ranked card, ignore suit
def getHighest(cards):
    highest=cards[0]
    for card in cards:
        if ranks.index(getRank(card)) > ranks.index(getRank(highest)):highest=card
    return highest

#Sort by rank, ignore suit
def sort(cards):
    sorted=[]
    while len(cards) > 0:
        highest=getHighest(cards)
        sorted.append(highest)
        cards.remove(highest)        
    return sorted

#Create the 52-card deck in order
def createDeck():
    deck=[]
    for suit in suits:
        for rank in ranks:
            deck.append(rank+suit)
    return deck

#Deal cards to players, return the trump suit
def deal(players, hand):
    deck=createDeck()
    shuffle(deck)
    trump = None
    if hand == 13:
        trump = getSuit(deck[int(len(deck)/2)])
    for i in range(hand):    
        for player in players:
            card=deck[0]
            deck.remove(card)
            player.append(card)

    if hand != 13:
        trump = getSuit(deck[0])

    #Sort each player's hand by suit then rank, starting with trumps
    sPlayers=[]
    for player in players:
        sp=[player[0]]
        catSuits=[[],[],[],[]]
        for card in player[1:]:
            catSuits[suits.index(getSuit(card))].append(card)
        
        scatSuits=[]
        for suit in catSuits:
            if len(suit)>0 and getSuit(suit[0]) == trump:
                scatSuits.append(suit)
        for suit in catSuits:
            if len(suit)>0 and getSuit(suit[0]) != trump:
                scatSuits.append(suit)
        
        for suit in scatSuits:
            sorted=sort(suit)
            for card in sorted:
                sp.append(card)
        sPlayers.append(sp)

    return trump, sPlayers

#TODO: don't play a trump if reached goal, bet more if leading and have high card, bet more if num cards is low 
#Play a card
def play(player, table, trump, tricks, bet):
    cards=player[1:]
    if len(table) > 0:
        led=table[0]
        follow=[]
        for card in cards:
            if getSuit(card)==getSuit(led):
                follow.append(card)
                cards.remove(card)
        
        if len(follow)>0:
            lowest=follow[0]
            for card in follow:
                if ranks.index(getRank(card)) < ranks.index(getRank(lowest)):lowest=card
            highest=follow[0]
            for card in follow:
                if ranks.index(getRank(card)) > ranks.index(getRank(highest)):highest=card
            
            if tricks == bet: #Try to lose the trick
                return lowest
            else: #Try to win more or conserve higher cards
                #Check if can win hand
                for card in table:
                    if getRank(card) == getRank(led) and ranks.index(getRank(card)) < ranks.index(getRank(highest)):
                        return highest
                return lowest
            return choice(follow)
    
    trumps=[]
    for card in cards:
        if getSuit(card)==trump:
            trumps.append(card)
            cards.remove(card)
    
    if len(trumps)>0:
        return choice(trumps)
    
    return choice(cards)

#Determine who won the trick
def getWinner(table, trump):
    led=table[0]
    highest=led
    for card in table:
        if card==led:continue
        if getSuit(card) == getSuit(led) and ranks.index(getRank(card))>ranks.index(getRank(highest)):highest=card
    
    if  getSuit(led)!=trump:
        for card in table:
            if card==led:continue
            if getSuit(card)==trump:
                if getSuit(highest) != trump:highest=card
                else: 
                    if ranks.index(getRank(card))>ranks.index(getRank(highest)):highest=card
    return table.index(highest)

#Figure out how many cards should be bet
def shouldBet(cards, trump, isLeading):
    num=0
    for card in cards:
        if (ranks.index(getRank(card)) >= ranks.index("7" if isLeading else "10") and getSuit(card) == trump) or (ranks.index(getRank(card)) >= ranks.index("9" if isLeading else "J")):num+=1
    return num


#Main method
def main():
    players=[["Chris"],["Pake"],["Dad"],["Rachel"]]
    scores=[0,0,0,0]
    for hand in range(1, 26):    
        #Clear screen
        if name == "nt": 
            system("cls") 
            system("echo off")
            system("color 06")
            system("title Up and Down the River")
        else: 
            system("clear") 
        
        print(players[0][0]+": "+str(scores[0])+"   "+players[1][0]+": "+str(scores[1])+"   "+players[2][0]+": "+str(scores[2])+"   "+players[3][0]+": "+str(scores[3]))

        #Deal cards and begin hand
        numCards=hand if hand <= 13 else 26-hand
        trump, players=deal(players, numCards)
        leading=hand%4
        print("Hand "+str(hand)+", "+str(numCards)+" card"+("s. " if numCards>1 else ". ")+" Trump is "+trump+". "+players[leading][0]+" leads")

        bid=[shouldBet(players[0][1:], trump, leading==0),shouldBet(players[1][1:], trump, leading==1),shouldBet(players[2][1:], trump, leading==2),shouldBet(players[3][1:], trump, leading==3)]
        tricks=[0,0,0,0]

        print(players[0][0]+" bets "+str(bid[0])+"   "+players[1][0]+" bets "+str(bid[1])+"   "+players[2][0]+" bets "+str(bid[2])+"   "+players[3][0]+" bets "+str(bid[3]))

        for trick in range(numCards):
            table=[]
            print("")

            #Let each player decide what card to play
            for i in range(4):
                index=i+leading
                if index>3:index-=4
                card=play(players[index], table, trump, tricks[index], bid[index])
                players[index].remove(card)
                table.append(card)
                print(players[index][0]+" plays "+card)
            winner=getWinner(table, trump)+leading
            if winner>3:winner-=4
            #Wait for input before advancing to next trick
            input("\n"+players[winner][0]+" wins. Press Enter to continue to next trick.")
            scores[winner]+=1
            tricks[winner]+=1
        
        for i in range(4):
            if tricks[i]==bid[i]:
                scores[i]+=5

        #Wait for input before advancing to next hand
        if hand < 25:
            input("\nPress Enter to continue to next hand.")

    if name == "nt":
        system("cls")
    else:
        system("clear")
    
    print("Final scores: "+players[0][0]+": "+str(scores[0])+"   "+players[1][0]+": "+str(scores[1])+"   "+players[2][0]+": "+str(scores[2])+"   "+players[3][0]+": "+str(scores[3]))
    winner=players[0]
    for i in range(len(scores)):
        if scores[i]>scores[players.index(winner)]:winner=players[i]
    print(winner[0]+" wins!")

if __name__=="__main__":
    main()