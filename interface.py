from xwingcampaign import *
import pickle
from preferences import *
titles = {'main_title': """
 __  __  __        ___                ____                            _             
 \ \/ /  \ \      / (_)_ __   __ _   / ___|__ _ _ __ ___  _ __   __ _(_) __ _ _ __  
  \  /____\ \ /\ / /| | '_ \ / _` | | |   / _` | '_ ` _ \| '_ \ / _` | |/ _` | '_ \ 
  /  \_____\ V  V / | | | | | (_| | | |__| (_| | | | | | | |_) | (_| | | (_| | | | |
 /_/\_\     \_/\_/  |_|_| |_|\__, |  \____\__,_|_| |_| |_| .__/ \__,_|_|\__, |_| |_|
                             |___/                       |_|            |___/       
"""}

colors = ['PINK', 'BLUE', 'GREEN', 'YELLOW', 'RED']
sectors_list = ['A1', 'B1', 'C1', 'D1', 'E1',
                'A2', 'B2', 'C2', 'D2', 'E2',
                'A3', 'B3', 'C3', 'D3', 'E3',
                'A4', 'B4', 'C4', 'D4', 'E4']




def save_campaigns(campaign_dict):
    with open(save_file, 'wb') as file:
        pickler = pickle.Pickler(file)
        pickler.dump(campaign_dict)


def load_campaigns():
    with open(save_file, 'rb') as file:
        depickler = pickle.Unpickler(file)
        campaign_dict = depickler.load()

    return campaign_dict

try:
    campaign_dict = load_campaigns()
except:
    campaign_dict = {}

def Clear():
    print('\n' * 100)


def newCampaign():

    faction1 = {}
    faction2 = {}

    proxy_colors = []
    for color in colors:
        proxy_colors.append(color)

    # -- First faction --
    print("First faction")
    print("What's the name of the faction ?")
    name = input()
    faction1['name'] = name
    print("What's the name of the player ?")
    player = input()
    faction1['player'] = player
    print("Choose a color :")
    i = 1
    for color in proxy_colors:
        print("[{}] {}".format(i, color))
        i += 1
    choice = input()

    color = proxy_colors[int(choice) - 1]
    faction1['color'] = color
    proxy_colors.remove(color)

    # -- Second Faction --
    print("Second faction")
    print("What's the name of the faction ?")
    name = input()
    faction2['name'] = name
    print("What's the name of the player ?")
    player = input()
    faction2['player'] = player
    print("Choose a color :")
    i = 1
    for color in proxy_colors:
        print("[{}] {}".format(i, color))
        i += 1
    choice = input()

    color = proxy_colors[int(choice) - 1]
    faction2['color'] = color

    factions = [Faction(faction1['name'], faction1['player'], faction1['color']),
                Faction(faction2['name'], faction2['player'], faction2['color'])]

    name = "{} versus {}".format(faction1['name'], faction2['name'])

    campaign_dict[name] = Campaign(factions[0], factions[1])

    campaignMenu(campaign_dict.get(name))


def campaignMenu(campaign):
    campaign_menu = True

    error = ''
    while campaign_menu:
        Clear()
        print(campaign.repr_factions())
        print(campaign.repr_sector_map())
        print()
        print("Campaign Menu")
        print(error)
        print("[1] : New battle")
        print("[0] : Quit")
        choice = input()

        if choice == '0':
            error = ''
            campaign_menu = False

        elif choice == '1':
            error = ''
            battleMenu(campaign)
        else:
            error = Color('ERROR : Unkown command', 'RED')


def battleMenu(campaign):
    battle_menu = True
    batt_error = ''

    while battle_menu:
        sector_chosen = False
        batt_error = ''
        while sector_chosen is False:
            Clear()
            print(campaign.repr_factions())
            print(campaign.repr_sector_map())
            print()
            print('Battle Menu')
            print(batt_error)
            print('Which sectors is under attack ?')
            print('(Type 0 to abort)')
            choice = input()

            if choice in sectors_list:
                batt_error = ''
                sector = choice
                sector_chosen = True
            elif choice == '0':
                battle_menu = False
                break
            else:
                batt_error = Color("ERROR : Unkown sector", 'RED')

        winner_chosen = False
        while winner_chosen is False:
            Clear()
            print(campaign.repr_factions())
            print(campaign.repr_sector_map())
            print()
            print('Battle Menu')
            print(batt_error)
            print(campaign.sectors[sector].repr_sector())
            print("Who won the battle ?")
            print("[1] : " + campaign.fac_names[0])
            print("[2] : " + campaign.fac_names[1])
            print('(Type 0 to abort)')
            choice = input()

            if choice == '0':
                batt_error = ''
                winner_chosen = True
                break
            elif choice in ['1', '2']:
                batt_error = ''
                winner = campaign.factions.get(campaign.fac_names[int(choice)-1])
                winner_chosen = True
            else:
                batt_error = Color("ERROR : Unkown command", 'RED')

        points_chosen = False
        while points_chosen is False:
            Clear()
            print(campaign.repr_factions())
            print(campaign.repr_sector_map())
            print()
            print('Battle Menu')
            print(batt_error)
            print(campaign.sectors[sector].repr_sector())
            print("Major or minor win ?")
            print("[1] : Major win (5 points)")
            print("[2] : Minor Win (3 points)")
            print('(Type 0 to abort)')
            choice = input()

            if choice == '0':
                batt_error = ''
                points_chosen = True
                break
            elif choice in ['1', '2']:
                batt_error = ''
                if choice == '1':
                    points = rules['major_victory']
                else:
                    points = rules['minor_victory']
                points_chosen = True
            else:
                batt_error = Color("ERROR : Unkown command", 'RED')

        campaign.battle(sector, winner, points)
        battle_menu = False

def loadCampaign():
    load_campaign = True
    load_error = ''
    while load_campaign:
        Clear()
        print("Campaigns List")
        campaign_list = []
        print(load_error)
        for i, name in enumerate(campaign_dict):
            i += 1
            print("[{}] : {}".format(i, name))
            campaign_list.append(name)
        print("[0] : Quit")

        choice = input()

        if choice == '0':
            load_error = ''
            load_campaign = False
        else:
            try:
                if int(choice) in range(len(campaign_list)) and choice is not '0':
                    load_error = ''
                    camp = campaign_dict.get(campaign_list[int(choice)-1])
                    load_campaign = False
                    campaignMenu(camp)
                else:
                    load_error = Color("ERROR : Unknown command", 'RED')
            except:
                load_error = Color("ERROR : Unknown command", 'RED')


def quit():
    print("_quit()")

func_dict = {'1': newCampaign,
             '2': loadCampaign,
             '0': quit}


def interface():

    continuer = True

    while continuer:
        Clear()
        print("Main Menu")
        print("[1] New Campaign")
        print("[2] Load Campaign")
        print("[0] Quit")
        choice = input()

        if choice == '0':
            break

        func = func_dict.get(choice)
        func()
    save_campaigns(campaign_dict)

interface()