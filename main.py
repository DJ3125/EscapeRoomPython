playerProperties = {
    'Path': "",
    'Inventory': [],
    'Events': [],
    'Turns': 0,
    'eggs': 0,
}
minigames = {
    'sedate': {
        'dinosaurs': {
            'types': ['dilo', 'raptor', 'rex'],
            'attacks': [],
            'predictions': {
                'predictionsL': [],
                'predictionsN': [],
            },
            'dinosleft': 0
        },
        'Meat': [],
        'player': {
            'lastloc': '',
            'Lives': 3,
            'location': '',
            'direction': '',
            'attacks': [],
        },
        'grid': {
            'letters': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            'numbers': [],
        }
    },
    'radio': {
        'frequency': 0,
    },
}
status = {
    'power': False,
    'fences': False,
}
obstacles = {
    'CarNumb': 0,
    'powercode': '',
}
locations = {
    'helipad': '',
}
dinosaurs = {
    'dilo': {
        'locked': False,
        'location': '',
        'sedated': False,
    },
    'raptor': {
        'locked': False,
        'location': '',
        'sedated': False,
    },
    'rex': {
        'locked': False,
        'location': '',
        'sedated': False,
    }
}
colors = {
    'black': '\033[0;30m',
    'red': '\033[0;31m',
    'green': '\033[0;32m',
    'blue': '\033[0;33m',
    'yellow': '\033[0;34m',
    'purple': '\033[0;35m',
    'white': '\033[0;37m',
    'base': '\033[0m',
}


def randdino(dino):
    proceed = False
    new = ''
    while not proceed:
        new = randsector()
        proceed = True
        for i in minigames['sedate']['dinosaurs']['types']:
            if dinosaurs[i]['location'] == new:
                proceed = False
        if locations['helipad'] == new:
            proceed = False
    dinosaurs[dino]['location'] = new


def changes():
    import random
    playerProperties['Turns'] += 1
    if playerProperties['Turns'] % 10 == 1:
        if not dinosaurs['dilo']['locked']:
            randdino('dilo')
        if not dinosaurs['raptor']['locked']:
            randdino('raptor')
        if not dinosaurs['rex']['locked']:
            randdino('rex')
    available = []
    for i in minigames['sedate']['dinosaurs']['types']:
        if not dinosaurs[i]['locked']:
            available.append(i)
    if len(minigames['sedate']['Meat']) > 0 and len(available) > 0:
        select = available[random.randint(0, len(available) - 1)]
        meat = minigames['sedate']['Meat'][random.randint(0, len(minigames['sedate']['Meat']) - 1)]
        dinosaurs[select]['location'] = meat
        dinosaurs[select]['locked'] = True
        minigames['sedate']['Meat'].remove(meat)


def initialize():
    import random
    obstacles['CarNumb'] = random.randint(1, 100)
    minigames['radio']['frequency'] = random.randint(1, 100)
    for i in range(5):
        obstacles['powercode'] = obstacles['powercode'] + str(random.randint(0, 9))
    locations['helipad'] = randsector()


def attack(letter, n, usedby):
    if letter > (len(minigames['sedate']['grid']['letters']) - 1) or letter < 0 or n not in minigames['sedate']['grid']['numbers']:
        return True
    else:
        if usedby == 'dino':
            minigames['sedate']['dinosaurs']['attacks'].append(minigames['sedate']['grid']['letters'][letter] + n)
        elif usedby == 'player':
            minigames['sedate']['player']['attacks'].append(minigames['sedate']['grid']['letters'][letter] + n)
        return False


def attacks(dinotype, *dinos):
    for i in dinos[0]:
        if dinotype == 'dilo':
            proceed = False
            count = 1
            while not proceed:
                if i['direction'] == 'right':
                    proceed = attack(minigames['sedate']['grid']['letters'].index(i['location'][0]), str(int(i['location'][1]) + count), 'dino')
                elif i['direction'] == 'left':
                    proceed = attack(minigames['sedate']['grid']['letters'].index(i['location'][0]), str(int(i['location'][1]) - count), 'dino')
                elif i['direction'] == 'down':
                    proceed = attack(minigames['sedate']['grid']['letters'].index(i['location'][0]) + count, i['location'][1], 'dino')
                elif i['direction'] == 'up':
                    proceed = attack(minigames['sedate']['grid']['letters'].index(i['location'][0]) - count, i['location'][1], 'dino')
                count += 1
        elif dinotype == 'raptor':
            raptorandhumanattack('dino', i['direction'], i['location'])
        elif dinotype == 'rex':
            for a in range(2):
                for j in range(3):
                    attack(minigames['sedate']['grid']['letters'].index(i['location'][0]) - 1 + a*2, str(int(i['location'][1]) - 1 + j), 'dino')
                    attack(minigames['sedate']['grid']['letters'].index(i['location'][0]) - 1 + j, str(int(i['location'][1]) - 1 + a*2), 'dino')


