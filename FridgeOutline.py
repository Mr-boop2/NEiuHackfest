import sqlite3
from colorama import *
from datetime import * 

 

class MyFridgeUI:
    def __init__(self):
        self.userInput = 0 
        self.itemsData = {}
        self.userItems = []
        self.itemsQuantity = []   
        self.userDB = MyFridgeDB()    
        self.userRecipes = MyRecipeDB()
    

    def IntroUI(self):

        try: 
            print(f"{Style.BRIGHT}{Fore.GREEN}Welcome to MyFridge \nWhat would you like to do today.{Fore.RESET}")
            self.userInput = int(input(f"{Fore.LIGHTBLUE_EX}1. Add Items \n{Fore.YELLOW}2. Update/Remove Items  \n{Fore.CYAN}3. View Current Items \n{Fore.RESET}4. Add Recipes  \n5. View Saved Recipes  \n6. View Available Recipes \n7. Update/Remove Recipes   \n8. Quit \nEnter Here: "))
            if self.userInput == 1: 
                self.userDB.createTable()
                self.userAddItems()                 
                self.contOperation()  

            elif self.userInput == 2:     
                numRows = self.userDB.fetchMethod()
                if numRows != 0: 
                    print('''Which item would you like to update/remove? \nEnter 00 to clear all. ''')
                    ingID = int(input("Enter Here: "))
                    if (ingID == 00):
                        self.userDB.updateItems(ingID)
                    else: 
                        updatedQuant = int(input("Enter your updated quantity: "))
                        self.userDB.updateItems(ingID,updatedQuant)
                self.contOperation()                   

            elif self.userInput == 3: 
                print(f"{Fore.GREEN}\nHere are your current items{Fore.RESET}")
                self.userDB.fetchMethod()
                self.contOperation()
        
            elif self.userInput == 4: 
                self.userRecipes.createTable()
                recipeName = input("Enter the name of your recipe: ").capitalize()
                self.userRecipes.userAddRecipe(recipeName)
                self.contOperation()
            
            elif self.userInput == 5:
                self.userRecipes.recipeDBFetchMethod()
                
                self.contOperation()
            elif self.userInput == 6:
                self.userRecipes.userViewAvailableRecipes()
                self.contOperation()


            elif self.userInput == 7:
                numRecipeRows = self.userRecipes.recipeDBFetchMethod()
                if numRecipeRows != 0:
                    print('''Which recipe would you like to update/remove? \nEnter 00 to clear all. ''')
                    recipeID = int(input("Enter RecipeID Here: "))
                    if recipeID == 00:
                        self.userRecipes.userUpdateRecipes(recipeID)
                    else:  
                        userChoice = int(input("Would you like to update or remove (1/0): "))
                        self.userRecipes.userUpdateRecipes(recipeID,userChoice)
                self.contOperation()
            
            elif self.userInput == 8:
                print("Goodbye.")      
            else: 
                print("Invalid Entry. Try Again.")
                self.IntroUI()
        except Exception as e: 
            print(e)
            print("Try Again.")
            self.IntroUI()

    def contOperation(self):
        keepGoing = input("Would you like to continue operation? (Y/N): ")    
        if keepGoing.lower() == 'y':
            self.IntroUI()
        elif keepGoing.lower() == "n":
            print("Goodbye.")
        else: 
            print("Invalid Input. Try Again.")
            self.contOperation()
    
    def userAddItems(self):        
        userContinue = 'y'
        while userContinue.lower() == 'y':
            ingredient = self.userGetIngredient()   
            ingClassEXP = self.userGetClass()                     
            ingQuantity = self.userGetIngQuant()            
            
            self.userDB.addItems(ingredient,ingClassEXP,ingQuantity)          
            userContinue = input(f"{Fore.LIGHTBLUE_EX}Would you like to continue adding items? (Y/N): {Fore.RESET}")            
            if (userContinue.lower() != 'y') and (userContinue.lower() != 'n'):
                print(f"{Fore.RED}Try again!")
                userContinue = input(f"{Fore.LIGHTBLUE_EX}Would you like to continue adding items? (Y/N): {Fore.RESET}")        

    def userGetIngredient(self):
        while True: 
            ingredient = (input(f"{Fore.LIGHTBLUE_EX}Add your Items (One at a time): {Fore.RESET}"))
            if (ingredient.isdigit() is False) and (ingredient != '') and not ingredient.isspace():
                return ingredient.capitalize() 
            else: 
                print("Try Again") 
                continue  

    def userGetClass(self):
        while True: 
            ingClass = input(f"Select your item class:\n1. Vegetable \n2. Meat \n3. Fruit \n4. Grain \nEnter Here: ")
            match ingClass: 
                case "1":
                    ingClass = Vegetable()
                    return ingClass.expiration()
                case "2":
                    ingClass = Meat()
                    return ingClass.expiration()
                case "3":
                    ingClass = Fruit()
                    return ingClass.expiration()
                case "4":
                    ingClass = Grain()
                    return ingClass.expiration()
    def userGetIngQuant(self):
        while True: 
            ingQuantity = input(f"{Fore.LIGHTBLUE_EX}Enter the Quantity: {Fore.RESET}")
            try: 
                ingQuantity = int(ingQuantity)
                if ingQuantity > 0:
                    return ingQuantity
                else: 
                    continue
            except ValueError:
                print(f"{Fore.LIGHTBLUE_EX}Try again!{Fore.RESET}")
                continue       
    
    def run(self):
        self.IntroUI()

