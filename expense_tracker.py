import csv
import os

menu = ['Add Expense', 'View Expenses', 'Filter by Category', 'Total Spent', 'Highest Spending Category', 'Exit']

print('Welcome to Personal Expense Tracker!')

for i, option in enumerate(menu):
    print(f'{i+1}. {option}')

def load_from_csv():
  data = []
  filename = 'data/expense.csv'
  file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
  if not file_exists:
    return data
  with open(filename, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
      data.append(dict(row))
  return data

expenses = load_from_csv()

def input_category():
  category = input('Enter expense category: ')
  if len(category.strip()) <= 0:
    print('*can\'t leave blank category!')
    return input_category()
  else:
    return category
  
def input_amount():
  amount = input('Enter expense amount: ')
  if len(amount.strip()) <= 0:
    print('*can\'t leave blank amount!')
    return input_amount()
  elif not amount.isdecimal():
    print('*amount should be numeric!')
    return input_amount()
  else:
    return amount
  
def input_date():
  date = input('Enter expense date (YYYY-MM-DD): ')
  if len(date.strip()) <= 0:
    print('*can\'t leave blank date!')
    return input_date()
  elif not len(date) == 10 or date[4] != '-' or date[7] != '-':
    print('*incorrect length or missing dashes, format should be like (YYYY-MM-DD)!')
    return input_date()
  else:
    return date

def save_in_csv(expense):
  filename = 'data/expense.csv'
  file_exists = os.path.isfile(filename) and os.path.getsize(filename) > 0
  with open(filename, mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=expense.keys())
    if not file_exists:
      writer.writeheader()
    writer.writerows([expense])
    
def expense_tracker(expenses):
  expense = {}
  print('---------------------------------------------')
  user_opt = input('Enter option number: ')
  print('---------------------------------------------')
  
  if user_opt == '1':
    print('Add Expense')
    category = input_category()
    amount = input_amount()
    date = input_date()
    expense['category'] = category.title()
    expense['amount'] = float(amount)
    expense['date'] = date
    expenses.append(expense)
    save_in_csv(expense)
    print('Expense added successfully!')
    expense_tracker(expenses)
  elif user_opt == '2':
    print('View Expenses')
    for expense in expenses:
      print(f"{expense['category']} - {expense['date']}\n{expense['amount']}")
    expense_tracker(expenses)
  elif user_opt == '3':
    print('Filter by Category')
    asked_category = input('Enter category: ')
    isCategoryAvailable = False
    for expense in expenses:
      if asked_category.lower() == expense['category'].lower():
        print(f"{expense['category']} - {expense['date']}\n{expense['amount']}")
        isCategoryAvailable = True
    if isCategoryAvailable == False:
      print(f'{asked_category} not found.')
    expense_tracker(expenses)
  elif user_opt == '4':
    total_expense = 0
    for expense in expenses:
      total_expense += float(expense['amount'])    
    print(f'Total Spent: {total_expense}')
    expense_tracker(expenses)
  elif user_opt == '5':
    print('Highest Spending Category')
    total_categories_expense = dict()
    for expense in expenses:
      category = expense['category']
      if category in total_categories_expense:
        total_categories_expense[category] += float(expense['amount'])
      else:
        total_categories_expense[category] = float(expense['amount'])
    print(f'{max(total_categories_expense, key=total_categories_expense.get)} - (Spending: {total_categories_expense[max(total_categories_expense, key=total_categories_expense.get)]})')
    expense_tracker(expenses)
  elif user_opt == '6':
    print('Exited')
  else:
    print('Invalid Option!')
    expense_tracker(expenses)

expense_tracker(expenses)