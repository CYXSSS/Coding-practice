# Ask the user for their age
age = int(input("Please enter your age: "))
if age >= 21:
    print("You are eligible to vote.")
elif 13 <= age <= 20:
    print("You are a teenager.")
elif 0 <= age < 13:
    print("You are a child.")
else:
    print("Invalid age entered.")

# Use a while loop to count down from 5 to 1
count = 5
while count > 0:
    print(count)
    count -= 1
print("Countdown finished!")

# Initialize the list of names
names = ["Alice", "Bob", "Charlie", "David"]
for name in names:
    print(f"Hello, {name}!")
print("All names have been greeted.")

# Skip negative numbers
# Stop the loop if a number greater than 10 is encountered
numbers = [1, -3, 5, -7, 11, -13, 17]
for num in numbers:
    if num < 0:
        continue
    if num > 10:
        break
    print(num)
    