class MyFridgeDB: 
    def __init__(self):
        self.conn = sqlite3.connect("FakeIngredients.sql")
        self.cur = self.conn.cursor()
    def createTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Inventory
                         (ItemID Integer Primary Key NOT NULL, IngredientName TEXT NOT NULL, 
                         Quantity INTEGER, Date TIMESTAMP, ExpDate TIMESTAMP)''')
        self.conn.commit()

    def addItems(self,ingredient,ingClassEXP,ingQuantity):
        ingCreationDate = datetime.today()
        self.cur.execute('''INSERT INTO Inventory (IngredientName, Quantity, Date, ExpDate)
                            VALUES (?,?,?,?)''',
                            (ingredient,ingQuantity,ingCreationDate.strftime("%A, %B %d %Y"),ingClassEXP))
        self.conn.commit()
   
    def fetchMethod(self):
        '''Selects all rows from Inventory table. For each row it will print each column then move to the next row.
        If the Inventory table is empty numRows returns False.'''
        self.cur.execute('''SELECT * FROM Inventory''') 
        results = self.cur.fetchall()
        self.numRows = len(results) 
        if self.numRows != 0: 
            print(f'{Fore.LIGHTCYAN_EX}ItemID. Item. Quantity. {Fore.YELLOW}Date Added. {Fore.RED}Expiration Date{Fore.RESET}')
            for x in results: 
                print(f'{x[0]}. {x[1]:3}: {x[2]:2} {Fore.YELLOW} {x[3]} {Fore.RED}{x[4]}{Fore.RESET}') 
        else:
            print("Your Fridge is empty add items.")
            self.numRows = False
        self.conn.commit()
        return self.numRows
   
    def updateItems(self,ingID,updatedQuant=None):
        '''Selects an item from the inventory table.
        User selects item with rowID and specifies updated quantity. 
        If updated quantity = 0 then it deletes the item from the table.'''
        if (ingID == 00):
            self.cur.execute('''DELETE FROM Inventory''')
            self.conn.commit()
        else: 
            try:
                self.cur.execute('''SELECT ItemID FROM Inventory WHERE RowID == ? ''', (ingID,))   
                results = self.cur.fetchone()
                if results == None:     
                    print("Item does not exist. Try again.")
                elif ingID in results: 
                    if updatedQuant > 0:
                        self.cur.execute('''UPDATE Inventory
                                    SET Quantity == ? WHERE RowID == ?''',
                                    (updatedQuant,ingID))
                    elif updatedQuant == 0:
                        print("Item Deleted")
                        self.cur.execute('''DELETE FROM Inventory WHERE RowID = ?''',(ingID,))
                self.conn.commit()
            except:
                print("Invalid Input. Try again.")  
    def closeDB(self):
        self.conn.close()

class Ingredient: 
    # Object classes to assign experation dates to ingredients 
    days = 7 
    def __init__(self):
        self.creationDate = datetime.now() 
    def expiration(self):
        expirationDate = self.creationDate + timedelta(self.days)
        return expirationDate.strftime("%A, %B %d %Y")
class Vegetable(Ingredient):
    days = 7 
class Meat(Ingredient):
    days = 3 
class Fruit(Ingredient):
    days = 5
class Grain(Ingredient):
    days = 4 

class MyRecipeDB: 
    # Handles Sqlite functions for the recipe table in sqlDB
    def __init__(self):
        self.ingList = []
        self.conn = sqlite3.connect("FakeIngredients.sql")
        self.cur = self.conn.cursor()
    def createTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS RecipeTable
                         (RecipeID Integer Primary Key NOT NULL, RecipeName TEXT, 
                         RecipeIngredients TEXT)''')
        self.conn.commit()
    def recipeDBFetchMethod(self):
        self.cur.execute('''SELECT * FROM RecipeTable''') 
        results = self.cur.fetchall()
        numRecipeRows = len(results) 
        if numRecipeRows != 0: 
            print(f'{Fore.LIGHTCYAN_EX}RecipeID. Recipe. RecipeIngredients.{Fore.RESET}')
            for x in results: 
                print(f'{x[0]}. {x[1]:3}: {x[2]} ') 
        else:
            print("No Current Recipes.")
            self.numRows = False
        self.conn.commit()
        return numRecipeRows
        
    def userAddRecipe(self,recipeName):
        try:     
            ingAmount = int(input("Enter the amount of ingredients: "))
            for num in range(ingAmount):
                ingName = input("Enter the ingredient: ") 
                self.ingList.append(ingName.strip())
            userRecipeIng = ' '.join(str(e) for e in self.ingList)
            self.cur.execute('''INSERT INTO RecipeTable (RecipeName,RecipeIngredients) VALUES (?,?)''',(recipeName,userRecipeIng))
            self.conn.commit()
        except:
            print("Invalid Input.")
    def userUpdateRecipes(self,recipeID,userChoice=None):      
        updateList = []  
        if recipeID == 00: 
            self.cur.execute('''DELETE FROM RecipeTable''')
            self.conn.commit()
        else: 
            try: 
                self.cur.execute('''SELECT RecipeID FROM RecipeTable WHERE RecipeID == ?''', (recipeID,))
                results = self.cur.fetchone()
                if results == None:     
                    print("Recipe does not exist. Try again.") 
                elif recipeID in results: 
                    if userChoice == 1:
                        numingredients = int(input("Enter the number of ingredients being added: "))
                        for num in range(numingredients):
                            ingName = input("Enter the Ingredient: ")
                            updateList.append(ingName.strip())
                            updateIng = ' '.join(str(e) for e in updateList)
                        self.cur.execute('''UPDATE Recipetable
                                    SET RecipeIngredients == RecipeIngredients || ? WHERE RecipeID == ?''',
                                    (updateIng,recipeID))
                    elif userChoice == 0:
                        print("Item Deleted")
                        self.cur.execute('''DELETE FROM RecipeTable WHERE RecipeID = ?''',(recipeID,))
                    self.conn.commit()
            except:
                print("Invalid Input.")
    def userViewAvailableRecipes(self):
        resultsList = []
        self.cur.execute('''SELECT * FROM RecipeTable''') 
        recipeResults = self.cur.fetchall()
        '''Selects all rows from Inventory table. For each row it will print each column then move to the next row.
        If the Inventory table is empty numRows returns False.'''
        self.cur.execute('''SELECT * FROM Inventory''') 
        ingResults = self.cur.fetchall()
        for index in range(len(ingResults)):
            resultsList.append(ingResults[index][1])
        for index in range(len(recipeResults)):
            recipeIngList = recipeResults[index][2].split()
            if (set(recipeIngList).issubset(set(resultsList))):
                print(f"{Fore.GREEN}Recipe: {recipeResults[index][1]} is available.{Fore.RESET}")
            else:
                print(f"{Fore.RED}Recipe: {recipeResults[index][1]} is not available. {Fore.RESET}")
           

