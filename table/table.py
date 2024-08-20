def print_multiplication_table(number, up_to=10):
    """
    Prints the multiplication table for a given number up to a specified range.

    Parameters:
    - number: The number for which the multiplication table is to be generated.
    - up_to: The range up to which the multiplication table should be printed.
    """
    print(f"Multiplication Table for {number}:")
    for i in range(1, up_to + 1):
        result = number * i
        print(f"{number} x {i} = {result}")

def main():
    try:
        number = int(input("Enter the number for which you want to generate the multiplication table: "))
        up_to = int(input("Enter the range up to which you want the table (default is 10): ") or 10)
        print_multiplication_table(number, up_to)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
