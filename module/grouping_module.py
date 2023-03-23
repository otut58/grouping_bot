import discord
from discord.ext import commands
import random

def addMember(members, name, id):
    if len(members) >= 10:
        return '10人までしか登録できないよ！'
    members.append(Member(name, id[0]))
    id[0] = id[0] + 1
    return f'{name}さんが参加しました！'

def setLongRange(members, name):
    nameInMembers = False
    for m in members:
        if m.name == name:
            m.havelongRangeWeapon()
            nameInMembers = True
            return f'{name}さんは後衛です！'
    if not nameInMembers:
        return f'{name}さんはいませんでした...'


def grouping(members, alpha, bravo):
    if len(members) > 8:
        gameMembers = pickMembers(members)
    elif len(members) < 8:
        return '最低でも8人は必要だよ！'
    elif len(members) == 8:
        gameMembers = members
    if len(gameMembers) < 8:
        return '8人じゃないよ！'
    memberSet = ''
    alpha.dissolution()
    bravo.dissolution()
    sortedByRate = sorted(gameMembers, key=lambda m : m.rate)
    for i in range(2):
        alpha.groupingTopRate(sortedByRate)
        alpha.groupingUnderRate(sortedByRate)
        bravo.groupingTopRate(sortedByRate)
        bravo.groupingUnderRate(sortedByRate)
    for m in members:
        if m.isWatching:
            memberSet += f'{m.name}: 観戦\n'
        else:
            memberSet += f'{m.name}:  {m.group}\n'
    return memberSet

def pickMembers(members):
    for m in members:
        m.playGame()
    if len(members) == 10:
        choiceMemberWatchingGame(members)
    choiceMemberWatchingGame(members)    
    pickedMembers = [m for m in members if not m.isWatching] 
    return pickedMembers

def choiceMemberWatchingGame(members):
    checkWatchFlag(members)
    tmp = random.sample(members, len(members))
    for t in tmp:
        if not t.hasWatched:
            t.watchGame()
            break

def checkWatchFlag(members):
    allMembersHaveWatched = True
    for m in members:
        if not m.hasWatched:
            allMembersHaveWatched = False
            break
    if allMembersHaveWatched:
        for m in members:
            m.hasNotWatchedGame()

def countWin(members, alpha, bravo, matchNum, wonTeam):
    output = ''
    if wonTeam == 'alpha':
        alpha.win()
        output += f'{alpha.groupNameJa}が勝ちました！'
    elif wonTeam == 'bravo':
        bravo.win()
        output += f'{bravo.groupNameJa}が勝ちました！'
    else:
        return 'そんなチームないよ！'
    matchNum[0] = matchNum[0] + 1
    for m in members:
        m.calcRate(matchNum[0])
    return output

def printMembers(members):
    output = '参加しているメンバー：\n'
    for m in members:
        output += f'{m.name}: {m.id}\n'
    return output

def printRate(members):
    output = '現在の勝率：\n'
    for m in members:
        output += f'{m.name}: {m.rate}\n'
    return output

def readWeapons():
    f = open('weapons.txt', 'r', encoding='UTF-8')
    weapons= f.readlines()
    f.close()
    return weapons

def choiceWeapon():
    weapons = readWeapons()
    return random.choice(weapons)

def choiceWeaponForMembers(members):
    output = ''
    for m in members:
        output += f'{m.name}: {choiceWeapon()}'
    return output

def readInst():
    f = open('help.txt', 'r', encoding='UTF-8')
    instMessage = f.readlines()
    f.close()
    return instMessage

def printInst():
    message = readInst()
    output = ''
    for m in message:
        output += m
    return output

class Member:

    def __init__(self, name, id):
        self.name = name
        self.winNum = 0
        self.rate = 0
        self.isLongRange = False
        self.isGrouped = False
        self.id = id
        self.group = ''
        self.isWatching = False
        self.hasWatched = False
    
    def havelongRangeWeapon(self):
        self.isLongRange = True

    def win(self):
        self.winNum += 1

    def calcRate(self, matchNum):
        self.rate = self.winNum / matchNum
    
    def grouped(self):
        self.isGrouped = True

    def isNotGrouped(self):
        self.isGrouped = False

    def isWhichGroup(self, group):
        self.group = group

    def watchGame(self):
        self.hasWatched = True
        self.isWatching = True

    def hasNotWatchedGame(self):
        self.hasWatched = False

    def playGame(self):
        self.isWatching = False


class Group:

    def __init__(self, name, nameJa):
        self.groupName = name
        self.groupNameJa = nameJa
        self.grooupedMembers = []
        self.hasLongRangeMember = False

    def printMembers(self):
        random.shuffle(self.grooupedMembers)
        memberList = ''
        for g in self.grooupedMembers:
            memberList += f'{g.name}\n'
        return memberList

    def win(self):
        for g in self.grooupedMembers:
            g.win()

    def dissolution(self):
        self.hasLongRangeMember = False
        for g in self.grooupedMembers:
            g.isNotGrouped()
        self.grooupedMembers = []

    def addGroup(self, member):
        self.grooupedMembers.append(member)
        member.isWhichGroup(self.groupNameJa)
        if member.isLongRange:
            self.hasLongRangeMember = True

    def groupingConcideredRange(self, member):
        if not self.hasLongRangeMember:
            self.addGroup(member)
            member.grouped()
            return True
        elif not member.isLongRange:
            self.addGroup(member)
            member.grouped()
            return True
        else:
            return False

    def groupingTopRate(self, members):
        for i in range(len(members)):
            if not members[i].isGrouped:
                if self.groupingConcideredRange(members[i]):
                    break

    def groupingUnderRate(self, members):
        for i in range(len(members))[::-1]:
            if not members[i].isGrouped:
                if self.groupingConcideredRange(members[i]):
                    break