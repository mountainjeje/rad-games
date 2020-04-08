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

def sendMsg(message, userdata, recipient=0):
    if not recipient:
        recipient = userdata[2]
    if(int(userdata[1]) < 2):
        subprocess.check_output("./hilink.sh send_sms \'" + recipient + "\' \'" + message + "\'", shell=True)
        print ('msg sent')
    else:
        print('Not allowed')
    return

def processMsg(msgcontent, userdata):
    reply = 'Message processed'
    if msgcontent.split()[0] in ('rg', 'Rg', 'RG'):
        writeData('name', msgcontent.split()[1], userdata)
        sendMsg('Tu es enregistre en tant que : ' + msgcontent.split()[1], userdata)
    else:
        reply = 'Unknown command'
    return reply

def writeData(elmnt, data, userdata):
    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()
    for element in dataRoot.findall('user'):
        if(userdata[2] == element.find('phone').text):
            for subelement in element.iter(elmnt):
                subelement.text = data
            break
    dataTree.write('users.xml')
    return

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
        sendMsg('Tu peux t enregistrer en envoyant : rg ton_nom', userdata, sender)
    elif not userdata:
        print('Unknown user')
