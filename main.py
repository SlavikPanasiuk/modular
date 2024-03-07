from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Expense(BaseModel):
    amount: int
    time: datetime
    category: str
    description: str

class Income(BaseModel):
    amount: int
    time: datetime
    category: str
    description: str

account_balance = 0
finances = {}

@app.post("/post_expense")
def post_expense(expense: Expense):
    global account_balance
    global finances
    
    if expense.amount < 0:
         return {"Не можна додати витрату, розмір якої менше 0"}
    account_balance -= expense.amount
    expnse_id = len(finances)
    finances[expnse_id] = expense
    print(type(expense))
    return {"massage": "result add"}

@app.post("/post_income")
def post_income(income: Income):
    global account_balance
    global finances
    
    if income.amount < 0:
        return {"Не можна додати дохід, розмір якого менше 0"}
    account_balance += income.amount
    income_id = len(finances)
    finances[income_id] = income
    return {"massage": "result add"}

@app.put("/put_expense/{finances_id}")
def update_expense(finances_id: int, expanse: Expense):
    for k, v in finances.items():
        if k == finances_id:
            finances[finances_id] = expanse
  
            
@app.put("/put_income/{finances_id}")
def update_income(finances_id: int, income: Income):
    for k, v in finances.items():
        if k == finances_id:
            finances[finances_id] = income
            
          
@app.get("/category/{category}")
def get_category(category: str):
    list_cat = []
    for key, value in finances.items():
        if value.category == category:
            list_cat.append(value)
    return list_cat

@app.get("/balance")
def get_balanse():
    return account_balance

@app.get("/get_finances")
def get_finances():
    return finances
         
@app.delete("/delete_finance/{finances_id}")
def delete_finance(finances_id: int):
    del finances[finances_id]            

@app.delete("/delelte_all")
def delete_all():
    global account_balance
    finances.clear()
    account_balance = 0    

@app.get("/statistics")
def statistics(start_date: datetime, end_date: datetime): 
    result = {}
    new_finances = {}
    for k, v in finances.items():
        if v.time <= end_date and v.time >= start_date:
            new_finances[k] = v
    
    new_expenses = {}
    for k, v in new_finances.items():
        if "Expense" in str(type(v)):
            new_expenses[k] = v
    
    new_income = {}
    for k, v in new_finances.items():
        if "Income" in str(type(v)):
            new_income[k] = v
    
    expense_cat = set()
    for k, v in new_expenses.items():        
        expense_cat.add(v.category)
        
    income_cat = set()
    for k, v in new_income.items():
        income_cat.add(v.category)    
       
    for current_cat in expense_cat:
        count_expenses = 0
        sum_expense = 0
        min_expense = 1000000
        max_expense = -9999999
        for k, v in new_expenses.items():
            if v.category == current_cat:
                count_expenses += 1
                min_expense = min(min_expense, v.amount)
                max_expense = max(max_expense, v.amount)
                sum_expense += v.amount
        mean_expense = sum_expense / count_expenses   
        result[f"{current_cat}_expense"] = {"count": count_expenses, "mean": mean_expense, "min": min_expense, "max": max_expense}
        
    for current_cat in income_cat:
        count_income = 0
        sum_income = 0
        min_income = 1000000
        max_income = -9999999
        for k, v in new_income.items():
            if v.category == current_cat:
                count_income += 1
                min_income = min(min_income, v.amount)
                max_income = max(max_income, v.amount)
                sum_income += v.amount
        mean_income = sum_income / count_income   
        result[f"{current_cat}_income"] = {"count": count_income, "mean": mean_income, "min": min_income, "max": max_income}
              
    return result
                
                   
        
        
        
        
           
        
   
       