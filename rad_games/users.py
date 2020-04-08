import xml.etree.ElementTree as ET
import subprocess

def checkUser(sender):

    data = []

    dataTree = ET.parse('users.xml')
    dataRoot = dataTree.getroot()

    for user in dataRoot.findall('user'):
        if(sender == user.find('phone').text):
            data.append(user.find('name').text)
            data.append(user.find('level').text)
            data.append(sender)
            #subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Salut " + name + "!\'", shell=True)
            break
    else:
        #subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Salut, tu peux t'enregistrer en renvoyant ton nom\'", shell=True)
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
    return data

oldmsgdate = ''
messageRoot = ET.fromstring(subprocess.check_output("./hilink.sh get_sms", shell=True))
for message in messageRoot.findall('Messages/Message'):
    sender = message.find('Phone').text
    msgcontent = message.find('Content').text
    msgdate = message.find('Date').text

if (msgdate != oldmsgdate): 
    data = checkUser(sender)
    print(data)


