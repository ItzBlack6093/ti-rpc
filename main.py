from PyMemoryEditor import OpenProcess
from pypresence import Presence
import time
import math

client_id = 1307579689522434078
RPC = Presence(client_id)
RPC.connect()

isGameDetected = 0

modeAddress = 0x4AE32A
modAddress = 0x4AE32C
levelAddress = 0x4AE300
sectionAddress = 0x4ACD8A
sakuraStageAddress = 0x4AE331
framesAddress = 0x4AE33C

def getModName(value):  # technically Big Master is the only one that being used. but if you modify 0x4AE32C, you can do weird stuff like 20G Shirase(?) and Big Sakura
    match value:
        case 1:
            return '20G'
        case 2:
            return 'Big'
        case 8:
            return 'TLS'
        case _:
            return ''

def getModeName(value):
    match value:
        case 1:
            return 'Easy'
        case 2:
            return 'Master'
        case 32:
            return 'Shirase'
        case 64:
            return 'Sakura'
        case 514:
            return 'Promotional Exam'
        case 4098:
            return 'Demotional Exam'
        case 16386:
            return 'Versus'
        case 16416:
            return 'Shirase Versus'
        case 258:
            return 'Attract Screen'
        case _:
            return 'Nothing'    
        
def getModeKey(value):
    match value:
        case 1:
            return 'easy'
        case 2:
            return 'master'
        case 32:
            return 'shirase'
        case 64:
            return 'sakura'
        case 514:
            return 'qualify'
        case 4098:
            return 'demotional'
        case _:
            return 'logo'

def getSakuraStage(value):
    stage = value % 256 + 1
    clearedStage = math.floor(value / 256)
    if stage > 20:
        return "EX" + str(stage - 20)
    return stage

def getBackground(mode, section):
    match mode:
        case 1:
            return min(100, section * 100)
        case 16386:
            return 1000
        case 16416:
            return 1000
        case _:
            return min(900, section * 100)
while True:
    try:
        with OpenProcess(process_name = "game.exe") as process:
            if isGameDetected != 1:
                print('Detected game.exe')
                isGameDetected = 1

            modeValue = process.read_process_memory(modeAddress, int, 2)
            modValue =  process.read_process_memory(modAddress, int, 2)
            level = process.read_process_memory(levelAddress, int, 2)
            section = process.read_process_memory(sectionAddress, int, 2)
            frames = process.read_process_memory(framesAddress, int, 2)

            state = 'Playing'

            if modeValue == 64:
                sakuraLevelValue = process.read_process_memory(sakuraStageAddress, int, 2)
                state = "Stage " + str(getSakuraStage(sakuraLevelValue))
            if frames == 0 or modeValue == 258: # attract mode shouldn't count as 'play'
                state = 'Not playing'

            RPC.update(
                state = state,
                details = getModName(modValue) + " " + getModeName(modeValue),
                small_image = getModeKey(modeValue),
                large_image = str(getBackground(modeValue, section)) + 's',
            )
    except:
        if isGameDetected == 0:
            print('An error occured. Did you open game.exe?')
            isGameDetected = -1
        elif isGameDetected == 1:
            print('game.exe closed')
            isGameDetected = -1
    time.sleep(0.5)

