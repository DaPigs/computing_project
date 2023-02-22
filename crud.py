import sqlite3
from tables import *

def main():
  #Connecting to sqlite
  cnt = sqlite3.connect("data.db")

  def sql(S):
      cur = cnt.execute(S)
      cnt.commit()
      return cur.fetchall()

  #Creating a cursor object using the cursor() method
  cursor = cnt.cursor()

  #CREATE
  #list of records to insert/create
  # records = [(...,...,...),(...,...,...)...]
  # def create(records) # pass a list of tuples as values to repalce the placeholder (?,?,?)
  #  query = "INSERT INTO <table> VALUES (?,?,?)"
  #  cursor.execute(query,records)
  # ...

  #READ
  # def read(,table):
  # query = "SELECT field 1, field 2, …FROM f"{table}""

  #UPDATE
  # def update():
  #   query = "UPDATE <table name> SET field1=value1, field2=value2,… [WHERE <condition>]"

  # #DELETE
  # def delete():
  #   query = "DELETE FROM <table name> [WHERE <condition>]"

  #some context of tables for users
  #no need bruh

  #user menu + input choice of CRUD (create, read, update, delete)

  runprogramme = True

  while runprogramme == True:
    print("Menu: \n(1)Create \n(2)Read \n(3)Update \n(4)Delete \n(5)Exit \n")
    CRUD_choice = int(input("What would you like to do? "))

    if CRUD_choice == 1:  #create
      # choose table via input
      table_choice = input(f"Please select a table to add a record({', '.join(table_dict.keys())}): ").lower()
      # insert in values via input and make a list
      record = []
      for i in table_dict[table_choice].items:
        record.append(f"Please input {i}: ")

      #insert in values into the table of choice
      record = tuple(record)
      query = f"INSERT INTO {table_choice} VALUES {record}"
      sql(query)

      #print the updated table
      showtable = sql(f"SELECT * FROM {table_choice};")  #returns a list
      for row in showtable:
        print(str(table_dict[table_choice](*row)), end="\n\n")

    elif CRUD_choice == 2:  #read
      #select a table
      table_choice = input(f"Please select a table to view records({', '.join(table_dict.keys())}): ").lower()
      #select all from table and display
      cursor.execute(f"SELECT * FROM {table_choice};")
      showtable = cursor.fetchall()
      for row in showtable:
        print(str(table_dict[table_choice](*row)), end="\n\n")

    elif CRUD_choice == 3:  #update
      table_choice = input(f"From which table do you want to update? {', '.join(table_dict.keys())}").lower()
      condition = input(f"Choose from which record do you want to update. When <field> = ... (eg. type 'StudentID = 2' ) {table_dict[table_choice].items}")
      field_update_choice = input(f"Which field do you want to update? {table_dict[table_choice].items}")
      update_specifics = input("what do you want to change this field in this record to? ")
      set_choice = f"{field_update_choice} = '{update_specifics}'"
      update_query = f"UPDATE {table_choice} SET {set_choice} WHERE {condition};"

      print(update_query)
      cursor.execute(update_query)
      print("Update successful! ")
      cursor.execute(f"SELECT * FROM {table_choice};")
      showtable = cursor.fetchall()  #returns a list
      for row in showtable:
        print(str(table_dict[table_choice](*row)), end="\n\n")

    elif CRUD_choice == 4:  #delete
      table_choice = input(f"From which table do you want to update? {', '.join(table_dict.keys())}").lower()
      condition = input(f"Choose which record you want to delete. When <field> = ... (eg. type 'StudentID = 2' ) {table_dict[table_choice].items}")
      delete_query = f"DELETE FROM {table_choice} WHERE {condition}"

      print(delete_query)
      cursor.execute(delete_query)
      print("Delete successful! ")
      cursor.execute(f"SELECT * FROM {table_choice};")
      showtable = cursor.fetchall()  #returns a list
      for row in showtable:
        print(str(table_dict[table_choice](*row)), end="\n\n")

    else:  #exit
      runprogramme = False

    # Commit your changes in the database
    cnt.commit()

  cnt.close()
  print("Exited. Thank you for using our service. 👍")
if(__name__ == "__main__"):
  main()