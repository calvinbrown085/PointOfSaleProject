from Database import Database
db = Database()

def runOneOff():
    print("woahs")
    itemList = [
        ("Milk",2,1.00,2.00,"A&E","dairy",10,2),
        ("Soda",3,.50,1.50,"Coke","Drinks",20,13),
        ("Bread",4,1.25, 2.00, "Panera", "Bread", 7,2),
        ("Butter",5,.20, 1.00, "Blue Bonnet", "Dairy", 20,10),
        ("Cereal",6, .90, 1.75, "General Mills", "Breakfast Food", 13,7),
        ("Chips", 7, 1.25, 3.00, "Lays", "Snack Foods", 18,4),
        ("Eggs", 8, 1.00, 1.89, "A&E", "Dairy", 5,1),
        ("Yogurt",9, .10, .59, "A&E", "Dairy", 9,3),
        ("Pizza", 10, 1.20, 3.97, "Red Baron", "Frozen Foods", 8,4),
        ("Coffee", 11, 3.00, 8.00, "Folgers", "Drinks",15,2),
        ("Juice", 12, .50, 2.20, "Ocean Spray", "Drinks", 8,6),
        ("Peanut Butter", 13, .95, 2.85, "Jiffy", "Snack Foods", 4,1),
        ("Ice Cream", 14, 1.00, 4.20, "Ben & Jerry", "Dairy", 19,3),
        ("Cheese", 15, .90, 2.15, "Market Pantry", "Dairy", 20,10),
        ("Chicken", 16, 2.50, 5.29, "Chucky Chicken", "Poultry", 16,12),
        ("Fish", 17, 2.00, 4.50, "Gortons", "Frozen Foods", 20,11),
        ("Hot Dogs", 18, .30, 2.00, "Oscar Meyer", "Meat", 13,9),
        ("Granola Bars", 19, 1.22, 3.27, "Nature Valley", "Snack Foods", 8,3),
        ("Rice", 20, .20, 2.15, "Minute Rice", "Rice", 70,40),
        ("Fruit Snacks", 21, .99, 2.50, "Welch's", "Snack Foods", 23,10),
        ("Oatmeal", 22, .20, 1.99, "Quaker Oats", "Breakfast Food", 6,2),
        ("Waffles", 23, 1.15, 3.17, "Eggo", "Breakfast Food", 40,13),
        ("Bananas", 24, .05, .85, "Chiquita", "Fruit", 20,14),
        ("Bacon", 25, 1.90, 3.00, "Hormel", "Meat", 12,1),
        ("Water", 26, .50, 1.25, "Dasani", "Water", 50,30),
        ("Cereal Bars", 27, 2.29, 3.25, "Nutri-Grain", "Breakfast Food",14,13),
        ("Hot Dogs", 28, 1.19, 2.00, "Meat", "Oscar-Meyer", 30,12),
        ("Hamburger", 29, 3.00, 4.49, "Meat", "Meat Sellers Inc", 10,12),
        ("Sugar", 30, 1.99, 2.99, "Sugar", "Sugar Co.", 14,11)
    ]
    for item in itemList:
        db.insertIntoInventoryLog(item[1], item[6], item[7])
