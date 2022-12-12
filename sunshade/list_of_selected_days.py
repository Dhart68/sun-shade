def list_of_selected_days(start = '2021-01-03', end = '2021-12-26', n=2):
     # List of day of the year given a starting and endind day and a number of dates  
       
    day_list=pd.date_range(start, end,n) # 52 for all year, use 2, 4, 8 to test
    
    return day_list