def setdino(dinotype, *others):
    import random
    import math
    directions = ['up', 'down', 'left', 'right']
    dino = {
        'location': minigames['sedate']['dinosaurs']['predictions']['predictionsL'][random.randint(0, len(minigames['sedate']['dinosaurs']['predictions']['predictionsL']) - 1)] + minigames['sedate']['dinosaurs']['predictions']['predictionsN'][random.randint(0, len(minigames['sedate']['dinosaurs']['predictions']['predictionsN']) - 1)],
    }
    # if dinotype == 'raptor':
        # dino['location'] = minigames['sedate']['dinosaurs']['predictions']['predictionsL'][int(math.cos(math.pi*random.randint(0, 1))) + random.randint(1, len(minigames['sedate']['dinosaurs']['predictions']['predictionsL']) - 2)] + minigames['sedate']['dinosaurs']['predictions']['predictionsN'][int(math.cos(math.pi*random.randint(0, 1))) + random.randint(1, len(minigames['sedate']['dinosaurs']['predictions']['predictionsN']) - 2)]
    proceed = False
    while not proceed:
        # if dinotype == 'raptor':
        #     dino['location'] = minigames['sedate']['dinosaurs']['predictions']['predictionsL'][int(math.cos(math.pi*random.randint(0, 1))) + random.randint(1, len(minigames['sedate']['dinosaurs']['predictions']['predictionsL']) - 2)] + minigames['sedate']['dinosaurs']['predictions']['predictionsN'][int(math.cos(math.pi*random.randint(0, 1))) + random.randint(1, len(minigames['sedate']['dinosaurs']['predictions']['predictionsN']) - 2)]
        # else:
        proceed = True
        dino['location'] = minigames['sedate']['dinosaurs']['predictions']['predictionsL'][random.randint(0, len(minigames['sedate']['dinosaurs']['predictions']['predictionsL']) - 1)] + minigames['sedate']['dinosaurs']['predictions']['predictionsN'][random.randint(0, len(minigames['sedate']['dinosaurs']['predictions']['predictionsN']) - 1)]
        for i in others[0]:
            if i['location'] == dino['location']:
                proceed = False
    if dino['location'][0] == 'A':
        directions.remove('up')
    elif dino['location'][0] == minigames['sedate']['grid']['letters'][len(minigames['sedate']['grid']['letters'])-1]:
        directions.remove('down')
    if dino['location'][1] == '1':
        directions.remove('left')
    elif dino['location'][1] == minigames['sedate']['grid']['numbers'][len(minigames['sedate']['grid']['numbers'])-1]:
        directions.remove('right')
    dino['direction'] = directions[random.randint(0, len(directions)-1)]
    return dino


def raptorandhumanattack(usedby, facing, loc):
    for a in range(3):
        if facing == 'right':
            attack(minigames['sedate']['grid']['letters'].index(loc[0]) - 1 + a, str(int(loc[1]) + 1), usedby)
        elif facing == 'left':
            attack(minigames['sedate']['grid']['letters'].index(loc[0]) - 1 + a, str(int(loc[1]) - 1), usedby)
        elif facing == 'down':
            attack(minigames['sedate']['grid']['letters'].index(loc[0]) + 1, str(int(loc[1]) - 1 + a), usedby)
        elif facing == 'up':
            attack(minigames['sedate']['grid']['letters'].index(loc[0]) - 1, str(int(loc[1]) - 1 + a), usedby)


def getsect():
    sectors = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    numbers = []
    for i in range(1, 8):
        numbers.append(str(i))
    for i in numbers:
        for j in letters:
            sectors.append(j.upper() + i)
    return sectors


def randsector():
    import random
    sectors = getsect()
    return sectors[random.randint(0, len(sectors)-1)]


