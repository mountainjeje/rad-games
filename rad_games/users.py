import xml.etree.ElementTree as ET
import subprocess

def checkUser(sender):

    userdata = []
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()

    for user in dataRoot.findall('user'):
        if user.get('phone') == sender:
            userdata.append(user.find('name').text)
            userdata.append(user.find('level').text)
            userdata.append(sender)
            break
    else:
        userdata = False
    return userdata
    
def registerUser(sender):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    
    newuser = ET.Element("user")
    ET.SubElement(newuser, "name")
    for name in newuser.iter('name'):
        name.text = 'New user'
    ET.SubElement(newuser, "phone")
    for phone in newuser.iter('phone'):
        phone.text = sender
    ET.SubElement(newuser, "level")
    for level in newuser.iter('level'):
        level.text = "1"
    dataRoot.append(newuser)
    dataTree.write('users.xml')
    print('New user!')
    return ('New user', '1', sender)

def sendMsg(message, userdata, recipient=0): #if userdata='None' add recipient
    if not recipient:
        recipient = userdata[2]
    if(int(userdata[1]) < 2):
        subprocess.check_output("./hilink.sh send_sms \'" + recipient + "\' \'" + message + "\'", shell=True)
        print ('Message sent')
    else:
        print('Not allowed')
    return

def processMsg(msgcontent, userdata):
    if msgcontent.split()[0] in ('nom', 'Nom') and len(msgcontent.split())>1:
        writeData('name', msgcontent.split()[1], userdata)
        sendMsg('Tu es enregistre en tant que : ' + msgcontent.split()[1], userdata)
    elif msgcontent.split()[0] in ('prendre', 'Prendre') and len(msgcontent.split())>1:
        freeslot = freeSpace('game/inventory/slot', userdata)
        print(freeslot)
        #if freeslot:
        #    writeData('game/inventory/slot' + str(freeslot), msgcontent.split()[1], userdata)
        #    sendMsg('L objet ' + msgcontent.split()[1] + ' est dans l inventaire', userdata)
        #else:
            #sendMsg('Inventaire plein!', userdata)
    #elif msgcontent.split()[0] in ('voir', 'Voir') and len(msgcontent.split())>1:
        #if msgcontent.split()[1] in ('inventaire', 'Inventaire'):
            #itemlist = strToList(readData('game/inventory', userdata).split(';'))
            #sendMsg('Inventaire : ' + str(itemlist), userdata)
            #print(itemlist)
    else:
        sendMsg('Rien compris mon pote', userdata)
        return 'Unknown command'
    return 'Message processed'

def writeData(element, data, userdata):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    for user in dataRoot.findall('user'):
        if user.get('phone') == userdata[2]:
            user.find(element).text = data
            break
    dataTree.write('users.xml')
    return

def readData(element, userdata):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    for user in dataRoot.findall('user'):
        if user.get('phone') == userdata[2]:
            return user.find(element).text
    else:
        return False

def freeSpace(element, userdata):
    i=0
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    for user in dataRoot.findall('user'):
        if user.get('phone') == userdata[2]:
            for slot in user.findall(element):
                if not slot.text:
                    return i
                i=i+1
            return False
    else:
        return False

def strToList(string):
    itemlist = []
    for items in readData('game/inventory', userdata).split(';'):
        itemlist.append(items.split(',')) 
    return itemlist

oldmsgdate = ''
messageRoot = ET.fromstring(subprocess.check_output("./hilink.sh get_sms", shell=True))
for message in messageRoot.findall('Messages/Message'):
    sender = message.find('Phone').text
    msgcontent = message.find('Content').text
    msgdate = message.find('Date').text

if (msgdate != oldmsgdate): 
    userdata = checkUser(sender)
    if userdata:
        reply = processMsg(msgcontent, userdata)
        print(reply)
    elif not userdata and msgcontent in ('Yo Rad!', 'Yo Rad !'):
        userdata = registerUser(sender)
        sendMsg('Tu peux t enregistrer en envoyant : Nom ton_nom (ex : Nom Rad)', userdata, sender)
    else:
        print('Unknown user')
