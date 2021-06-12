import re
from PIL import Image, ImageGrab
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import numpy as np
from datetime import date
import jpype
from tkinter import *

jpype.startJVM(jpype.getDefaultJVMPath(), '-ea', '-Djava.classpath.path=.')
handHistoryPath = 'C:\\Users\\testw\\Documents\\Winamax Poker\\accounts\\roucoups\\history'

def calculer():

        raiseList =[]
        evTreshold = variable.get()
        playersInfo = []
        playerName = []
        playerStacks = []
        seatOrder = []
        stacks = []
        finalOrderName = []
        noSmallBlind = False
        flop = False
        turn = False
        river = False
        payouts = [0.333, 0.333, 0.333, 0, 0, 0]
        dateInverted =[]

        pic = ImageGrab.grab(bbox =(0, 0, 470, 22))
        pic = pic.convert('RGB')
        picFocus = np.array(pic)
        windowTitle = pytesseract.image_to_string(picFocus ,config='--psm 13 --oem 3')
        ante = 0
        numeroTournoi = re.search(r'\d+', re.search(r'\(\d+\)', windowTitle).group()).group()
        BB = re.search(r'\d+', re.search(r'\-\d+', windowTitle).group()).group()
        if re.search(r'\(ante \d+\)', windowTitle):
                ante = re.search(r'\d+', re.search(r'\(ante \d+\)', windowTitle).group()).group()

        #today = date.today()	
        #d1 = today.strftime("%d/%m/%Y")
        #dateInverted.extend(re.findall(r'\d+', d1))
        #jour = dateInverted[0]
        #mois = dateInverted[1]
        #annee = dateInverted[2]

        HHPath = handHistoryPath + '\\' + '20210425_Double or Nothing(' + numeroTournoi + ')_real_holdem_no-limit.txt'
        #HHPath = handHistoryPath + '\\' + annee + mois + jour + '_Double or Nothing(' + numeroTournoi + ')_real_holdem_no-limit.txt'
        handhistory = open(HHPath, 'r')
        historyLines = handhistory.readlines()
                

        for index in reversed(range(len(historyLines))):
                if re.search(r'Winamax Poker', historyLines[index]):
                        startLine = index
                        break

        for index2 in range(startLine, len(historyLines)):
                if re.search(r'\*\*\* PRE-FLOP \*\*\*', historyLines[index2]):
                        preflopLine = index2

        for index3 in range(startLine, len(historyLines)):
                if re.search(r'\*\*\* FLOP \*\*\*', historyLines[index3]):
                        flopLine = index3
                        flop = True

        for index4 in range(startLine, len(historyLines)):
                if re.search(r'\*\*\* TURN \*\*\*', historyLines[index4]):
                        turnLine = index4
                        turn = True

        for index5 in range(startLine, len(historyLines)):
                if re.search(r'\*\*\* RIVER \*\*\*', historyLines[index5]): 
                        riverLine = index5
                        river = True

        for index6 in range(startLine, len(historyLines)):
                if re.search(r'\*\*\* SUMMARY \*\*\*', historyLines[index6]): 
                        summaryLine = index6

        for index7 in range(startLine, len(historyLines)):
                if re.search(r'posts .+ blind', historyLines[index7]):
                        blindLine = index7
                        break

        nextUtg = re.search(r'\w+', re.search(r'\w+', historyLines[preflopLine+2]).group()).group()

        for index in range(startLine, len(historyLines)):
                playersInfo.extend(re.findall(r'(Seat .+\d+\))', historyLines[index]))


        for items in playersInfo:
                playerName.append(re.search(r'\w+', re.search(r'(: .+ \()', items).group()).group())
                playerStacks.append(re.search(r'\d+', re.search(r'\(\d+\)', items).group()).group())
                
        if not flop:
                
                                                        ###### PREFLOP #######

                for index7 in reversed(range(blindLine, summaryLine)):                 # recupère toutes les mises preflop
                                for index8 in range(len(playerName)):
                                        if re.search(r'(\d+)$', historyLines[index7]):
                                                postName = re.search(r'\w+', historyLines[index7]).group()
                                                postAmount = re.search(r'(\d+)$', historyLines[index7]).group() 

                                                if str(postName) not in raiseList:
                                                        if playerName[index8] == postName:
                                                                playerStacks[index8] = int(playerStacks[index8]) - int(postAmount)
                                                                if re.search(r'raises \d+ to \d', historyLines[index7]): 
                                                                        raiseList.append(playerName[index8])
        if flop:
                

                                                        ###### PREFLOP #######

                for index7 in reversed(range(blindLine, flopLine)):                 # recupère toutes les mises preflop
                                for index8 in range(len(playerName)):
                                        if re.search(r'(\d+)$', historyLines[index7]):
                                                postName = re.search(r'\w+', historyLines[index7]).group()
                                                postAmount = re.search(r'(\d+)$', historyLines[index7]).group() 

                                                if str(postName) not in raiseList:
                                                        if playerName[index8] == postName:
                                                                playerStacks[index8] = int(playerStacks[index8]) - int(postAmount)
                                                                if re.search(r'raises \d+ to \d', historyLines[index7]): 
                                                                        raiseList.append(playerName[index8])

        raiseList.clear()

        if flop and turn and river:     # dans le cas ou il y a flop/turn/river
                        

                                    ######## FLOP #########

                for index11 in reversed(range(flopLine, turnLine)):           # recupère toute les mises au flop
                        for index12 in range(len(playerName)):
                                if re.search(r'(\d+)$', historyLines[index11]):
                                        postName = re.search(r'\w+', historyLines[index11]).group()
                                        postAmount = re.search(r'(\d+)$', historyLines[index11]).group() 

                                        if str(postName) not in raiseList:
                                                if playerName[index12] == postName:
                                                        playerStacks[index12] = int(playerStacks[index12]) - int(postAmount)
                                                        if re.search(r'raises \d+ to \d+', historyLines[index11]):
                                                                raiseList.append(playerName[index12])
                raiseList.clear()

                                    ######## TURN #########

                for index13 in reversed(range(turnLine, riverLine)):           # recupère toute les mises au turn
                        for index14 in range(len(playerName)):
                                if re.search(r'(\d+)$', historyLines[index13]):
                                        postName = re.search(r'\w+', historyLines[index13]).group()
                                        postAmount = re.search(r'(\d+)$', historyLines[index13]).group() 

                                        if str(postName) not in raiseList:
                                                if playerName[index14] == postName:
                                                        playerStacks[index14] = int(playerStacks[index14]) - int(postAmount)
                                                        if re.search(r'raises \d+ to \d+', historyLines[index13]):
                                                                raiseList.append(playerName[index14])
                raiseList.clear()
                

                                    ######## RIVER #########

                for index15 in reversed(range(riverLine, summaryLine)):           # recupère toute les mises à la river
                        for index16 in range(len(playerName)):
                                if re.search(r'(\d+)$', historyLines[index15]):
                                        postName = re.search(r'\w+', historyLines[index15]).group()
                                        postAmount = re.search(r'(\d+)$', historyLines[index15]).group()

                                        if str(postName) not in raiseList:
                                                if playerName[index16] == postName:
                                                        playerStacks[index16] = int(playerStacks[index16]) - int(postAmount)
                                                        if re.search(r'raises \d+ to \d+', historyLines[index15]):
                                                                raiseList.append(playerName[index16])
                raiseList.clear()

        elif flop and turn and not river:  #dans le cas ou il y a flop/turn
                
                                                    ######## FLOP #########

                for index17 in reversed(range(flopLine, turnLine)):           # recupère toute les mises au flop
                        for index18 in range(len(playerName)):
                                if re.search(r'(\d+)$', historyLines[index17]):
                                        postName = re.search(r'\w+', historyLines[index17]).group()
                                        postAmount = re.search(r'(\d+)$', historyLines[index17]).group() 

                                        if str(postName) not in raiseList:
                                                if playerName[index18] == postName:
                                                        playerStacks[index18] = int(playerStacks[index18]) - int(postAmount)
                                                        if re.search(r'raises \d+ to \d+', historyLines[index17]):
                                                                raiseList.append(playerName[index18])
                raiseList.clear()

                                    ######## TURN #########

                for index19 in reversed(range(turnLine, summaryLine)):           # recupère toute les mises au turn
                        for index20 in range(len(playerName)):
                                if re.search(r'(\d+)$', historyLines[index19]):
                                        postName = re.search(r'\w+', historyLines[index19]).group()
                                        postAmount = re.search(r'(\d+)$', historyLines[index19]).group() 

                                        if str(postName) not in raiseList:
                                                if playerName[index20] == postName:
                                                        playerStacks[index20] = int(playerStacks[index20]) - int(postAmount)
                                                        if re.search(r'raises \d+ to \d+', historyLines[index19]):
                                                                raiseList.append(playerName[index20])
                raiseList.clear()

        elif flop and not turn and not river:   # dans le cas ou il y a seulement flop

                                                    ######## FLOP #########

                for index21 in reversed(range(flopLine, summaryLine)):           # recupère toute les mises au flop
                        for index22 in range(len(playerName)):
                                if re.search(r'(\d+)$', historyLines[index21]):
                                        postName = re.search(r'\w+', historyLines[index21]).group()
                                        postAmount = re.search(r'(\d+)$', historyLines[index21]).group() 

                                        if str(postName) not in raiseList:
                                                if playerName[index22] == postName:
                                                        playerStacks[index22] = int(playerStacks[index22]) - int(postAmount)
                                                        if re.search(r'raises \d+ to \d+', historyLines[index21]):
                                                                raiseList.append(playerName[index22])
                raiseList.clear()


        for index100 in range(startLine, len(historyLines)):           # recupère ante
                if re.search('posts ante', historyLines[index100]):
                        anteName = re.search(r'\w+', historyLines[index100]).group()
                        anteAmount = re.search(r'\d+', re.search(r'posts ante \d+', historyLines[index100]).group()).group()

                        for index101 in range(len(playerName)):
                                if playerName[index101] == anteName:
                                        playerStacks[index101] = int(playerStacks[index101]) - int(anteAmount)


        for index23 in range(startLine, len(historyLines)):           # cherche si joueur all-in et lui attribue stack = 0
                if re.search('and is all-in', historyLines[index23]):
                        allinName = re.search(r'\w+', historyLines[index23]).group()

                        for index24 in range(len(playerName)):
                                if playerName[index24] == allinName:
                                        playerStacks[index24] = 0

        for index25 in range(startLine, len(historyLines)):           # rend le montant du pot au(x) vainqueur(s)

                if re.search('collected \d+', historyLines[index25]):
                        collectedName = re.search(r'\w+', historyLines[index25]).group()
                        collectedAmount = re.search(r'\d+', re.search(r'collected \d+ from', historyLines[index25]).group()).group()

                        for index26 in range(len(playerName)):
                                if playerName[index26] == collectedName:
                                        playerStacks[index26] = int(playerStacks[index26]) + int(collectedAmount)

       

        for index7 in range(len(playerName)):

                if playerName[index7] == nextUtg:
                        nextHandStart = index7

        for index8 in range(len(playerStacks)):
                if nextHandStart+index8 > len(playerStacks)-1:
                        nextHandStart = nextHandStart - len(playerStacks)

                stacks.append(playerStacks[index8 + nextHandStart])

        for index12 in range(len(playerName)):
                if nextHandStart+index12 > len(playerName)-1:
                        nextHandStart = nextHandStart - len(playerName)

                finalOrderName.append(playerName[index12 + nextHandStart])

        sb = len(stacks)-2
        if stacks[sb] == 0:
                noSmallBlind = True
     
        for index11 in range(len(finalOrderName)):
                if finalOrderName[index11] == "roucoups":
                        hero = index11

        playerStacksToHero = stacks[(hero):]
        stackszero = 0

        for index13 in range(len(playerStacksToHero)):
                if playerStacksToHero[index13] == 0:
                        stackszero = stackszero +1
        hero = (len(playerStacksToHero)-1) - stackszero
        raiser = varGr.get()
        
        if raiser > 11:
                raiser = hero
        
        if raiser == hero and hero == 0:
                raiser = 1

        bbFound = 0
        while bbFound == 0:
            lastPlayer = len(stacks)-1
            if stacks[lastPlayer] == 0:
                stacks.pop(lastPlayer)
                temp = stacks[0]
                stacks.pop(0)
                stacks.append(temp)
                if temp != 0:
                    bbFound = 1

            else:
                bbFound = 1

        stacks = [i for i in stacks if i != 0]

        players = len(stacks)
        payouts = payouts[:(players)]

        _cr = jpype.JPackage("pokerai").game.icm.CalcRanges()

        def _list_to_jarray(jtype, plist):
            jarray = jpype.JArray(jtype)(len(plist))

            for i, val in enumerate(plist):
                jarray[i] = jtype(val)

            return jarray 

        def calc(players, stacks, raiser, bb, ante, nosb, evthreshold, payouts):
            jplayers = jpype.JInt(players)
            jstacks = _list_to_jarray(jpype.JInt, stacks)
            jranges = jpype.JArray(jpype.JInt)(players)
            jraiser = jpype.JInt(raiser)
            jBB = jpype.JInt(bb)
            jante = jpype.JInt(ante)
            jnoSmallBlind = jpype.JBoolean(noSmallBlind)
            jevTreshold = jpype.JDouble(evTreshold)
            jpayouts = _list_to_jarray(jpype.JDouble, payouts)

            _cr.calc(jplayers, jstacks, jraiser, jBB, jante, jnoSmallBlind, jevTreshold, jpayouts, jranges);
            return [r for r in jranges]

        ranges = calc(players, stacks, raiser, BB, ante, noSmallBlind, evTreshold, payouts);

        dictionnaire = {0:"none", 1:"KK+,AKs", 2:"QQ+,AK", 3:"JJ+,AK", 4:"TT+,AQ+", 5:"99+,AQ+", 6:"88+,AQo+,ATs+", 7:"88+,AJo+,ATs+", 8:"66+,AT+", 9:"66+,ATo+,A9s+", 10:"55+,ATo+,A8s+,KQs", 11:"44+,A9o+,A8s+,KQs", 12:"44+,A9o+,A7s+,KJs+", 13:"44+,AKs,AQs,AJs,ATs,A9s,A8s,A8o+,A7s,A5s,KJs+", 14:"44+,A8o+,A4s+,KJs+", 15:"33+,A7o+,A4s+,KTs+", 16:"33+,A7o+,A3s+,KQo,KTs+", 17:"33+,A7o+,A2s+,KQo,KTs+", 18:"33+,AKo,AQo,AJo,ATo,A9o,A8o,A7o,A5o,A2s+,KQo,KTs+", 19:"33+,A5o+,A2s+,KQo,KTs+", 20:"33+,A4o+,A2s+,KJo+,KTs+", 21:"33+,A4o+,A2s+,KJo+,KTs+,QJs", 22:"33+,A3o+,A2s+,KJo+,KTs+,QJs", 23:"22+,A2+,KJo+,K9s+,QJs", 24:"22+,A2+,KTo+,K9s+,QJs", 25:"22+,A2+,KTo+,K8s+,QTs+", 26:"22+,A2+,K9o+,K7s+,QTs+,JTs", 27:"22+,A2+,K9o+,K6s+,QJo,QTs+,JTs", 28:"22+,A2+,K9o+,K6s+,QJo,Q9s+,JTs", 29:"22+,A2+,K8o+,K5s+,QJo,Q9s+,JTs", 30:"22+,A2+,K8o+,K4s+,QTo+,Q9s+,JTs", 31:"22+,A2+,K7o+,K4s+,QTo+,Q9s+,JTs", 32:"22+,A2+,K7o+,K2s+,QTo+,Q9s+,JTs", 33:"22+,A2+,K6o+,K2s+,QTo+,Q8s+,JTs", 34:"22+,A2+,K5o+,K2s+,QTo+,Q8s+,J9s+", 35:"22+,A2+,K5o+,K2s+,Q9o+,Q8s+,J9s+", 36:"22+,A2+,K5o+,K2s+,Q9o+,Q8s+,JTo,J9s+", 37:"22+,A2+,K4o+,K2s+,Q9o+,Q8s+,JTo,J9s+", 38:"22+,A2+,K4o+,K2s+,Q9o+,Q6s+,JTo,J9s+,T9s", 39:"22+,A2+,K3o+,K2s+,Q9o+,Q6s+,JTo,J9s+,T9s", 40:"22+,A2+,K2+,Q9o+,Q5s+,JTo,J8s+,T9s", 41:"22+,A2+,K2+,Q8o+,Q5s+,JTo,J8s+,T9s", 42:"22+,A2+,K2+,Q8o+,Q4s+,J9o+,J8s+,T9s", 43:"22+,A2+,K2+,Q8o+,Q3s+,J9o+,J8s+,T8s+", 44:"22+,A2+,K2+,Q7o+,Q3s+,J9o+,J7s+,T8s+", 45:"22+,A2+,K2+,Q6o+,Q2s+,J9o+,J7s+,T8s+", 46:"22+,A2+,K2+,Q6o+,Q2s+,J9o+,J7s+,T8s+,98s", 47:"22+,A2+,K2+,Q5o+,Q2s+,J8o+,J7s+,T8s+,98s", 48:"22+,A2+,K2+,Q5o+,Q2s+,J8o+,J7s+,T9o,T8s+,98s", 49:"22+,A2+,K2+,Q5o+,Q2s+,J8o+,J6s+,T9o,T8s+,98s", 50:"22+,A2+,K2+,Q4o+,Q2s+,J8o+,J5s+,T9o,T7s+,98s", 51:"22+,A2+,K2+,Q4o+,Q2s+,J7o+,J4s+,T9o,T7s+,98s", 52:"22+,A2+,K2+,Q3o+,Q2s+,J7o+,J4s+,T9o,T7s+,98s", 53:"22+,A2+,K2+,Q3o+,Q2s+,J7o+,J4s+,T8o+,T7s+,97s+", 54:"22+,A2+,K2+,Q3o+,Q2s+,J7o+,J3s+,T8o+,T7s+,97s+", 55:"22+,A2+,K2+,Q2+,J7o+,J3s+,T8o+,T6s+,97s+", 56:"22+,A2+,K2+,Q2+,J6o+,J2s+,T8o+,T6s+,97s+,87s", 57:"22+,A2+,K2+,Q2+,J6o+,J2s+,T8o+,T6s+,98o,97s+,87s", 58:"22+,A2+,K2+,Q2+,J6o+,J2s+,T7o+,T6s+,98o,97s+,87s", 59:"22+,A2+,K2+,Q2+,J5o+,J2s+,T7o+,T6s+,98o,96s+,87s", 60:"22+,A2+,K2+,Q2+,J5o+,J2s+,T7o+,T5s+,98o,96s+,87s", 61:"22+,A2+,K2+,Q2+,J4o+,J2s+,T7o+,T4s+,98o,96s+,86s+", 62:"22+,A2+,K2+,Q2+,J4o+,J2s+,T6o+,T4s+,98o,96s+,86s+", 63:"22+,A2+,K2+,Q2+,J4o+,J2s+,T6o+,T4s+,97o+,96s+,86s+", 64:"22+,A2+,K2+,Q2+,J4o+,J2s+,T6o+,T3s+,97o+,96s+,86s+,76s", 65:"22+,A2+,K2+,Q2+,J3o+,J2s+,T6o+,T3s+,97o+,95s+,86s+,76s", 66:"22+,A2+,K2+,Q2+,J3o+,J2s+,T6o+,T2s+,97o+,95s+,87o,86s+,76s", 67:"22+,A2+,K2+,Q2+,J3o+,J2s+,T6o+,T2s+,96o+,95s+,87o,85s+,76s", 68:"22+,A2+,K2+,Q2+,J3o+,J2s+,T5o+,T2s+,96o+,95s+,87o,85s+,76s", 69:"22+,A2+,K2+,Q2+,J2+,T5o+,T2s+,96o+,95s+,87o,85s+,76s", 70:"22+,A2+,K2+,Q2+,J2+,T5o+,T2s+,96o+,94s+,87o,85s+,75s+", 71:"22+,A2+,K2+,Q2+,J2+,T4o+,T2s+,96o+,94s+,87o,85s+,75s+", 72:"22+,A2+,K2+,Q2+,J2+,T4o+,T2s+,96o+,94s+,86o+,85s+,75s+,65s", 73:"22+,A2+,K2+,Q2+,J2+,T4o+,T2s+,95o+,93s+,86o+,84s+,75s+,65s", 74:"22+,A2+,K2+,Q2+,J2+,T3o+,T2s+,95o+,93s+,86o+,84s+,75s+,65s", 75:"22+,A2+,K2+,Q2+,J2+,T3o+,T2s+,95o+,93s+,86o+,84s+,76o,75s+,65s", 76:"22+,A2+,K2+,Q2+,J2+,T3o+,T2s+,95o+,92s+,86o+,84s+,76o,74s+,65s", 77:"22+,A2+,K2+,Q2+,J2+,T2+,95o+,92s+,86o+,84s+,76o,74s+,65s,54s", 78:"22+,A2+,K2+,Q2+,J2+,T2+,95o+,92s+,85o+,84s+,76o,74s+,65s,54s", 79:"22+,A2+,K2+,Q2+,J2+,T2+,94o+,92s+,85o+,83s+,76o,74s+,64s+,54s", 80:"22+,A2+,K2+,Q2+,J2+,T2+,94o+,92s+,85o+,83s+,75o+,74s+,64s+,54s", 81:"22+,A2+,K2+,Q2+,J2+,T2+,94o+,92s+,85o+,82s+,75o+,73s+,64s+,54s", 82:"22+,A2+,K2+,Q2+,J2+,T2+,93o+,92s+,85o+,82s+,75o+,73s+,64s+,54s", 83:"22+,A2+,K2+,Q2+,J2+,T2+,93o+,92s+,85o+,82s+,75o+,73s+,65o,64s+,54s", 84:"22+,A2+,K2+,Q2+,J2+,T2+,93o+,92s+,84o+,82s+,75o+,73s+,65o,63s+,53s+", 85:"22+,A2+,K2+,Q2+,J2+,T2+,92+,84o+,82s+,75o+,73s+,65o,63s+,53s+", 86:"22+,A2+,K2+,Q2+,J2+,T2+,92+,84o+,82s+,74o+,73s+,65o,63s+,53s+,43s", 87:"22+,A2+,K2+,Q2+,J2+,T2+,92+,84o+,82s+,74o+,72s+,65o,63s+,53s+,43s", 88:"22+,A2+,K2+,Q2+,J2+,T2+,92+,84o+,82s+,74o+,72s+,64o+,63s+,54o,53s+,43s", 89:"22+,A2+,K2+,Q2+,J2+,T2+,92+,84o+,82s+,74o+,72s+,64o+,63s+,54o,52s+,43s", 90:"22+,A2+,K2+,Q2+,J2+,T2+,92+,83o+,82s+,74o+,72s+,64o+,62s+,54o,52s+,43s", 91:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,74o+,72s+,64o+,62s+,54o,52s+,42s+", 92:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,73o+,72s+,64o+,62s+,54o,52s+,42s+", 93:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,73o+,72s+,64o+,62s+,53o+,52s+,42s+", 94:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,73o+,72s+,63o+,62s+,53o+,52s+,42s+", 95:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,73o+,72s+,63o+,62s+,53o+,52s+,43o,42s+,32s", 96:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,72+,63o+,62s+,53o+,52s+,43o,42s+,32s", 97:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,72+,63o+,62s+,52+,43o,42s+,32s", 98:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,72+,62+,52+,43o,42s+,32s", 99:"22+,A2+,K2+,Q2+,J2+,T2+,92+,82+,72+,62+,52+,42+,32s", 100:"any two"}

        pourcentageHero = ranges[hero]

        Texte.set(str(pourcentageHero) + '% ' + str(dictionnaire[pourcentageHero]))

# Création de la fenêtre principale (main window)
Mafenetre = Tk()
Mafenetre.title('fpdb-0.40.5')
Mafenetre.wm_attributes("-topmost", 1)

BoutonLancer = Button(Mafenetre, text ='import', command = calculer)
BoutonLancer.pack(side = LEFT, padx = 5, pady = 1)

Texte = StringVar()

#menu déroulant
OptionList = [0, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
variable = StringVar()
variable.set(OptionList[0])
opt = OptionMenu(Mafenetre, variable, *OptionList)
opt.pack(side = LEFT, padx = 5, pady = 1)

#radiobuttons
vals = [12, 2, 3, 4, 5]#, 6, 7, 8, 9]
etiqs = ['auto', 'bu', 'co', 'mp', 'utg']#, '6', '7', '8', '9']
varGr = IntVar()
varGr.set(vals[0])
for i in range(5):#(9):
    b = Radiobutton(Mafenetre, variable=varGr, text=etiqs[i], value=vals[i])
    b.pack(side = LEFT)#, expand=1)

LabelResultat = Label(Mafenetre, textvariable=Texte , fg ='red', bg ='white')
LabelResultat.pack(side = LEFT, padx = 5, pady = 1)

Mafenetre.mainloop()

                                        
                                        









