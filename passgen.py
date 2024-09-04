import random
import string
def generate_password(length, use_uppercase = True, use_lowercase = True, use_numbers = True, use_special_chars = True):
    if length < 1:
        raise ValueError("Password length needs to be at least 1.")
    
    char_pool = ''
    
    if use_uppercase:
        char_pool += string.ascii_uppercase
    if use_lowercase:
        char_pool += string.ascii_lowercase
    if use_numbers:
        char_pool += string.digits
    if use_special_chars:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("You have to choose at least one category.")
    
    password = ''.join(random.choice(char_pool) for _ in range(length))
    return password

def get_user_input():
    length = int(input("Write down the password length you wish: "))
    use_uppercase = input("Capital letters? y/n: ").lower() == 'y'
    use_lowercase = input("Small letters? y/n: ").lower() == 'y'
    use_numbers = input("Numbers? y/n: ").lower() == 'y'
    use_special_chars = input("Symbols? y/n: ").lower() == 'y'
    
    return length, use_uppercase, use_lowercase, use_numbers, use_special_chars

def main(session):
    length, use_uppercase, use_lowercase, use_numbers, use_special_chars = get_user_input()
    password = session.generate(length, use_uppercase, use_lowercase, use_numbers, use_special_chars)
    if password:
        print(f"Generated password: {password}")
        print(f"Password strength: {password_strength(password)}")
        save_password_to_file(password)

def save_password_to_file(password, filename='passwords.txt'):
    with open(filename, 'a') as file:
        file.write(password + '\n')
    print(f"The password is stored in {filename}.")

def read_passwords_from_file(filename='passwords.txt'):
    try:
        with open(filename, 'r') as file:
            passwords = file.readlines()
            print("Stored passwords:")
            for password in passwords:
                print(password.strip())
    except FileNotFoundError:
        print("The file dosen't exist.")

class PasswordGeneratorSession:
    def __init__(self, max_attempts = 5):
        self.attempts = 0
        self.max_attempts = max_attempts

    def can_generate_password(self):
        return self.attempts < self.max_attempts
    
    def generate(self, *args, **kwargs):
        if not self.can_generate_password():
            print("You reached the maximum amount of tries for this session.")
            return None
        self.attempts += 1
        return generate_password(*args, **kwargs)
    
def test_password_generator():
    assert len(generate_password(10)) == 10, "Error in generating the password length."
    assert any(c.isupper() for c in generate_password(10, use_uppercase=True, use_lowercase=False, use_numbers=False, use_special_chars=False)), "Capital letters not included."
    assert any(c.islower() for c in generate_password(10, use_uppercase=False, use_lowercase=True, use_numbers=False, use_special_chars=False)), "Small letters not included."
    assert any(c.isdigit() for c in generate_password(10, use_uppercase=False, use_lowercase=False, use_numbers=True, use_special_chars=False)), "Numbers not included."
    assert any(c in string.punctuation for c in generate_password(10, use_uppercase=False, use_lowercase=False, use_numbers=False, use_special_chars=True)), "Symbols not included."
    print("All tests passed.")

def password_strength(password):
    criteria = [
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password)
    ]
    strength = sum(criteria)

    if strength < 2:
        return"Weak"
    elif strength == 2:
        return"Mid"
    else:
        return "Strong"
    
if __name__ == "__main__":
    session = PasswordGeneratorSession(max_attempts = 3)
    main(session)

    read_passwords_from_file()

    test_password_generator()