import xml.etree.ElementTree as ET
import subprocess
import time

def checkUser(sender):

    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()

    for user in dataRoot.findall('user'):
        if user.get('phone') == sender:
            return user.get('userid')
    else:
        return False
    
def registerUser(sender):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    usercount = 0

    for user in dataRoot.findall('user'):
        usercount=usercount+1

    newuser = ET.Element("user")
    newuser.set('phone', sender)
    newuser.set('userid', str(usercount))
    name = ET.SubElement(newuser, "name")
    name.text = 'Rad Junior'
    level = ET.SubElement(newuser, "level")
    level.text = "1"
    game = ET.SubElement(newuser, "game")
    inventory = ET.SubElement(game, "inventory")
    for i in range(3):
        slot = ET.SubElement(inventory, 'slot')
    chest = ET.SubElement(game, "chest")
    for i in range(8):
        slot = ET.SubElement(chest, 'slot')
    dataRoot.append(newuser)
    dataTree.write('users.xml')
    print('New user!')
    return (usercount)

def sendMsg(message, userid, recipient=0): #if userid='None' add recipient
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    if not recipient:
        recipient = dataRoot[int(userid)].get("phone")
    subprocess.check_output("./hilink.sh send_sms \'" + recipient + "\' \'" + message + "\'", shell=True)
    print ('Message sent')
    return

def processMsg(msgcontent, userid):
    if msgcontent.split()[0] in ('nom', 'Nom') and len(msgcontent.split())>1:
        writeData('name', msgcontent.split()[1], userid)
        sendMsg('Tu es enregistre en tant que : ' + msgcontent.split()[1], userid)
    elif msgcontent.split()[0] in ('nom', 'Nom') and len(msgcontent.split())==1:
        sendMsg('Tu es enregistre en tant que : ' + readData('name', userid), userid)
    elif msgcontent.split()[0] in ('prendre', 'Prendre') and len(msgcontent.split())>1:
        freeslot = freeSpace('game/inventory/slot', userid)
        if freeslot in range(3):
            writeData('game/inventory', msgcontent.split()[1], userid, 'slot', freeslot)
            sendMsg('L objet ' + msgcontent.split()[1] + ' est dans l inventaire', userid)
        else:
            sendMsg('Inventaire plein!', userid)
    elif msgcontent.split()[0] in ('voir', 'Voir') and len(msgcontent.split())>1:
        if msgcontent.split()[1] in ('inventaire', 'Inventaire'):
            itemlist = readData('game/inventory/slot', userid, 'slot')
            sendMsg('Inventaire : ' + str(itemlist), userid)
            print(itemlist)
    else:
        sendMsg('Rien compris mon pote', userid)
        return 'Unknown command'
    return 'Message processed'

def writeData(element, data, userid, mode=False, slot=0, freeslot=0):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    if not mode:
        dataRoot[int(userid)].find(element).text = data
        dataTree.write('users.xml')
        return True
    if mode == 'slot':
        storage = dataRoot[int(userid)].find(element)
        storage[int(slot)].text = data
        dataTree.write('users.xml')
        return True
    else:
        return False

def readData(element, userid, mode='normal'):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    if mode == 'normal':
        return dataRoot[int(userid)].find(element).text
    if mode == 'slot':
        itemlist = []
        for slot in dataRoot[int(userid)].findall(element):
            itemlist.append(slot.text)
        return itemlist
    else:
        return False

def freeSpace(element, userid):
    i=0
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    for slot in dataRoot[int(userid)].findall(element):
        if not slot.text:
            return i
        i=i+1
    else:
        return 'no space'

def strToList(string):
    itemlist = []
    for items in readData('game/inventory', userdata).split(';'):
        itemlist.append(items.split(',')) 
    return itemlist

oldmsgdate = ''
while True:
    messageRoot = ET.fromstring(subprocess.check_output("./hilink.sh get_sms", shell=True))
    for message in messageRoot.findall('Messages/Message'):
        sender = message.find('Phone').text
        msgcontent = message.find('Content').text
        msgdate = message.find('Date').text

    if (msgdate != oldmsgdate): 
        oldmsgdate = msgdate
        userid = checkUser(sender)
        if userid:
            reply = processMsg(msgcontent, userid)
            print(reply)
        elif not userid and msgcontent in ('Yo Rad!', 'Yo Rad !'):
            userid = registerUser(sender)
            sendMsg('Bienvenue dans Rad Games!', userid, sender)
            print(userid)
        else:
            print('Unknown user')
    time.sleep(10)
