import random # to generate random numbers
import tkinter as tk # to create GUI
import os

def get_file_names(directory):
    file_names = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            file_names.append(file)
    return file_names

# Global Variables
player_name = ""
player_money = 0
player_health = 100
player_points = 0

player_inventory = {
    'weapons': [],
    'keys': [],
    'armors': [],
    'healing_pads': []
}

room_descriptions = []

shop_items = {
    'weapons': [],
    'keys': [],
    'armors': [],
    'healing_pads': []
}

roomsData = [] # list to store rooms data
enemiesData = []

# Function to load room descriptions from a text file
def load_room_descriptions():
    files = get_file_names('files')
    for filename in files:
        if "Room" in filename:
            filename = 'files/' + filename
            file = open(filename, 'r')
            welcome = file.readline().strip('\n')
            description = file.readline().strip('\n')
            file.readline().strip('\n')
            file.readline().strip('\n')
            enemy = file.readline().strip('\n').split(',')
            enemiesData.append({
                'name': enemy[0],
                'damage': enemy[1],
                'health': enemy[2]
            })

            roomsData.append({
                'welcome': welcome,
                'description': description
            })


# Function to load shop items from a file
def load_shop_items():
    w = 1
    k = 1
    a = 1
    h = 1
    files = get_file_names('files')
    for filename in files:
        if "Shop" in filename:
            filename = 'files/' + filename
            file = open(filename, 'r')
            for line in file:
                line = line.strip('\n')
                if (not '#' in line) and ('weapon' in line):
                    weapon = line.split(":")[1]
                    weapon = weapon.split(",")
                    id = 'w' + str(w)
                    w += 1
                    shop_items['weapons'].append({'id': id, 'name': weapon[0], 'damage': weapon[1], 'price': weapon[2]})
                elif (not '#' in line) and ('key' in line):
                    key = line.split(":")[1]
                    key = key.split(",")
                    id = 'k' + str(k)
                    k += 1
                    shop_items['keys'].append({'id': id, 'code': key[0], 'price': key[1]})
                elif (not '#' in line) and ('armour' in line):
                    armour = line.split(":")[1]
                    armour = armour.split(",")
                    id = 'a' + str(a)
                    a += 1
                    shop_items['armors'].append({'id': id, 'durability': armour[0], 'price': armour[1]})
                elif (not '#' in line) and ('healingPad' in line):
                    pad = line.split(":")[1]
                    pad = pad.split(",")
                    id = 'h' + str(h)
                    h += 1
                    shop_items['healing_pads'].append({'id': id, 'health': pad[0], 'price': pad[1]})

# Function to display the player's inventory
def display_inventory():
    global player_inventory

    inventory_window = tk.Toplevel()
    inventory_window.title("Inventory")

    weapons_label = tk.Label(inventory_window, text="Weapons:")
    weapons_label.pack()
    for weapon in player_inventory['weapons']:
        weapon_label = tk.Label(inventory_window, text=f"Name: {weapon['name']}, Damage: {weapon['damage']}, Price: {weapon['price']}")
        weapon_label.pack()

    keys_label = tk.Label(inventory_window, text="Keys:")
    keys_label.pack()
    for key in player_inventory['keys']:
        key_label = tk.Label(inventory_window, text=f"Code: {key['code']}, Price: {key['price']}")
        key_label.pack()

    armors_label = tk.Label(inventory_window, text="Armors:")
    armors_label.pack()
    for armor in player_inventory['armors']:
        print(armor)
        armor_label = tk.Label(inventory_window, text=f"Durability: {armor['durability']}, Price: {armor['price']}")
        armor_label.pack()

# Function to enter a room
def enter_room(room_name):
    global roomsData, enemiesData
    room_index = int(room_name.split()[-1]) - 1
    room = roomsData[room_index]
    enemy = enemiesData[room_index]
    enemy_name = enemy['name']
    enemy_damage = enemy['damage']
    enemy_health = enemy['health']

    print('\n > Entered in', room_name, '\n')
    print(room['welcome'])
    print(room['description'])
    print(f"Enemy: \n   > {enemy_name}, Damage: {enemy_damage}, Health: {enemy_health}")


def find_item(id):
    for key in shop_items:
        for item in shop_items[key]:
            if item['id'] == id:
                return (key, item)
    return None


# Function to open the shop
def open_shop():
    global player_money
    print("\n\t\t | Welcome to Shop | \n")
    print(" > You have money:", player_money)
    print("\n\t\t | Items in Shop |")
    for key in shop_items:
        print('\n  > ', key.upper(), ' < ')
        for item in shop_items[key]:
            print(item)

    id = input("\nEnter ID of item to purchase: ")
    item = find_item(id)
    if item == None:
        print("\n > Sorry. Item not available!")
    else:
        player_inventory[item[0]].append(item[1])
        print('\n > Item Added to Inventory!')

# Function to create the GUI
def create_gui():
    global player_name, player_money, player_health, player_points, player_inventory

    # Create the main window
    window = tk.Tk()
    window.title("Text Adventure Game")

    # Display player information
    player_info_label = tk.Label(window, text=f"Name: {player_name}\nMoney: {player_money}\nHealth: {player_health}\nPoints: {player_points}")
    player_info_label.pack()

    # Display inventory
    inventory_button = tk.Button(window, text="Inventory", command=display_inventory)
    inventory_button.pack()

    # Create buttons for rooms and shop
    room_buttons_frame = tk.Frame(window)
    room_buttons_frame.pack()

    room_names = ["Room 1", "Room 2", "Room 3", "Room 4"]
    for room_name in room_names:
        room_button = tk.Button(room_buttons_frame, text=room_name, command=lambda name=room_name: enter_room(name))
        room_button.pack(side=tk.LEFT)

    shop_button = tk.Button(window, text="Shop", command=open_shop)
    shop_button.pack()

    # Start the main loop
    window.mainloop()

# Function to initialize the game
def startGame():
    global player_name, player_money, player_health, player_points
    player_name = input("Enter your name: ")
    player_money = random.randint(50, 310)
    player_health = 100 # full health
    player_points = 0 # starting points
    load_room_descriptions() # load rooms data
    load_shop_items() # loading shop data

# Main function to start the game
def main():
    startGame()
    create_gui()

if __name__ == "__main__":
    main()
