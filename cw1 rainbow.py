import hashlib
import random
import string

# Define the reduce function
def reduce_function(hashed, pass_length):
    result = ""
    for i in range(pass_length):
        result += chr(ord('a') + hashed % 26)
        hashed //= 26
    return result

# Create a random password of a specified size
def create_password(size):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(size))

# Build a rainbow table
def build_rainbow_table(chain_amount, chain_size, pass_length):
    r_table = {}
    for i in range(chain_amount):
        passw = create_password(pass_length)
        hashed_pass = hashlib.md5(passw.encode()).hexdigest()
        reducedd_pass = passw
        for j in range(chain_size):
            hashed_pass = hashlib.md5(reducedd_pass.encode()).hexdigest()
            reducedd_pass = reduce_function(int(hashed_pass, 16), pass_length)
        r_table[hashed_pass] = (passw, reducedd_pass)
    return r_table

# Decrypt the password
def decrypt_pass(hash_val, r_table):
    pass_length = 8
    chain_size = 1000
    if hash_val in r_table:
        passw, reduced_pass = r_table[hash_val]
        for i in range(chain_size):
            if reduce_function(int(hash_val, 16), pass_length) == reduced_pass:
                return passw
            hash_val = hashlib.md5(reduce_function(int(hash_val, 16), pass_length).encode()).hexdigest()
        return "Password not found."
    else:
        return "Sorry, the hash value is not found in the rainbow table."

# Build the rainbow table
chain_amount = 1000
chain_size = 1000
pass_length = 8
r_table = build_rainbow_table(chain_amount, chain_size, pass_length)

# Display the rainbow table in the desired format
print("Rainbow Table:")
for hashed_pass in sorted(r_table.keys()):
    passw, reduced_pass = r_table[hashed_pass]
    print(hashed_pass, reduced_pass, passw)

# Ask the user to enter an MD5 hash value to crack
hash_val = input("Enter an MD5 hash value to be checked: ")
if hash_val:
    passw = decrypt_pass(hash_val, r_table)
    if passw != "Password not found.":
        print("The plaintext password is:", passw)
    else:
        print("Sorry, the password could not be found in the rainbow table.")
else:
    print("No hash value was entered.")
