# replayparser.py by Rei Armenia(lazerzes)
#
# This function set takes in a .roa replay file and extracts the information
# that the user may find useful.


import sys
from enum import Enum

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def parser(filename):

    f = open(filename, "r")
    print ("file.name:", f.name)

    lines = f.readlines()
    players = []

    # Even lines contain player information, except for line 0 which contains
    # replay information, if an even line starts with the letter H then it is
    # a human player, and has an input replay that we can use.
    # This section of code detects if a line starts with H, if so then it takes
    # that line and the next line and puts it into a list of player objects
    for i, line in enumerate(lines):
        if (i % 2 == 0 and i != 0):
            if(line[0] == 'H'):
                players.append(Player(line, lines[i + 1]))

class Replay:
    def __init__(self):
        self.players = []


# The Player class is a wrapper for our player file, it contains the raw
# information that we pull from the replay file as information that we can
# easily work with in python.
class Player:
    def __init__(self, p_info, p_replay):
        self.name = self.getName(p_info)
        self.character = self.getCharacter(p_info)
        self.actions = self.getActions(p_replay)

    def getName(self, info_line):
        name = info_line[1:33]
        name = name.rstrip()
        print ("name:", name)
        return name

    def getCharacter(self, info_line):
        character_id = info_line[39:41]
        print("character_id:", character_id)
        enum = Character(int(character_id))
        print("enumized", enum, enum.value)
        return enum

    def getActions(self, replay_line):
        actions = []
        i = 0

        #self.getSingleAction(0, replay_line, actions)
        #print("action_frame", actions[0].frame_num, "action id", actions[0].input_id)

        while i < len(replay_line):
            i += self.getSingleAction(i, replay_line, actions)

    def getSingleAction(self, start, replay_line, action_list):
        counter = 0;
        frame_str = ""
        input_str = ""

        while True:
            if is_number(replay_line[start + counter]):
                frame_str = frame_str + replay_line[start + counter]
                counter += 1
            else:
                break

        while True:
            if replay_line[start + counter] != 'y':
                input_str = input_str + replay_line[start + counter]
                break
            else:
                input_str = input_str + replay_line[start + counter]
                counter += 1
                input_str = input_str + replay_line[start + counter]
                counter += 1
                input_str = input_str + replay_line[start + counter]
                counter += 1
                input_str = input_str + replay_line[start + counter]
                break

        print("action_frame", frame_str, "action id", input_str)
        action_list.append(Action(frame_str, input_str))

        counter += 1
        return counter



class Action:
    def __init__(self, frame_num, input_id):
        self.frame_num = frame_num
        self.input_id = input_id



class Character(Enum):
    NONE = 0
    INVALID = 1
    ZETTERBURN = 2
    ORCANE = 3
    WRASTOR = 4
    KRAGG = 5
    FORSBURN = 6
    MAYPUL = 7
    ABSA = 8
    ETALUS = 9
    ORI = 10
    RANNO = 11
    CLAIREN = 12

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print ("You must include a file.")
    elif(len(sys.argv) > 2):
        for i, arg in enumerate(sys.argv):
            if(i != 0):
                parser(arg)
    else:
        parser(sys.argv[1])
