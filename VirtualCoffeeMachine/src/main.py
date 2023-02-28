MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources: dict[str, int] = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}
money = 0.0
while True:
    choice = input("What would you like? (espresso/latte/cappuccino):")
    if choice == 'off':
        break
    elif choice == 'report':
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Money: ${money}")
    elif choice == 'espresso' or choice == 'latte' or choice == 'cappuccino':
        if choice != 'espresso':
            milk = MENU[choice]['ingredients']['milk']
            if resources['milk'] < milk:
                print("Sorry:( there is not enough milk.")

        water = MENU[choice]['ingredients']['water']
        coffee = MENU[choice]['ingredients']['coffee']
        if resources['water'] < water:
            print("Sorry:( there is not enough water.")
        elif resources['coffee'] < coffee:
            print("Sorry:( there is not enough coffee.")
        else:
            print("Please insert coins.")
            quarters = int(input("How many quarters?:"))
            dimes = int(input("How many dimes?:"))
            nickles = int(input("How many nickles?:"))
            pennies = int(input("How many pennies?:"))
            total = quarters*0.25 + dimes*0.1 + nickles*0.05 + pennies*0.01
            if total < MENU[choice]['cost']:
                print("Sorry that's not enough money. Money refunded.")
            else:
                money += MENU[choice]['cost']
                change = round(total - MENU[choice]['cost'], 2)
                print(f"Here is ${change} in change.")
                resources['water'] -= MENU[choice]['ingredients']['water']
                resources['coffee'] -= MENU[choice]['ingredients']['coffee']
                if choice != 'espresso':
                    resources['milk'] -= MENU[choice]['ingredients']['milk']
                print(f"Here is your {choice}, Enjoy!")
    else:
        print("Please enter a valid selection! Try again!!")

