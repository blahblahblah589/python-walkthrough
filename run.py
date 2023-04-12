import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    """
    Get sales figures input from user
    """
    print("please enter sales data from last market.")
    print("Data should be six numbers, sepparated by a comma.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter data here:")
    
    sales_data = data_str.split(",")
    validate_data(sales_data)
    

def validate_data(values):
    """
    Convert all string values into integers, throws error if 
    cannot be converted or not 6 values
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, {len(values) provided}."
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_sales_data()