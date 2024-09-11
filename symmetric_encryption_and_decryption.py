from cryptography.fernet import Fernet
import argparse

# Function to encrypt data using the provided cipher suite
def encrypt(data, cipher_suite):
    return cipher_suite.encrypt(data.encode())

# Function to decrypt encrypted data using the provided cipher suite
def decrypt(encrypted_data, cipher_suite):
    return cipher_suite.decrypt(encrypted_data)  # Corrected parameter name to encrypted_data

# Function to read the contents of a file
def readFile(source_file):
    with open(source_file, "r") as file:
        return file.read()

# Function to select the operation mode (encrypt or decrypt)
def selectMode(mode, encrypt_func, decrypt_func):
    print(f"Selecting {mode} mode")
    if mode == "encrypt":
        return encrypt_func()  # Call the encryption function
    elif mode == "decrypt":
        return decrypt_func()  # Call the decryption function

# Main block of the script
if __name__=="__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_source_file", action="store", type=str, help="The data file to be encrypted")
    parser.add_argument("-m", "--mode", action="store", type=str, help="Select mode (encrypt, decrypt, genkey)")
    parser.add_argument("-k", "--key_source_file", action="store", type=str, help="The key file to encrypt or decrypt the data")
    parser.add_argument("-o", "--output_file", action="store", type=str, help="The output file of the result")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Assign variables from parsed arguments
    mode = args.mode
    data_source_file = args.data_source_file
    key_source_file = args.key_source_file
    output_file = args.output_file

    # Check if all required arguments are provided for encryption/decryption
    if mode and data_source_file and key_source_file and output_file:
        data = readFile(data_source_file)  # Read the data to be encrypted/decrypted
        key = readFile(key_source_file)     # Read the key for encryption/decryption
        cipher_suite = Fernet(key)          # Create a cipher suite using the key

        # Open the output file to write the result
        with open(output_file, "w") as file:
            result = selectMode(
                mode,
                lambda: encrypt(data, cipher_suite),  # Pass the encryption function
                lambda: decrypt(data.encode(), cipher_suite),  # Pass the decryption function
            )
            file.write(result.decode())  # Write the result to the output file

    # If only mode and output file are provided, generate a new key
    elif mode and output_file:
        with open(output_file, "w") as file:
            result = Fernet.generate_key()  # Generate a new key
            file.write(result.decode())      # Write the new key to the output file

