import xml.etree.ElementTree as ET

dataTree = ET.parse('users.xml')
dataRoot = dataTree.getroot()
for user in dataRoot.findall('user'):
        game = ET.Element('game')
        inventory = ET.SubElement(game, 'inventory')
        for i in range(3):
            slot = ET.SubElement(inventory, 'slot')
        chest = ET.SubElement(game, 'chest')
        for i in range(8):
            slot = ET.SubElement(chest, 'slot')
        user.append(game)
        print('yo')
dataTree.write('users.xml')