def hunt(dinosaur):
    dinos = []
    for i in range(minigames['sedate']['dinosaurs']['dinosleft']):
        dinos.append(setdino(dinosaur, dinos))
    minigames['sedate']['dinosaurs']['attacks'].clear()
    minigames['sedate']['player']['attacks'].clear()
    attacks(dinosaur, dinos)
    proceed = False
    subsectors = []
    for i in minigames['sedate']['grid']['letters']:
        for j in minigames['sedate']['grid']['numbers']:
            subsectors.append(i+j)
    minigames['sedate']['player']['lastloc'] = minigames['sedate']['player']['location']
    while not proceed:
        choice = input('What sub-sector do you want to go to, or do you want to abort?')
        choice = choice.strip().lower()
        if choice == 'abort':
            if not dinosaurs[dinosaur]['locked']:
                randdino(dinosaur)
            return True
        elif choice.upper() in subsectors:
            choice = choice.upper()
            if minigames['sedate']['player']['location'] == minigames['sedate']['player']['lastloc']:
                print('You chose to stay in sub-sector ' + choice)
            else:
                print('You choose to move to sub-sector ' + choice)
            minigames['sedate']['player']['location'] = choice
            proceed = True
        else:
            print('That\'s not a valid sub-sector')
    proceed = False
    directions = ['up', 'down', 'left', 'right']
    while not proceed:
        for i in directions:
            print(i)
        choice = input('What direction do you want to face, or do you want to abort?')
        choice = choice.strip().lower()
        if choice == 'abort':
            if not dinosaurs[dinosaur]['locked']:
                randdino(dinosaur)
            return True
        elif choice in directions:
            print('You chose to face ' + choice)
            minigames['sedate']['player']['direction'] = choice
            proceed = True
        else:
            print('That\'s not a valid direction')
    if 'rested' in playerProperties['Events']:
        raptorandhumanattack('player', minigames['sedate']['player']['direction'], minigames['sedate']['player']['location'])
    else:
        if minigames['sedate']['player']['direction'] == 'right':
            attack(minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0]), minigames['sedate']['grid']['numbers'][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1]) + 1], 'player')
        elif minigames['sedate']['player']['direction'] == 'left':
            attack(minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0]), minigames['sedate']['grid']['numbers'][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1]) - 1], 'player')
        elif minigames['sedate']['player']['direction'] == 'down':
            attack(minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0]) + 1, minigames['sedate']['grid']['numbers'][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1])], 'player')
        elif minigames['sedate']['player']['direction'] == 'up':
            attack(minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0]) - 1, minigames['sedate']['grid']['numbers'][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1])], 'player')
    if minigames['sedate']['player']['lastloc'] == minigames['sedate']['player']['location'] and dinosaur == 'rex':
        minigames['sedate']['dinosaurs']['attacks'].clear()
    UI = []
    for i in range(len(minigames['sedate']['grid']['letters'])):
        x = []
        for j in range(len(minigames['sedate']['grid']['numbers'])):
            x.append('O')
        UI.append(x)
    for i in minigames['sedate']['dinosaurs']['attacks']:
        UI[minigames['sedate']['grid']['letters'].index(i[0])][minigames['sedate']['grid']['numbers'].index(i[1])] = 'X'
    for i in minigames['sedate']['player']['attacks']:
        UI[minigames['sedate']['grid']['letters'].index(i[0])][minigames['sedate']['grid']['numbers'].index(i[1])] = '#'
    for i in dinos:
        if i['direction'] == 'right':
            UI[minigames['sedate']['grid']['letters'].index(i['location'][0])][minigames['sedate']['grid']['numbers'].index(i['location'][1])] = '>'
        elif i['direction'] == 'left':
            UI[minigames['sedate']['grid']['letters'].index(i['location'][0])][minigames['sedate']['grid']['numbers'].index(i['location'][1])] = '<'
        elif i['direction'] == 'up':
            UI[minigames['sedate']['grid']['letters'].index(i['location'][0])][minigames['sedate']['grid']['numbers'].index(i['location'][1])] = '^'
        elif i['direction'] == 'down':
            UI[minigames['sedate']['grid']['letters'].index(i['location'][0])][minigames['sedate']['grid']['numbers'].index(i['location'][1])] = 'v'
    if minigames['sedate']['player']['direction'] == 'right':
        UI[minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0])][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1])] = '→'
    elif minigames['sedate']['player']['direction'] == 'left':
        UI[minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0])][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1])] = '←'
    elif minigames['sedate']['player']['direction'] == 'up':
        UI[minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0])][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1])] = '↑'
    elif minigames['sedate']['player']['direction'] == 'down':
        UI[minigames['sedate']['grid']['letters'].index(minigames['sedate']['player']['location'][0])][minigames['sedate']['grid']['numbers'].index(minigames['sedate']['player']['location'][1])] = '↓'
    text = '    '
    for i in minigames['sedate']['grid']['numbers']:
        text = text + i + '  '
    text = '\u0332'.join(text)
    print(text)
    for i in range(len(UI)):
        txt = minigames['sedate']['grid']['letters'][i] + ' | '
        for j in UI[i]:
            txt = txt + j + '  '
        print((((((((((((txt.replace('O', colors['green'] + 'O' + colors['base'])).replace('X', colors['red'] + 'X' + colors['base'])).replace('#', colors['purple'] + '#' + colors['base'])).replace('^', colors['blue'] + '^' + colors['base'])).replace('<', colors['blue'] + '<' + colors['base'])).replace('v', colors['blue'] + 'v' + colors['base'])).replace('>', colors['blue'] + '>' + colors['base'])).replace('↓', colors['white'] + '↓' + colors['base'])).replace('→', colors['white'] + '→' + colors['base'])).replace('←', colors['white'] + '←' + colors['base'])).replace('↑', colors['white'] + '↑' + colors['base'])))
    if minigames['sedate']['player']['location'] in minigames['sedate']['dinosaurs']['attacks']:
        minigames['sedate']['player']['Lives'] -= 1
        print('You are attacked by the dinosaur. You have ' + str(minigames['sedate']['player']['Lives']) + ' lives left')
    else:
        for i in range(len(dinos)):
            if dinos[i]['location'] in minigames['sedate']['player']['attacks']:
                minigames['sedate']['dinosaurs']['dinosleft'] -= 1
                print('You sedated a Dino! You have ' + str(minigames['sedate']['dinosaurs']['dinosleft']) + ' dinos left to sedate')
            elif dinos[i]['location'] == minigames['sedate']['player']['location']:
                minigames['sedate']['dinosaurs']['dinosleft'] -= 1
                print('You landed right on top of a dino and sedated it! You have ' + str(minigames['sedate']['dinosaurs']['dinosleft']) + ' dinos left to sedate')
    if minigames['sedate']['player']['Lives'] == 0:
        input('you have no lives left. You have to abort the mission. Press enter to continue')
        if not dinosaurs[dinosaur]['locked']:
            randdino(dinosaur)
        return True
    elif minigames['sedate']['dinosaurs']['dinosleft'] == 0:
        input('You sedated all the dinos! Press anywhere to continue')
        dinosaurs[dinosaur]['sedated'] = True
        dinosaurs[dinosaur]['locked'] = True
        return True
    else:
        print('You are at ' + minigames['sedate']['player']['location'])
        txts = 'The dinos were at '
        for i in dinos:
            txts = txts + i['location'] + ','
        print(txts)
        print('Theres still more dinosaurs to sedate. You need to keep looking')
        minigames['sedate']['dinosaurs']['predictions']['predictionsL'].append(minigames['sedate']['player']['location'][0])
        minigames['sedate']['dinosaurs']['predictions']['predictionsN'].append(minigames['sedate']['player']['location'][1])


