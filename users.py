import xml.etree.ElementTree as ET
import subprocess

knownsender = False
name = "None"

dataTree = ET.parse('contacts.xml')
dataRoot = dataTree.getroot()

messageRoot = ET.fromstring(subprocess.check_output("./hilink.sh get_sms", shell=True))
for message in messageRoot.findall('Messages/Message'):
    sender = message.find('Phone').text
    print(sender)

for contact in dataRoot.findall('contact'):
    if(sender == contact.find('number').text):
        knownsender = True
        name = contact.find('name').text
        #subprocess.check_output("./hilink.sh send_sms \'" + sender + "\' \'Salut " + name + "!\'", shell=True)
        print(name)

if not knownsender:
    #subprocess.check_output("./hilin.sh send_sms \'" + sender + "\' \'Salut, tu peux t'enregistrer en renvoyant ton nom\'", shell=True)
    newcontact = ET.Element("contact")
    ET.SubElement(newcontact, "name")
    ET.SubElement(newcontact, "number")
    for number in newcontact.iter('number'):
        number.text = sender
    ET.SubElement(newcontact, "level")
    for level in newcontact.iter('level'):
        level.text = "1"
    ET.dump(newcontact)
    dataRoot.append(newcontact)
    dataTree.write('contacts.xml')
    print('New user!')
