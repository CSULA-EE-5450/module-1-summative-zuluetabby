class Ship:
    id = 0

    def __init__(self, ship_parts=list(), drowned=0):
        self.size = len(elements)
        self.elements = elements
        self.drowned_elements = drowned
        self.id = Ship.id
        Ship.id += 1

    def is_drowned(self):
        return self.drowned_elements == self.size

    def hit(self, row, col):
        for element in self.elements:
            if element.row == row and element.col == col and not element.shot_down:
                element.shot_down = True
                self.drowned_elements += 1
                return self
        return None

    def add_element(self, ship_element):
        self.elements.append(ship_element)
        self.size += 1

    def destroy_ship(self):
        for element in self.elements:
            del element
        self.size = 0


class ShipElement:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.shot_down = False
