import os
import random
import time
from datetime import datetime

# Menu data
screen_data = {
    "menu": {
        "title": "**********************\n* Epic Fighting Game *\n**********************\n",
        "sub-text": "Im bored, choose and option\n",
        "options": {
            "1":{
                "title": "Start Game",
                "state": "character_select"
            }, "2": {
                "title": "Exit",
                "state": "exit"
            }
        }
    },
    "character_select": {
        "title": "Character Select",
        "sub-text": "Choose your fighters!\n",
        "options": {

        }
    },
    "post_fight": {
        "title": "Post Fight Details",
        "sub-text": "Numbers babyyyy",
        "options": {
            "1": {
                "title": "Return to Menu",
                "state": "menu"
            },
            "2": {
                "title": "Exit",
                "state": "exit"
            }
        }
    }
}

# Melee range is by default 5 meters
# Speed is meters per turn the character can move
fighter_data = {
    "1":{
        "name": "Johnny Cools",
        "health": 100,
        "attack": 20,
        "speed": 30,
        "weapon_type": "Sword",
        "weapon_class": "Melee",
        "range": 5
    },
    "2":{
        "name": "Sally Swift",
        "health": 70,
        "attack": 15,
        "speed": 40,
        "weapon_type": "Dagger",
        "weapon_class": "Melee",
        "range": 5
    },
    "3":{
        "name": "Big Bob",
        "health": 150,
        "attack": 25,
        "speed": 20,
        "weapon_type": "Hammer",
        "weapon_class": "Melee",
        "range": 5
    },
    "4":{
        "name": "Ronny Ranger",
        "health": 50,
        "attack": 30,
        "speed": 40,
        "weapon_type": "Long Bow",
        "weapon_class": "Ranged",
        "range": 60
    },
    "5":{
        "name": "Pistol Pierre",
        "health": 40,
        "attack": 25,
        "speed": 40,
        "weapon_type": "Long Bow",
        "weapon_class": "Ranged",
        "range": 40
    }
}



"""
MAIN FIGHTING GAME LOGIC START
"""

class ScreenController:
    """This class is used to control the state and print text to screen"""

    def __init__(self):
        self.state = ""
        self.text_to_display = {}

    """Changes the current state

    Args:
        new_state(string): The new state to update too
    """   
    def change_state(self, new_state):
        self.state = new_state

    """Clears screen and prints text based on the current state."""
    def print_screen(self):
        self.text_to_display = screen_data.get(self.state, {})
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.text_to_display.get('title', '')}\n{self.text_to_display.get('sub-text', '')}")
        for option_key, option_value in self.text_to_display.get('options', {}).items():
            print(f"{option_key}. {option_value.get('title', '')}")

    """Print all the characters from character data."""
    def print_characters_list(self):
        for fighter_key, fighter_value in fighter_data.items():
            print(f"{fighter_key}. {fighter_value.get('name', '')} - Health: {fighter_value.get('health', '')}, Attack: {fighter_value.get('attack', '')}, Speed: {fighter_value.get('speed', '')}, Weapon: {fighter_value.get('weapon_type', '')}")

    """Handles user selection for changing state."""
    def handle_state_input(self):
        user_selection = input("Select an option: ")
        if user_selection in self.text_to_display.get('options', {}):
            selected_option = self.text_to_display['options'][user_selection]
            self.change_state(selected_option.get('state'))

game_state_controller = ScreenController()

class Player:
    """The class that the handles player stats, and makes them take damage"""

    def __init__(self, name, health, attack, speed, weapon_type, weapon_class, range):
        self.name = name
        self.health = health
        self.attack = attack
        self.speed = speed
        self.weapon = weapon_type
        self.weapon_class = weapon_class
        self.range = range

    """Tracks the players health and reduces it

    Args:
        damage(int): The ammount of damage to subtract from the health
    
    Returns:
        boolean: True/False if the player has been slain
    """
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            return True  # Player is dead
        return False  # Player is still alive

