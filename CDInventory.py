#------------------------------------------#
# Title: Assignment07_Starter.py
# Desc: Working with classes and functions.
# Change Log: Vakhtang Gurasashvili
# 2020-Aug-28, Created File
#------------------------------------------#

# -- DATA -- #
import pickle
strChoice = '' # User input
lstTbl = []   #List of Dictionaries
dicRow = {}  # User Data Input Dictionary
strFileName = 'CDInventory.txt'  # data storage file
Bnr_Filename = 'CDInventory.dat'
objFile = '' # file object
Usr_Choice = ''
e= ''
# -- PROCESSING -- #
class DataProcessor:
    @staticmethod 
    def data_add(data, table):
        dicRow = {}
        dicRow['ID'] = (data[0])
        dicRow['Title'] = (data[1])
        dicRow['Artist'] =(data[2])
#       global lstT                  just for records :)
        table.append(dicRow)
        return table
    
    @staticmethod 
    def data_del(table, intIDDel):
        #show_inventory(lstTbl)
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        # 3.5.1.2 ask user which ID to remove
        # 3.5.2 search thru table and delete CD
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                   del lstTbl[intRowNr]
                   blnCDRemoved = True
                   break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
    
    @staticmethod
    def table_clear(table):
        table.clear()
        

class FileProcessor:
    """Processing the data to and from text file"""
    @staticmethod
    def read_file(FileName, table):
            dicRow ={}
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
            strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled  :')
            if strYesNo.lower() == 'yes':
                print('reloading...')
                table.clear()  # this clears existing data and allows to load data from file
                
                try:
                    with open(FileName) as objFile:
                        for line in objFile:
                            data = line.strip().split(',')
                            dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                            table.append(dicRow)
                    return table
                except FileNotFoundError as e :
                    print()
                    print('File Not Found')
                    print(e)
                    print()
                    print()
                return None

            else:
                input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(table)
    
    @staticmethod
    def write_file(FileName, table):
        # 3.6.1 Display current inventory and ask user for confirmation to save
        
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            try:
                objFile = open(FileName, 'a')
                for row in lstTbl:
                    lstValues = list(row.values())
                    lstValues[0] = str(lstValues[0])
                    objFile.write(','.join(lstValues) + '\n')
            except Exception :
                print('THERE WAS AN ERROR IN PROCESSING REQUEST')
            finally:
                objFile.close()
            print('data successfully saved'.upper())
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
    
    @staticmethod
    def pickle_processor_dump(FileName, table):
        with open(FileName, 'wb') as objFile:
            pickle.dump(table, objFile)
    @staticmethod
    def pickle_processor_load(FileName, table):
        try:
            with open(FileName, 'rb') as objFile:
                table = pickle.load(objFile)
                table = list(table)
                print(type(table))
                return table
        except FileNotFoundError as e :
            print()
            print('File Not Found')
            print(e)
            print()
            print()
            return None

            # -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""
    @staticmethod
    def print_menu():
        print()
        print()
        print('{:*^60}'.format('Welcome To CD_Inventory Menu'))
        print()
        print('{:@^60}'.format('  Please Make Your Choice  '))
        print("""
              A) ADD NEW ENTRY
              
              I) DISPLAY CURRENT INVENTORY

              S) SAVE DATA TO fILE
              
              L) LOAD DATA FROM FILE
          
              D) DELETE DATA FROM INVENTORY
              
              B) LOAD/DUMP TO/FROM FILE IN BINARY MODE
              
              X) EXIT tHE PROGRAMM
                                              """)

    @staticmethod
    def menu_choice():
        choice = ''
        while choice not in ['l', 'a', 'i', 'd', 's', 'x','b']:
            choice = input('Which operation would you like to perform? [l, a, i, d, b, s or x]: ').lower().strip()
            print()  # Add extra space for layout
        return choice
    
    @staticmethod
    def usr_del():
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print('this is not a valid value fo id'.upper())
            print()
            print(e)
            print()
            return IO.usr_del()
        else:
            return intIDDel
    
    @staticmethod
    def usr_input():
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        try:
            int(strID)
            return int(strID), strTitle, stArtist
        except ValueError as v:
            print()
            print('The Id You Entered Is Not A Number')
            print()
            print(v)
            return IO.usr_input()
    
    @staticmethod
    def show_inventory(lsttab):
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in lsttab:
            print('{:<6}{:^20}{:20}'.format(row['ID'], row['Title'], row['Artist']))
        print('======================================')
    @staticmethod
    def pickle_Choice():
        print(' please choose to load/dump data from/to file'.title())
        print()
        print('for save data to file press : "s"\n\n'.upper() + 'for load data press : "l"'.upper())
        print()
        Usr_Choice = input()
        
        return Usr_Choice

# M A I N   B O D Y
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)
IO.show_inventory(lstTbl)
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        FileProcessor.read_file(strFileName, lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        dtpl=IO.usr_input()
        DataProcessor.data_add(dtpl, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        IO.show_inventory(lstTbl)
        DataProcessor.data_del(lstTbl, IO.usr_del())
    elif strChoice == 's':
        
        # 3.6.1 Display current inventory and ask user for confirmation to save
        FileProcessor.write_file(strFileName, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    
    # There is some problems with this block below, currently working on it , dump section works but load section doesn't operates as intended
    #3.8dump/ load data in binary mode
    elif strChoice == 'b':        
        Usr_Choice = IO.pickle_Choice()
       
        if Usr_Choice == 's':
            FileProcessor.pickle_processor_dump(Bnr_Filename, lstTbl)
            continue
        
        elif Usr_Choice == 'l':
            a = FileProcessor.pickle_processor_load(Bnr_Filename, lstTbl)
            lstTbl.append(a)
            continue
    else:
        print('General Error')



