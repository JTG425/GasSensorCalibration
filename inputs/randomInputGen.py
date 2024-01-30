import random

class randomInputGen():
    # Function to generate random numbers with a step between 0.05 and 0.10
    def generate_random_numbers(start, count):
        numbers = [start]
        for _ in range(count - 1):
            start += random.uniform(0.05, 0.10)
            numbers.append(start)
        return numbers

    # Generate 100 random numbers starting from 0
    random_numbers = generate_random_numbers(0, 100)

    # Write the numbers to a data file
    with open('data.txt', 'w') as file:
        for number in random_numbers:
            file.write(f"{number:.2f}\n")

    print("Random numbers written to 'data.txt'")
