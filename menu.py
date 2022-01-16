import os
# Script for creating a menu
class menu:
    menuItems = []
    
    # Prints out the list of items, prompts a choice
    def __repr__(self):
        counter = 1
        for x in self.menuItems:
            print(str(counter) + ': ' + x)
            counter += 1
        print('\n Choose:')
        
    
    # CONSTRUCTOR
    def __init__(self, *args):
        # loop given *args
        for x in args:
            # add to menulist
            self.menuItems.append(x)
        
        #call to repr for printing
        c = self.__repr__()
        # Get user input to set item
        self.setMenuItem(input())
        # get and print the choice
        print('You chose: %s' % self.getMenuItem())

    def setMenuItem(self, c):
        self.menuItem = c
    # Gets the value of chosen(c) index
    def getMenuItem(self):#, c):
#        return self.menuItems[c - 1]
        return self.menuItems[int(self.menuItem) - 1]
# This is how you call the method from when imported
if __name__ == "__main__":
    foo = menu("this","is","a","template")
