#Task 3
import csv
employees_data = []
with open('python_homework-1/csv/employees.csv', mode='r', newline='') as file:
  reader = csv.reader(file)
  employees_data = list(reader)

full_names = [f"{row[0]} {row[1]}" for row in employees_data[1:]]

print("--- Full Names ---")
print(full_names)

names_with_e = [name for name in full_names if "e" in name.lower()]

print("\n--- Names containing 'e' ---")
print(names_with_e)
