from format import Color
from preferences import *

sector_map = """
    A       B       C       D       E

1   {} ----- {} ----- {} ----- {} ----- {}
    |       |       |       |       |
    |       |       |       |       |
2   {} ----- {} ----- {} ----- {} ----- {}
    |       |       |       |       |
    |       |       |       |       |
3   {} ----- {} ----- {} ----- {} ----- {}
    |       |       |       |       |
    |       |       |       |       |
4   {} ----- {} ----- {} ----- {} ----- {}
""".format('{A1:}', '{B1:}', '{C1:}', '{D1:}', '{E1:}',
           '{A2:}', '{B2:}', '{C2:}', '{D2:}', '{E2:}',
           '{A3:}', '{B3:}', '{C3:}', '{D3:}', '{E3:}',
           '{A4:}', '{B4:}', '{C4:}', '{D4:}', '{E4:}')


class Sector:
    def __init__(self, position):
        """
        :param position: Set sector's position
        """
        self.pos = position
        self.value = 0
        self.owner = False

    def set_owner(self, faction):
        self.owner = faction

    def set_value(self, value):
        self.value = value

    def __repr__(self):
        if self.owner is False:
            result = str(self.value)
        else:
            result = str(Color(self.value, self.owner.color))

        return result

    def repr_sector(self):
        return "Sector {} | Owner : {} | Value : {}".format(self.pos, self.owner, self.value)


class Faction:
    def __init__(self, name, player, color):
        """
        :param name: Name of the faction
        :param player: Faction's player
        :param color: Faction's color (see format.py to see available colors
        """
        self.name = name
        self.player = player
        self.color = color

        self.points = 0
        self.owned_sectors = 0

    def set_points(self, points):
        self.points = points

    def set_owned_sectors(self, owned_sectors):
        self.owned_sectors = owned_sectors

    def __repr__(self):
        return str(Color(self.name, self.color))


class Campaign:
    def __init__(self, faction1, faction2):
        """
        :param faction1: 
        :param faction2: 
        """
        self.fac_names = [faction1.name, faction2.name]
        self.factions = {faction1.name: faction1,
                         faction2.name: faction2}

        # -- Create and assign the sectors
        self.sectors = {}
        for number in ['1', '2', '3', '4']:
            for letter in ['A', 'B', 'C', 'D', 'E']:
                self.sectors[letter + number] = Sector(letter + number)

        for sector in self.sectors.values():
            if sector.pos in ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'A4', 'B4']:
                sector.set_owner(self.factions.get(self.fac_names[0]))
            else:
                sector.set_owner(self.factions.get(self.fac_names[1]))

            sector.set_value(rules['initial_points'])

        self.update_points_own()

    def battle(self, sector_pos, winner, points):

        sector = self.sectors.get(sector_pos)

        if winner == sector.owner:
            proxy_value = sector.value + points

            if proxy_value > rules['max_points']:
                new_value = rules['max_points']
            else:
                new_value = proxy_value

            sector.set_value(new_value)

        else:
            proxy_value = sector.value - points

            if proxy_value == 0:
                sector.set_value(0)
                sector.set_owner(False)

            elif proxy_value > 0:
                if proxy_value > rules['max_points']:
                    new_value = rules['max_points']
                else:
                    new_value = proxy_value

                sector.set_value(new_value)

            elif proxy_value < 0:
                proxy_value -= (proxy_value * 2)

                if proxy_value > rules['max_points']:
                    new_value = rules['max_points']
                else:
                    new_value = proxy_value

                sector.set_value(new_value)
                sector.set_owner(winner)

        self.update_points_own()

    def update_points_own(self):
        for faction in self.factions.values():
            pts = 0
            own = 0
            for sector in self.sectors.values():
                if sector.owner == faction:
                    pts += sector.value
                    own += 1

            faction.set_points(pts)
            faction.set_owned_sectors(own)

    def repr_factions(self):
        faction1 = self.factions.get(self.fac_names[0])
        faction2 = self.factions.get(self.fac_names[1])

        return "{} ({} - {}) {}".format(faction1, faction1.points, faction2.points, faction2)

    def repr_sector_map(self):
        """Return the sectors' map with colored values"""
        return sector_map.format(A1=self.sectors.get('A1'), B1=self.sectors.get('B1'), C1=self.sectors.get('C1'),
                                 D1=self.sectors.get('D1'), E1=self.sectors.get('E1'),
                                 A2=self.sectors.get('A2'), B2=self.sectors.get('B2'), C2=self.sectors.get('C2'),
                                 D2=self.sectors.get('D2'), E2=self.sectors.get('E2'),
                                 A3=self.sectors.get('A3'), B3=self.sectors.get('B3'), C3=self.sectors.get('C3'),
                                 D3=self.sectors.get('D3'), E3=self.sectors.get('E3'),
                                 A4=self.sectors.get('A4'), B4=self.sectors.get('B4'), C4=self.sectors.get('C4'),
                                 D4=self.sectors.get('D4'), E4=self.sectors.get('E4'))

    def __repr__(self):
        return "{} versus {}".format(self.fac_names[0], self.fac_names[1])