userFridge = MyFridgeUI()

userFridge.run()
import sqlite3
from colorama import *
from datetime import * 

 

class MyFridgeUI:
    def __init__(self):
        self.userInput = 0 
        self.itemsData = {}
        self.userItems = []
        self.itemsQuantity = []   
        self.userDB = MyFridgeDB()    
        self.userRecipes = MyRecipeDB()
    

    def IntroUI(self):

        try: 
            print(f"{Style.BRIGHT}{Fore.GREEN}Welcome to MyFridge \nWhat would you like to do today.{Fore.RESET}")
            self.userInput = int(input(f"{Fore.LIGHTBLUE_EX}1. Add Items \n{Fore.YELLOW}2. Update/Remove Items  \n{Fore.CYAN}3. View Current Items \n{Fore.RESET}4. Add Recipes  \n5. View Saved Recipes  \n6. View Available Recipes \n7. Update/Remove Recipes   \n8. Quit \nEnter Here: "))
            if self.userInput == 1: 
                self.userDB.createTable()
                self.userAddItems()                 
                self.contOperation()  

            elif self.userInput == 2:     
                numRows = self.userDB.fetchMethod()
                if numRows != 0: 
                    print('''Which item would you like to update/remove? \nEnter 00 to clear all. ''')
                    ingID = int(input("Enter Here: "))
                    if (ingID == 00):
                        self.userDB.updateItems(ingID)
                    else: 
                        updatedQuant = int(input("Enter your updated quantity: "))
                        self.userDB.updateItems(ingID,updatedQuant)
                self.contOperation()                   

            elif self.userInput == 3: 
                print(f"{Fore.GREEN}\nHere are your current items{Fore.RESET}")
                self.userDB.fetchMethod()
                self.contOperation()
        
            elif self.userInput == 4: 
                self.userRecipes.createTable()
                recipeName = input("Enter the name of your recipe: ").capitalize()
                self.userRecipes.userAddRecipe(recipeName)
                self.contOperation()
            
            elif self.userInput == 5:
                self.userRecipes.recipeDBFetchMethod()
                
                self.contOperation()
            elif self.userInput == 6:
                self.userRecipes.userViewAvailableRecipes()
                self.contOperation()


            elif self.userInput == 7:
                numRecipeRows = self.userRecipes.recipeDBFetchMethod()
                if numRecipeRows != 0:
                    print('''Which recipe would you like to update/remove? \nEnter 00 to clear all. ''')
                    recipeID = int(input("Enter RecipeID Here: "))
                    if recipeID == 00:
                        self.userRecipes.userUpdateRecipes(recipeID)
                    else:  
                        userChoice = int(input("Would you like to update or remove (1/0): "))
                        self.userRecipes.userUpdateRecipes(recipeID,userChoice)
                self.contOperation()
            
            elif self.userInput == 8:
                print("Goodbye.")      
            else: 
                print("Invalid Entry. Try Again.")
                self.IntroUI()
        except Exception as e: 
            print(e)
            print("Try Again.")
            self.IntroUI()

    def contOperation(self):
        keepGoing = input("Would you like to continue operation? (Y/N): ")    
        if keepGoing.lower() == 'y':
            self.IntroUI()
        elif keepGoing.lower() == "n":
            print("Goodbye.")
        else: 
            print("Invalid Input. Try Again.")
            self.contOperation()
    
    def userAddItems(self):        
        userContinue = 'y'
        while userContinue.lower() == 'y':
            ingredient = self.userGetIngredient()   
            ingClassEXP = self.userGetClass()                     
            ingQuantity = self.userGetIngQuant()            
            
            self.userDB.addItems(ingredient,ingClassEXP,ingQuantity)          
            userContinue = input(f"{Fore.LIGHTBLUE_EX}Would you like to continue adding items? (Y/N): {Fore.RESET}")            
            if (userContinue.lower() != 'y') and (userContinue.lower() != 'n'):
                print(f"{Fore.RED}Try again!")
                userContinue = input(f"{Fore.LIGHTBLUE_EX}Would you like to continue adding items? (Y/N): {Fore.RESET}")        

    def userGetIngredient(self):
        while True: 
            ingredient = (input(f"{Fore.LIGHTBLUE_EX}Add your Items (One at a time): {Fore.RESET}"))
            if (ingredient.isdigit() is False) and (ingredient != '') and not ingredient.isspace():
                return ingredient.capitalize() 
            else: 
                print("Try Again") 
                continue  

    def userGetClass(self):
        while True: 
            ingClass = input(f"Select your item class:\n1. Vegetable \n2. Meat \n3. Fruit \n4. Grain \nEnter Here: ")
            match ingClass: 
                case "1":
                    ingClass = Vegetable()
                    return ingClass.expiration()
                case "2":
                    ingClass = Meat()
                    return ingClass.expiration()
                case "3":
                    ingClass = Fruit()
                    return ingClass.expiration()
                case "4":
                    ingClass = Grain()
                    return ingClass.expiration()
    def userGetIngQuant(self):
        while True: 
            ingQuantity = input(f"{Fore.LIGHTBLUE_EX}Enter the Quantity: {Fore.RESET}")
            try: 
                ingQuantity = int(ingQuantity)
                if ingQuantity > 0:
                    return ingQuantity
                else: 
                    continue
            except ValueError:
                print(f"{Fore.LIGHTBLUE_EX}Try again!{Fore.RESET}")
                continue       
    
    def run(self):
        self.IntroUI()

