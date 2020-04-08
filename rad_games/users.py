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
        newuser = ET.Element("user")
        ET.SubElement(newuser, "name")
        for newname in newuser.iter('name'):
            newname.text = 'New user'
        ET.SubElement(newuser, "phone")
        for number in newuser.iter('phone'):
            number.text = sender
        ET.SubElement(newuser, "level")
        for level in newuser.iter('level'):
            level.text = "2"
        dataRoot.append(newuser)
        dataTree.write('users.xml')
        print('New user!')
    return userdata

def sendMsg(recipient, message, userdata):
    if userdata[1] in {'1', '0'}:
        #subprocess.check_output("./hilink.sh send_sms \'" + recipient + "\' \'" + message "\'", shell=True)
        print ('msg sent')
    else:
        print('not allowed')
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
    #reply = processMsg(msgcontent, userdata)
    sendMsg(sender, 'Hello world', userdata)