def hunting(dino):
    txt = 'you have found the {} in this sector. Do you want to pursue? y/n'
    choice = input(txt.format(dino))
    choice = choice.strip().lower()
    if choice == 'y' or choice == 'yes':
        minigames['sedate']['player']['Lives'] = 3
        print('This is how the grid will look like:')
        minigames['sedate']['grid']['numbers'].clear()
        minigames['sedate']['dinosaurs']['predictions']['predictionsN'].clear()
        minigames['sedate']['dinosaurs']['predictions']['predictionsL'].clear()
        for i in range(1, 8):
            minigames['sedate']['grid']['numbers'].append(str(i))
            minigames['sedate']['dinosaurs']['predictions']['predictionsN'].append(str(i))
            minigames['sedate']['dinosaurs']['predictions']['predictionsL'].append(minigames['sedate']['grid']['letters'][i - 1])
        text = '    '
        for i in minigames['sedate']['grid']['numbers']:
            text = text + i + '  '
        text = '\u0332'.join(text)
        print(text)
        for i in minigames['sedate']['grid']['letters']:
            txt = i + ' | '
            for j in minigames['sedate']['grid']['numbers']:
                txt = txt + 'O  '
            print(txt)
        print(
            'Each \"O\" represents a subsector. For example, subsector A1 would be the \"O\" in the first row and column')
        print('the dinosaur will appear in one of these subsectors, which is represented by an arrow.')
        print('The arrow will face in a specific direction, showing what direction the dinosaur will direct its attacks')
        print('Each dino has specific abilities and attacks, so keep it them in mind when you hunt')
        if dino == 'raptor':
            minigames['sedate']['dinosaurs']['dinosleft'] = 2
            print('The raptor will hunt in packs.')
        else:
            minigames['sedate']['dinosaurs']['dinosleft'] = 1
            if dino == 'rex':
                print('The rex can attack on all fronts. However, its VISION IS BASED ON MOVEMENT.')
            elif dino == 'dilo':
                print('The dilophosaurus can attack anything in its view.')
        print('The X symbols represent the dinosaurs attacks. The # symbols represent your attacks.')
        print('Your location is the arrow, while the dinosaurs location is the small arrow without a line.')
        while minigames['sedate']['dinosaurs']['dinosleft'] > 0:
            if hunt(dino):
                break
    else:
        print('You ran away.')


