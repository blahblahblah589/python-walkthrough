import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("please enter sales data from last market.")
        print("Data should be six numbers, sepparated by a comma.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter data here:")
    
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data valid")
            break

    return sales_data


def validate_data(values):
    """
    Convert all string values into integers, throws error if 
    cannot be converted or not 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, {len(values)} provided."
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


# def update_sales_worksheet(data):
#     """
#     Update sales data worksheet, add new row with list data provided
#     """
#     print("Update sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated.\n")


# def update_surplus_worksheet(data):
#     """
#     Update surplus data worksheet, add new row with list data provided
#     """
#     print("update surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated.\n")


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet) 
    worksheet_to_update.append_row(data)
    print(f'Worksheet {worksheet} updated.\n')


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def get_last_five_sales():
    """
    Collect collumn of data from sales worksheet, collecting 
    last five entries for each sandwich and 
    returns the data as a list of lists 
    """
    sales = SHEET.worksheet("sales")
   

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("welcome to Love Sandwiches Data Automation")
# main()
get_last_five_sales()

sales_columns = get_last_five_sales()