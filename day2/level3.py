import level2
choice = input("Are you under 87A rebate yes or no")
if choice == 'yes' and level2.taxable_income <= 700000:
    print(f"the taxable amount is {level2.taxable_income}")
    
elif level2.taxable_income <= 300000:
    print(f"the taxable amount is {level2.taxable_income}")
    
elif level2.taxable_income <= 600000:
    level2.taxable_income += (5/100)* level2.taxable_income
    print(f"the taxable amount is {level2.taxable_income}")
    
elif level2.taxable_income <= 900000:
    level2.taxable_income += (10/100)* level2.taxable_income
    print(f"the taxable amount is {level2.taxable_income}")
elif level2.taxable_income <= 1200000:
    level2.taxable_income += (15/100)* level2.taxable_income
    print(f"the taxable amount is {level2.taxable_income}")    
elif level2.taxable_income <= 1500000:
    level2.taxable_income += (20/100)* level2.taxable_income
    print(f"the taxable amount is {level2.taxable_income}")
else:
    level2.taxable_income += (30/100)* level2.taxable_income
    print(f"the taxable amount is {level2.taxable_income}")

health = level2.taxable_income + (4/100)*level2.taxable_income    
level2.taxable_income += health
print(f"the total tax amount is {level2.taxable_income}")
 