def traveling():
    proceed = False
    sectors = getsect()
    while not proceed:
        changes()
        go = False
        choice = ''
        while not go:
            print('-------------------------------------')
            print('Here are the Sectors:')
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
            for i in range(1, 8):
                txt = ''
                for j in letters:
                    txt = txt + ' ' + j.upper() + str(i) + ','
                print(txt)
            print('Visitor Center')
            print('Maintenance Shed')
            choice = input('Which sector do you want to travel to?')
            choice = choice.strip()
            if len(choice) == 2 or choice.lower() == 'visitor center' or choice.lower() == 'maintenance shed':
                go = True
        if choice.lower() == 'visitor center':
            proceed = True
            print('You go back to the front entrance of the visitor center.')
            playerProperties['Path'] = '1'
        elif choice.lower() == 'maintenance shed':
            if status['power']:
                print('You have no reason to be here. You already have the power on.')
            else:
                print('Your at the maintenance shed. As you venture in, you see the switch for the power. However, there is a 5 digit lock in order to turn on the power.')
                trying = True
                while trying:
                    choice1 = input('Enter the 5 digit code, or go back')
                    choice1 = choice1.strip().lower()
                    if choice1 == 'back':
                        trying = False
                        print('You give up and exit.')
                    elif choice1 == obstacles['powercode']:
                        print('You got the code for the power! The power is now on!')
                        status['power'] = True
                        blocked(False)
                        trying = False
                    else:
                        print('Incorrect code. Try again')
        else:
            choice = choice[0].upper() + choice[1]
            if choice in sectors:
                print('You picked sector ' + choice)
            if dinosaurs['dilo']['location'] == choice:
                if not dinosaurs['dilo']['sedated']:
                    hunting('dilo')
                else:
                    print('You come across the dilo. However, it\'s already sedated')
            elif dinosaurs['raptor']['location'] == choice:
                if not dinosaurs['raptor']['sedated']:
                    hunting('raptor')
                else:
                    print('You come across the raptors. However, they\'re already sedated')
            elif dinosaurs['rex']['location'] == choice:
                if not dinosaurs['rex']['sedated']:
                    hunting('rex')
                else:
                    print('You come across the rex. However, it\'s already sedated')
            elif locations['helipad'] == choice:
                if dinosaurs['dilo']['sedated'] and dinosaurs['raptor']['sedated'] and dinosaurs['rex']['sedated'] and status['fences'] and 'called' in playerProperties['Events']:
                    print('You escaped the island! Congrats!')
                    print('')
                    playerProperties['Events'].append('Win')
                    proceed = True
                else:
                    if not (dinosaurs['dilo']['sedated'] and dinosaurs['raptor']['sedated'] and dinosaurs['rex']['sedated']) and not status['fences']:
                        print('You still need to sedate the dinos and turn on the fences.')
                    elif not status['fences']:
                        print('You still need to turn on the fences.')
                    elif not (dinosaurs['dilo']['sedated'] and dinosaurs['raptor']['sedated'] and dinosaurs['rex']['sedated']):
                        print('You still need to sedate the carnivores.')
                    elif 'called' not in playerProperties['Events']:
                        print('You still need to call for help.')
            else:
                print('Theres nothing here.')
                if 'meat' in playerProperties['Inventory'] and choice not in minigames['sedate']['Meat']:
                    choice2 = input('Do you want to place meat here?y/n')
                    choice2 = choice2.strip().lower()
                    if choice2 == 'y' or choice2 == 'yes':
                        print('You cut some meat from the main slab and placed it on the ground.')
                        minigames['sedate']['Meat'].append(choice)
                elif choice in minigames['sedate']['Meat']:
                    print('There\'s no point in placing meat here since theres meat here already.')


