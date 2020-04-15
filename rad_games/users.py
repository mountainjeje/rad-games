import xml.etree.ElementTree as ET
import subprocess

def checkUser(sender):

    userdata = []
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()

    for user in dataRoot.findall('user'):
        if(sender == user.find('phone').text):
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
        writeData('game/inventory', msgcontent.split()[1], userdata)
        sendMsg('L objet ' + msgcontent.split()[1] + ' est dans l inventaire', userdata)
    elif msgcontent.split()[0] in ('voir', 'Voir') and len(msgcontent.split())>1:
        if msgcontent.split()[1] in ('inventaire', 'Inventaire'):
            itemlist = []
            for items in readData('game/inventory', userdata).split(';'):
                itemlist.append(items.split(',')) 
            sendMsg('Inventaire : ' + str(itemlist), userdata)
            print(itemlist)
    else:
        sendMsg('Rien compris mon pote', userdata)
        return 'Unknown command'
    return 'Message processed'

def writeData(elmnt, data, userdata):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    for element in dataRoot.findall('user'):
        if(userdata[2] == element.find('phone').text):
            subelement = element.find(elmnt)
            subelement.text = data
            break
    dataTree.write('users.xml')
    return

def readData(elmnt, userdata):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    for element in dataRoot.findall('user'):
        if element.get('phone') == userdata[2]:
            return element.find(elmnt).text
        break
    else:
        return False

def freeSlot(itemlist):
    #itemlist = []
    #for items in storage.split(';'):
    #    itemlist.append(items.split(',')) 
    #print(itemlist)
    for i in range(len(itemlist)):
        #print(itemlist[i])
        #print(itemlist[i][0])
        if itemlist[i][0] == '0':
            return i
    else:
        return False

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
    elif not userdata:
        print('Unknown user')