class MyFridgeDB: 
    def __init__(self):
        self.conn = sqlite3.connect("FakeIngredients.sql")
        self.cur = self.conn.cursor()
    def createTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Inventory
                         (ItemID Integer Primary Key NOT NULL, IngredientName TEXT NOT NULL, 
                         Quantity INTEGER, Date TIMESTAMP, ExpDate TIMESTAMP)''')
        self.conn.commit()

    def addItems(self,ingredient,ingClassEXP,ingQuantity):
        ingCreationDate = datetime.today()
        self.cur.execute('''INSERT INTO Inventory (IngredientName, Quantity, Date, ExpDate)
                            VALUES (?,?,?,?)''',
                            (ingredient,ingQuantity,ingCreationDate.strftime("%A, %B %d %Y"),ingClassEXP))
        self.conn.commit()
   
    def fetchMethod(self):
        '''Selects all rows from Inventory table. For each row it will print each column then move to the next row.
        If the Inventory table is empty numRows returns False.'''
        self.cur.execute('''SELECT * FROM Inventory''') 
        results = self.cur.fetchall()
        self.numRows = len(results) 
        if self.numRows != 0: 
            print(f'{Fore.LIGHTCYAN_EX}ItemID. Item. Quantity. {Fore.YELLOW}Date Added. {Fore.RED}Expiration Date{Fore.RESET}')
            for x in results: 
                print(f'{x[0]}. {x[1]:3}: {x[2]:2} {Fore.YELLOW} {x[3]} {Fore.RED}{x[4]}{Fore.RESET}') 
        else:
            print("Your Fridge is empty add items.")
            self.numRows = False
        self.conn.commit()
        return self.numRows
   
    def updateItems(self,ingID,updatedQuant=None):
        '''Selects an item from the inventory table.
        User selects item with rowID and specifies updated quantity. 
        If updated quantity = 0 then it deletes the item from the table.'''
        if (ingID == 00):
            self.cur.execute('''DELETE FROM Inventory''')
            self.conn.commit()
        else: 
            try:
                self.cur.execute('''SELECT ItemID FROM Inventory WHERE RowID == ? ''', (ingID,))   
                results = self.cur.fetchone()
                if results == None:     
                    print("Item does not exist. Try again.")
                elif ingID in results: 
                    if updatedQuant > 0:
                        self.cur.execute('''UPDATE Inventory
                                    SET Quantity == ? WHERE RowID == ?''',
                                    (updatedQuant,ingID))
                    elif updatedQuant == 0:
                        print("Item Deleted")
                        self.cur.execute('''DELETE FROM Inventory WHERE RowID = ?''',(ingID,))
                self.conn.commit()
            except:
                print("Invalid Input. Try again.")  
    def closeDB(self):
        self.conn.close()

class Ingredient: 
    # Object classes to assign experation dates to ingredients 
    days = 7 
    def __init__(self):
        self.creationDate = datetime.now() 
    def expiration(self):
        expirationDate = self.creationDate + timedelta(self.days)
        return expirationDate.strftime("%A, %B %d %Y")
class Vegetable(Ingredient):
    days = 7 
class Meat(Ingredient):
    days = 3 
class Fruit(Ingredient):
    days = 5
class Grain(Ingredient):
    days = 4 

           

userFridge = MyFridgeUI()

userFridge.run()