def choices():
    if 'intro' in playerProperties['Events']:
        if playerProperties['Path'] == '':
            print('You\'re in the middle of the visitor center. The light shines brightly from the windows, illuminating the Tyrannosaur skeleton that looms overhead.')
            options = ['Explore the building', 'Go out the front door', 'Call for help']
            ask(options)
        else:
            if playerProperties['Path'][0] == '0':
                # exploring building
                if len(playerProperties['Path']) >= 2:
                    if playerProperties['Path'][1] == '0':
                        # control center
                        if 'card' in playerProperties['Inventory']:
                            if len(playerProperties['Path']) >= 3:
                                if playerProperties['Path'][2] == '0':
                                    print('You inspect the control center. The room is spacious and colored a semi-dark grey. Lights flash red. As you examine the computers, you see something of interest. On the computer, it says the power code is ' + obstacles['powercode'])
                                    blocked(False)
                                elif playerProperties['Path'][2] == '1':
                                    if len(playerProperties['Path']) >= 4:
                                        if playerProperties['Path'][3] == '0':
                                            if status['power']:
                                                proceed = False
                                                while not proceed:
                                                    txt = 'As you examine the computer, it asks, \"Do you want to turn the fence power {}? y/n\"'
                                                    if status['fences']:
                                                        x = input(txt.format('off'))
                                                    else:
                                                        x = input(txt.format('on'))
                                                    x = x.strip().lower()
                                                    if x == 'y' or x == 'yes':
                                                        status['fences'] = not status['fences']
                                                        txt = 'The computer beeps. You have turned the fences {}'
                                                        if not status['fences']:
                                                            print(txt.format('off'))
                                                        else:
                                                            print(txt.format('on'))
                                                        proceed = True
                                                    elif x == 'no' or x == 'n':
                                                        print('You cancel, and nothing happens.')
                                                        proceed = True
                                                blocked(False)
                                            else:
                                                print('As you examine the computer, you try and turn it on. However, as you try to do inspect, it gives you an error. Apparently, the fences nor the security systems work without power.')
                                                blocked(False)
                                        elif playerProperties['Path'][3] == '1':
                                            if status['power']:
                                                proceed = False
                                                while not proceed:
                                                    print('---------------------')
                                                    print('The computer gives you a list of targets.')
                                                    options = ['helipad', 'dilo', 'raptor', 'rex', 'back']
                                                    for i in options:
                                                        print(i.capitalize())
                                                    print('')
                                                    choice = input('What do you want to find?')
                                                    choice = choice.strip().lower()
                                                    if choice in options:
                                                        if choice == 'helipad':
                                                            print('The computer says:')
                                                            print('The helipad is at sector ' + locations['helipad'])
                                                        elif not options.index(choice) == options.index('back'):
                                                            print('The computer says:')
                                                            print('The ' + choice + ' is at sector ' + dinosaurs[choice]['location'])
                                                        else:
                                                            print('You do nothing and step away.')
                                                        proceed = True
                                                blocked(False)
                                            else:
                                                print('As you examine the computer, you try and turn it on. However, as you try to do inspect, it gives you an error. Apparently, the fences nor the security systems work without power.')
                                                blocked(False)
                                    else:
                                        print('You take a further look and inspect the computers responsible for security and the fences')
                                        options = ['Inspect Fence Power', 'Inspect Security']
                                        ask(options)
                            else:
                                print('As you approach the control center, you see that the room is blocked by a card lock. You slide your card through the slot and enter the control center')
                                options = ['Inspect', 'Restore Systems']
                                ask(options)
                        else:
                            print('As you approach the control center, you see that the room is blocked by a card lock. However, you do not have a key card.')
                            blocked(True)
                    elif playerProperties['Path'][1] == '1':
                        # lab
                        if 'card' in playerProperties['Inventory']:
                            if len(playerProperties['Path']) >= 3:
                                if playerProperties['Path'][2] == '0':
                                    print('As you enter the lab, you see pristine, sparkling equipment. There are many dino eggs everywhere, and there\'s a medical closet in the corner')
                                    blocked(False)
                                elif playerProperties['Path'][2] == '1':
                                    proceed = False
                                    while not proceed:
                                        choice = input('Do you want to grab meat or leaves?')
                                        choice = choice.strip().lower()
                                        if choice == 'meat':
                                            print('you grabbed the meat')
                                            playerProperties['Inventory'].append('meat')
                                            proceed = True
                                        elif choice == 'leaves':
                                            print('you grabbed the leaves')
                                            playerProperties['Inventory'].append('leaves')
                                            proceed = True
                                    blocked(False)
                                elif playerProperties['Path'][2] == '2':
                                    if playerProperties['eggs'] == 20:
                                        print('Cheat codes. Not actually tho lol, that\'s cheating.')
                                    else:
                                        playerProperties['eggs'] += 1
                                        print('You Tended to the Eggs')
                                    blocked(False)
                                elif playerProperties['Path'][2] == '3':
                                    if 'bullets' not in playerProperties['Inventory']:
                                        x = input('As you open the closet, you see tranquilizer bullets. Do you want to take it? y/n')
                                        x = (x.strip()).lower()
                                        if x == 'yes' or x == 'y':
                                            print('You grabbed the tranquilizer bullets')
                                            playerProperties['Inventory'].append('bullets')
                                    else:
                                        print('As you open the closet, you see it\'s empty. You already took the tranquilizer bullets.')
                                    blocked(False)
                            else:
                                print('As you approach the lab, you see that the room is blocked by a card lock. You slide your card through the slot and enter the lab')
                                options = ['Inspect', 'Get Dino Food', 'Tend to Eggs', 'Inspect The Medical Closet']
                                ask(options)
                        else:
                            print('As you approach the lab, you see that the room is blocked by a card lock. However, you do not have a key card.')
                            blocked(True)
                    elif playerProperties['Path'][1] == '2':
                        # garage
                        if len(playerProperties['Path']) >= 3:
                            if playerProperties['Path'][2] == '0':
                                print('You see boxes piled around. Ironically, there are no cars. They all seem to be taken.')
                                blocked(False)
                            elif playerProperties['Path'][2] == '1':
                                if 'gun' in playerProperties['Inventory']:
                                    print('As you open the closet, you see there\'s nothing there. You already took the tranquilizer gun')
                                    blocked(False)
                                else:
                                    x = input('As you open the closet, you see an empty tranquilizer gun. Do you want to take it? y/n')
                                    x = (x.strip()).lower()
                                    if x == 'yes' or x == 'y':
                                        print('You grabbed the tranquilizer gun and put it in your inventory.')
                                        playerProperties['Inventory'].append('gun')
                                    blocked(False)
                            elif playerProperties['Path'][2] == '2':
                                print('As you turn to you\'re left, you see a wall full of keys, labeled 1 through 100')
                                options = []
                                for i in range(1, 101):
                                    options.append(str(i))
                                proceed = False
                                while not proceed:
                                    choice = input('Which key do you choose, or do you want to go back?')
                                    choice = choice.strip()
                                    if choice.lower() == 'back':
                                        print('You leave the wall and go back into the middle of the garage.')
                                        proceed = True
                                    elif choice not in options:
                                        print('That\'s not a valid key.')
                                    elif str('K'+choice) in playerProperties['Inventory']:
                                        print('You already have this key.')
                                    else:
                                        print('You take key ' + choice)
                                        playerProperties["Inventory"].append('K'+choice)
                                        proceed = True
                                blocked(False)
                        else:
                            print('As you step into the middle of the garage, you\'re greeted with the smell of dust. Seems like nobody was here for a while.')
                            options = ['Inspect', 'Go To Weaponry', 'Look At the Key Chain on the Wall']
                            ask(options)
                    elif playerProperties['Path'][1] == '3':
                        # hotel
                        if len(playerProperties['Path']) >= 3:
                            if playerProperties['Path'][2] == '0':
                                print('You decide to rest for the night in the hotel.')
                                print('When you wake up in the morning, you feel REINVIGORATED.')
                                print('You feel like once you\'re ready, you can go ON THE HUNT.')
                                playerProperties['Events'].append('rested')
                                blocked(False)
                            elif playerProperties['Path'][2] == '1':
                                print('In the hotel, you see a nicely patterned carpet, as well as some bright lighting. It seems as if this place was only for VIPs. Despite this, you can see a small crack in the wall. Is it important? Maybe. Maybe not.')
                                blocked(False)
                            elif playerProperties['Path'][2] == '2':
                                if 'spider' in playerProperties['Events']:
                                    print('The crevice is empty')
                                else:
                                    print('As you examine the crevice, you see a small spider. It asks:')
                                    choice = input('What did the spider say to the fly?')
                                    choice = choice.lower().strip()
                                    if choice == 'will you walk into my parlour?':
                                        playerProperties['Inventory'].append('bullets')
                                        playerProperties['Inventory'].append('gun')
                                        playerProperties['Inventory'].append('meat')
                                        playerProperties['Inventory'].append('card')
                                        playerProperties['Events'].append('spider')
                                        print('You feel you\'re inventory get fuller. You thank the spider and get on you\'re way.')
                                    else:
                                        print('Nothing happened')
                                blocked(False)
                            elif playerProperties['Path'][2] == '3':
                                print('You grab the key card and put it in your inventory.')
                                playerProperties['Inventory'].append('card')
                                blocked(False)
                        else:
                            print('You step into the hotel. It feels safe here, a place where you can rest and relax and prepare for the hard obstacles ahead.')
                            options = ['Rest', 'Inspect', 'Examine Crevice']
                            if 'card' not in playerProperties['Inventory']:
                                options.append('Grab Key card')
                            ask(options)
                else:
                    print('As you venture into the visitor center, you see 4 signs associated with 4 hallways.')
                    options = ['Control center', 'Lab', 'Garage', 'Hotel']
                    ask(options)
            elif playerProperties['Path'][0] == '1':
                # GoingOutside
                if 'gun' in playerProperties['Inventory'] and 'bullets' in playerProperties['Inventory']:
                    if len(playerProperties['Path']) >= 2:
                        if playerProperties['Path'][1] == '0':
                            print('You look around. Nothing seems to be close by. You also see a car. The car seems to be a little damaged, but still good enough for travel. You see that the car number is ' + str(obstacles['CarNumb']))
                            blocked(False)
                        elif playerProperties['Path'][1] == '1':
                            keys = 0
                            for i in playerProperties['Inventory']:
                                if i[0] == 'K':
                                    keys = keys + 1
                            if keys == 0:
                                print('You try and open the car. However, you have no keys.')
                                blocked(False)
                            elif keys == 1:
                                key = ''
                                for i in playerProperties['Inventory']:
                                    if i[0] == 'K':
                                        key = i
                                        break
                                if str('K'+str(obstacles['CarNumb'])) == key:
                                    print('You stick your key in the car and you get in')
                                    traveling()
                                else:
                                    print('You try and open the car with your key. However, your key doesnt work.')
                                    blocked(False)
                            else:
                                proceed = False
                                for i in playerProperties['Inventory']:
                                    if str('K' + str(obstacles['CarNumb'])) == i:
                                        print('You stick your key in the car and you get in')
                                        traveling()
                                        proceed = True
                                        break
                                if not proceed:
                                    print('You try and open the car with all your keys. However, none of your keys work.')
                                    blocked(False)
                    else:
                        print('You go outside, armed with your loaded tranquilizer gun. Nothing seems to be here at the moment though.')
                        options = ['Inspect', 'Travel to a Sector']
                        ask(options)
                else:
                    print('You exit the building. However, you suddenly hear some weird noises near the bushes up ahead. Its probably not safe to go outside without a weapon.')
                    blocked(False)
            elif playerProperties['Path'][0] == '2':
                # Calling For Help
                if 'called' in playerProperties['Events']:
                    print('You pick up the radio. However, you realize you dont need to call for help again.')
                    blocked(True)
                else:
                    print('You use the radio. However, you don\'t know the frequency. Try and guess the frequency.')
                    proceed = False
                    while not proceed:
                        choice = input('What is your guess from 1 - 100, or do you want to go back?')
                        choice.strip()
                        if choice.lower() == 'back':
                            print('You give up. Quitter')
                            proceed = True
                            continue
                        try:
                            if int(choice) < 1 or int(choice) > 100 or not int(choice) % 1 == 0:
                                print('That\'s not a valid number')
                            elif int(choice) > minigames['radio']['frequency']:
                                print('Too high')
                            elif int(choice) < minigames['radio']['frequency']:
                                print('Too low')
                            elif int(choice) == minigames['radio']['frequency']:
                                print('Correct')
                                print('For the helicopter to land, you need to sedate, fence in, and trap all the carnivores.')
                                proceed = True
                                playerProperties['Events'].append('called')
                                blocked(True)
                        except ValueError:
                            print('That\'s not a valid number')
                    blocked(False)
    else:
        print(colors['base'] + 'You\'re on Isla Nublar. You\'re an investor in John Hammond\'s dinosaur atrraction on the island. However, due to unknown reasons, the dinosaurs have escape and everyone has left besides you. However, there is still hope. If you can call a helicopter, you can safely get off the island.')
        playerProperties['Events'].append('intro')


