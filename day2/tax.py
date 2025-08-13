emp_Name = input("enter the name of the employee: ")
emp_Id = int(input("enter the id of the employee: "))
basic_salary=int(input("enter the salary of the employee: "))
special_allowances = int(input("enter the special allowance of the employee: "))
bonus = int(input("enter the bonus percentage of the employee: "))
gross_monthly_salary = basic_salary + special_allowances
annual_gross_salary = (gross_monthly_salary * 12) + (bonus / 100) * basic_salary
print(f"the gross salary of an employee is: {gross_monthly_salary} ")
print(f"the gross salary of an employee is: {annual_gross_salary} ")