import rsa
import secrets
import scrypt
import string
import random

# Generate RSA keys
public_key, private_key = rsa.newkeys(1024)

# Save the public key
with open("public.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

# Save the private key
with open("private.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))

# Creating a symmetric key sym_key
random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
salt = secrets.token_bytes(32)
sym_key = scrypt.hash(random_string, salt, N=2048, r=8, p=1, buflen=32)

print("\nSymmetric key: ", sym_key)

# Loading the public key from the public key .PEM file
with open("public.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

# Encrypting the symmetric key with the public key
encrypted_sym_key = rsa.encrypt(sym_key, public_key)
print("\nEncrypted Symmetric key : ", encrypted_sym_key)

# Loading the private key from the private key .PEM file
with open("private.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

# Decrypting the symmetric key
decrypted_sym_key = rsa.decrypt(encrypted_sym_key, private_key)
print("\nDecrypted symmetric key : ", decrypted_sym_key)

print("\nPublic and private keys have been generated and saved.\n\n")