# Secure-Banking-System
A Secure Banking System implemented in Python, featuring RSA and AES/3DES encryption for secure communication between a simulated bank server and multiple ATM clients. The project showcases user authentication, account balance management, and secure fund transfer capabilities.


## Programming Language

- Python

## Features

- **RSA Encryption**: Utilizes RSA encryption for securing communication between the client and server.
- **Symmetric Encryption**: Employs the `cryptography` library's Fernet for encrypting user credentials and transaction data.
- **Banking Operations**: Supports transferring funds and checking account balances.

## Dependencies

- Python libraries: `rsa`, `cryptography`, `socket`, `pickle`, `csv`, `sys`.

## Setup and Execution

NOTE: It is necessary to create and activate the virtual environmentin order to run the code.

### Setting Up the Virtual Environment


Before running the scripts, you need to activate a Python virtual environment. 


1. **Create a Virtual Environment in the existing folder(if not already created)**: `python -m venv myenv`
2. **Activate the Virtual Environment**: Run `source myenv/bin/activate` to activate the virtual environment.

### Generate RSA Keys

1. Run `python3 encrypt.py` to generate `public.pem` and `private.pem` files. 
     Note : (I have already generated this, you can delete both the key files and run it again)
2. Place these files in the same directory as the client and server scripts.

### Start the Server (Bank)

- Execute `bank.py` with a specified port number.
- Example: `python3 bank.py <port number>`
- example: python3 bank.py 7776

### Run the Client (ATM)

- In a separate terminal, run `atm.py` with the server's hostname and the same port number.
- Example: `python3 atm.py <domain name> <bank server’s port number>`
- example: python3 atm.py remote00.cs.binghamton.edu 7776
- Follow the prompts to perform banking operations.



## Special Notes

- **Security**: The private key (`private.pem`) should be kept secure and not shared.
- **Data Storage**: User credentials are stored in `passwd.csv` and account balances in `balance.csv`. These should be present in the same directory as the server script.
- **Password Storage**: Passwords are stored in plain text in `passwd.csv`.
- **Error Handling**: Both the client and server include basic error handling for network communication and data processing.
