Select [col]
From [table]
Where [condition] # filter rows
Group By [col]
Having [groupby_col_calculation_condition] # filter group
Order by [col] [Desc], [col] 

# NULL
Coalesce([col],0) # replace null with 0

# Select 
Count(Distinct [col])
5 div 2 # return 2
5 mod 2 # retun 1

# String Operations
replace('abcd','ab','AB') # return ABcd
left('character', 4) # return char
substring('character' from 4 for 2) # return ra

# Date Operations
Datediff(Date1, Date2) # Date1 - Date2
Date_format('2025-07-25','%Y/%b/%d') # return 2025/Jul/25

# Filter string in Where, %任意字符任意长度, _任意单个字符 ~ .
Where Name Like '%a%' # Name contains a
Where Name Like 'a_'  # Name contains two characters and starts with a
Where Name Like '[BC]%' # Name starts with B or C
Where Name Like '[^A]%' # Name not starts with A
Where Name Like '%\%%' Escape '\' # Name contains %

Where Name Regexp '^[a-z].*ck$' # Name starts with any from a to z and end with ck, * = ? & +

Where REGEXP_LIKE(mail, '^[A-Za-z][A-Za-z0-9_.-]*@leetcode\[.]com$', 'c') # email starts with a letter, email string may contain letters (upper or lower case), digits, underscore '_', period '.', and/or dash '-' and domain is leetcode.com

# Exists
Select w.name
From Websites As w
Where Exists (Select * From access_log as l Where l.site_id=w.id and l.count>200) # return name of website which has more than 200 visits

# Case When
Select SUM(CASE WHEN product_type = 'clothes' THEN Unit ELSE 0 END) As sum_unit_clothes, SUM(CASE WHEN product_type = 'shoes' THEN Unit ELSE 0 END) As sum_unit_shoes
From Product

# Window Function
- Aggregation function: SUM, AVG, COUNT, MAX, MIN
- RANK, DENSE_RANK, ROW_NUMBER
Window Function OVER ([PARTITION BY [COLS]] ORDER GY [COLS])

** Compute the moving average of how much the customer paid in a 7 days window **
With cte as (
    Select visited_on, sum(amount) as daily_amount
    From Customer
    Group By visited_on
)

Select visited_on,
    sum(daily_amount) over (order by visited_on Rows Between 6 Preceding and Current Row) as amount,
    round(avg(daily_amount) over (order by visited_on Rows Between 6 Preceding and Current Row), 2) as average_amount
From cte
Limit 1000 Offset 6

