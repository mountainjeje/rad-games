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

def sendMsg(recipient, message, userdata):
    if(int(userdata[1]) < 2):
        subprocess.check_output("./hilink.sh send_sms \'" + recipient + "\' \'" + message + "\'", shell=True)
        print ('msg sent')
    else:
        print('Not allowed')
    return

oldmsgdate = ''
messageRoot = ET.fromstring(subprocess.check_output("./hilink.sh get_sms", shell=True))
for message in messageRoot.findall('Messages/Message'):
    sender = message.find('Phone').text
    msgcontent = message.find('Content').text
    msgdate = message.find('Date').text

if (msgdate != oldmsgdate): 
    userdata = checkUser(sender)
    print(userdata)
    #we first check if user wants to upgrade to level 1 and receive msgs from rad
    if not userdata and msgcontent in ('Yo Rad!', 'Yo Rad !'):
        userdata = registerUser(sender)
    elif not userdata:
        print('Unknown user')
    print(userdata)
    #reply = processMsg(msgcontent, userdata)
    #sendMsg(sender, 'Hello world', userdata)
