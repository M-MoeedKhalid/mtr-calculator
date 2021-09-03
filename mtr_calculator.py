import requests


# Function to calculate tax per bracket and total tax
def get_tax(salary, tax_bracks):
    salary_per_bracket = dict()
    total_tax = 0
    # Loop over each individual bracket
    for idx, tax_br in enumerate(tax_bracks):

        # Get current bracket values
        bracket_min = tax_br['min']
        rate = tax_br['rate']
        bracket_max = tax_br.get('max')

        # Terminating condition | If we are in the last bracket or the salary lies
        # in current bracket. We cant use "range" for comparison of salary as
        # we might deal with salary in floats
        if (idx == len(tax_bracks) - 1) or (bracket_min < salary < bracket_max):
            salary_per_bracket[str(idx + 1)] = round((salary - bracket_min) * rate, 2)
            total_tax = total_tax + salary_per_bracket[str(idx + 1)]
            return round(total_tax, 2), salary_per_bracket

        # Otherwise just update total salary and the bands
        else:
            salary_per_bracket[str(idx + 1)] = round((bracket_max - bracket_min) * rate, 2)
            total_tax = total_tax + salary_per_bracket[str(idx + 1)]


# Function that validates the input salary and displays the taxes + ER
def tax_calculator(tax_brackets):
    # Basic while loop validation until a valid salary is entered or a terminating
    # condition (entering) is met
    while True:
        try:
            input_salary = input("Please Enter your salary in CAD or"
                                 " Enter X to go back to the previous Menu ")
            if input_salary == 'X':
                break
            input_salary = float(input_salary)
            if input_salary <= 0:
                raise ValueError
            tax, bands = get_tax(input_salary, tax_brackets)

            # Printing Final result
            print(f"Your Total tax is {tax} CAD")
            for key, value in bands.items():
                print(f"Your Tax for bracket {key} is {value} CAD")
            print(f'The Effective Tax Rate is {round((tax / input_salary) * 100, 2)}% \n')
            break
        except ValueError:
            print('Error : Make sure you enter a valid numeric Salary greater than 0 or enter X to exit'
                  '\n')
        except Exception:
            print("There was an internal error. Please contact the system administrator")


# # Function that validates the input URL and calls to calculate taxes
def tax_calculator_by_year(url):
    # Basic while loop validation until a year and a valid salary is entered or a terminating
    # condition (entering X) is met
    while True:
        try:
            print("Enter the year you want to get tax for E.g. 2019: or enter X to exit ")
            year = input()
            if year == 'X':
                break
            if int(year) not in range(1900, 2100):
                raise ValueError

            res = requests.get(url + f'{str(year)}/')
            yearly_tax_brackets = res.json()['tax_brackets']
            tax_calculator(yearly_tax_brackets)
            break
        except ValueError:
            print('Please enter a valid year (b/w 1900 - 2100)')
        except KeyError:
            print(res.json()['errors'][0]['message'])
        except Exception:
            print("There was an internal error. Please contact the system administrator")


# Menu printing and looping in main
def main():
    user_input = 1
    url = 'http://localhost:5000/tax-calculator/brackets/'

    # We store the base URL tax brackets at the start rather than calling the API on every iteration
    # This saves us time as well as excessive API calls
    response = requests.get(url)
    tax_brackets = response.json()['tax_brackets']

    print("-----Welcome to your very own Marginal Tax Rate calculator-----")
    while user_input != 3:
        print("Press 1 to calculate tax according to the marginal tax rates 2020"
              "\nPress 2 to calculate tax for a specific year"
              "\nPress 3 to exit")
        user_input = input()
        if user_input == '1':
            tax_calculator(tax_brackets)
        elif user_input == '2':
            tax_calculator_by_year(url)
        elif user_input == '3':
            break
        else:
            print("Please enter an option from the menu")
    print("Thank you for using our tax calculator!")


if __name__ == "__main__":
    main()
