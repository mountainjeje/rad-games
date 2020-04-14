import xml.etree.ElementTree as ET

dataTree = ET.parse('users.xml')
dataRoot = dataTree.getroot()
for element in dataRoot.findall('user'):
    if('123' == element.get('phone')):
        inventory = element.find('game/inventory')
        #game = element.find('game')
        #game = ET.Element('game')
        #inventory = ET.SubElement(game, 'inventory')
        #for items in game.iter('inventory'):
        inventory.text = '(1,1), (0,0), (0,0)'
        #element.append(inventory)
        print('yo')
        break
dataTree.write('users.xml')
