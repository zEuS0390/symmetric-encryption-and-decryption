from cryptography.fernet import Fernet
import argparse

def encrypt(data, cipher_suite):
	return cipher_suite.encrypt(data.encode())

def decrypt(encrypted_data, cipher_suite):
	return cipher_suite.decrypt(data.encode())

def readFile(source_file):
	with open(source_file, "r") as file:
		return file.read()

def selectMode(mode, encrypt_func, decrypt_func):
	print(f"Selecting {mode} mode")
	if mode == "encrypt": return encrypt_func()
	elif mode == "decrypt": return decrypt_func()

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--data_source_file", action="store", type=str, help="The data file to be encrypted")
	parser.add_argument("-m", "--mode", action="store", type=str, help="Select mode (encrypt, decrypt, genkey)")
	parser.add_argument("-k", "--key_source_file", action="store", type=str, help="The key file to encrypt or decrypt the data")
	parser.add_argument("-o", "--output_file", action="store", type=str, help="The output file of the result")

	args = parser.parse_args()

	mode = args.mode
	data_source_file = args.data_source_file
	key_source_file = args.key_source_file
	output_file = args.output_file
	
	if mode and data_source_file and key_source_file and output_file:
		data = readFile(data_source_file)
		key = readFile(key_source_file)
		cipher_suite = Fernet(key)

		with open(output_file, "w") as file:
			result = selectMode(
				mode, 
				lambda: encrypt(data, cipher_suite),
				lambda: decrypt(data, cipher_suite),
			)
			file.write(result.decode())

	elif mode and output_file:
		with open(output_file, "w") as file:
			result = Fernet.generate_key()
			file.write(result.decode())