def ask(*options):
    proceed = False
    possibilities = []
    for i in options[0]:
        possibilities.append(i)
    for i in range(len(possibilities)):
        possibilities[i] = str(possibilities[i]).lower()
    while not proceed:
        xy = len(possibilities)
        if not playerProperties['Path'] == '':
            xy += 1
        print('Currently, you see ' + str(xy) + ' options:')
        print('----------------')
        for i in options[0]:
            print(str(i))
        if not playerProperties['Path'] == '':
            print('Back')
        print('What do you want to do?')
        choice = input()
        choice = (choice.strip()).lower()
        if choice in possibilities:
            playerProperties['Path'] = playerProperties['Path'] + str(possibilities.index(choice))
            proceed = True
        elif not playerProperties['Path'] == '' and choice == 'back':
            proceed = True
            playerProperties['Path'] = playerProperties['Path'][:len(playerProperties['Path'])-1]
        print('----------------')


def blocked(dialogue):
    if dialogue:
        input('The only thing you can do is go back')
    else:
        input('Press Enter to continue')
    print('--------------------')
    playerProperties['Path'] = playerProperties['Path'][:len(playerProperties['Path']) - 1]


def main():
    import math
    initialize()
    while 'Win' not in playerProperties['Events']:
        changes()
        choices()
    print('You\'re score is ' + str(math.floor(7000/playerProperties['Turns'])))


main()