class FightingLoop:
    """This class containts the methods for the fighting loop"""

    def __init__(self):
        self.actions_log = ""
        self.distance_between = 20
        self.turn = 1
        self.action_delay_low = 2.5
        self.action_delay_high = 3.5

    """Print battle event to screen, stores in log, and initiates a delay
    
    Args:
        event(string): The event to print and log
    """
    def log_event(self, event):
        print(event)
        self.actions_log += event
        time.sleep(random.uniform(self.action_delay_low, self.action_delay_high))


    """Processes a turn in battle
    
    Args:
        attacker(Player): The attacker for the turn
        defender(Player): The defender for the turn
    """
    def process_turn(self, attacker, defender):
        # Default is melee
        weapon_class = "Melee"
        if attacker.weapon_class == "Ranged":
            weapon_class = "Ranged"

        
        if self.distance_between > attacker.range:

            distance_moved = 0

            if (self.distance_between - attacker.speed) < attacker.range:
                self.distance_moved = self.distance_between - attacker.range # This is always 0 for some reason
                self.distance_between = attacker.range

            else:
                distance_moved = attacker.speed
                self.distance_between = self.distance_between - attacker.speed

            self.log_event(f"Turn: {self.turn} | {attacker.name} moves {distance_moved}, " +
                           f"and is now {self.distance_between} meters from {defender.name}\n")

        elif (attacker.weapon_class == "Ranged" and 
                self.distance_between < attacker.range/2 and 
                random.randint(1, 100) <= 30):
            distance_moved = attacker.range - self.distance_between
            self.distance_between = attacker.range
            self.log_event(f"Turn: {self.turn} | {attacker.name} moves " + 
                           f"{distance_moved}, and is now {self.distance_between} meters from {defender.name}\n")

        else:
            self.log_event(f"Turn: {self.turn} | {attacker.name} " + 
                           f"{"swings at" if weapon_class == "Melee" else "shoots"} {defender.name} with " +  
                           f"their {attacker.weapon}" + 
                           f"{f" from {self.distance_between} meters away" if weapon_class == "Ranged" else ""}... \n")

            damage = attacker.attack + random.randint(-10, 5)
            
            if random.randint(1, 100) <= attacker.range/2:
                self.log_event(f"Turn: {self.turn} | {attacker.name} misses their {"swing" if weapon_class == "Melee" else "shot"}\n")

            elif random.randint(1, 100) <= defender.speed:
                self.log_event(f"Turn: {self.turn} | {defender.name} dodged the "+
                               f"{"swing" if weapon_class == "Melee" else "shot"} from {attacker.name}!\n")

            else:
                self.log_event(f"Turn: {self.turn} | {attacker.name} hits {defender.name} for " + 
                               f"{damage} damage! {defender.name} has {defender.health - damage} health remaining.\n")

                if defender.take_damage(damage):
                    self.log_event(f"Turn: {self.turn} | {defender.name} has been slain!")

                    return True

        self.turn += 1
        self.log_event("---------------------------------------------------\n")

    """Controls the fighting loop

    Args:
        player1(Player): First fighter chosen
        player2(Player): Second fighter chosen    
    """
    def start_fight(self, player1, player2):
        os.system('cls' if os.name == 'nt' else 'clear')

        first_player = player1 if random.choice([True, False]) else player2
        second_player = player2 if first_player == player1 else player1

        ln = f"{first_player.name} will go first! Both fighters are 20 meters apart\n"
        print(ln)
        self.actions_log += ln
        ln = "---------------------------------------------------\n"
        print(ln)
        self.actions_log += ln

        time.sleep(4)

        # Combat loop
        while True:

            if self.process_turn(first_player, second_player):
                break

            if self.process_turn(second_player, first_player):
                break

            
        # Post game choices
        while True:
            choice = input("\nFight over! Would you like to save the results to a file? (y/n) ")

            if choice.lower() == 'y':
                with open(f"{first_player.name}_vs_{second_player.name}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt", "w") as f:
                    f.write(self.actions_log)
                print("Battle successfully chronicled")
                game_state_controller.change_state("exit")
                break

            elif choice.lower() == 'n':
                game_state_controller.change_state("exit")
                break

            else:
                print("Please select a valid option (y/n)") 


"""
MAIN FIGHTING GAME LOGIC END
"""

def main():
    game_state_controller.change_state("menu")
    while True:
        match game_state_controller.state:
            case "menu":
                game_state_controller.print_screen()
                game_state_controller.handle_state_input()

            case "character_select":
                game_state_controller.print_screen()
                game_state_controller.print_characters_list()
                player1 = input("Select First Fighter: ")
                player2 = input("Select Second Fighter: ")
                if player1 in fighter_data and player2 in fighter_data:
                    FightingLoop().start_fight(Player(**fighter_data[player1]), Player(**fighter_data[player2]))
                else:
                    print("Invalid fighter selection. Returning to menu.")
                    game_state_controller.change_state("menu")
            case "exit":
                print("Exiting the game. Goodbye!")
                break


if __name__ == "__main__":
    main()