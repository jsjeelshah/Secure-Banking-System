import socket
import rsa
from cryptography.fernet import Fernet
import pickle
import sys

def transfer_funds(s):
    while True:
        print("\n")
        print("-"*60)
        print("  Please select an account to transfer money (enter 1 or 2):\n    1. Savings\n    2. Checking")
        print("-"*60)
        account_type = input("Enter choice: ")
        print("-"*60)
        if account_type not in ["1", "2"]:
            print("\nIncorrect input. Please try again.")
            continue
        recipient_id = input("\nEnter recipient's user ID: ")
        amount = input("Enter the amount to transfer: $ ")

        trans_data = pickle.dumps(["1", account_type, recipient_id, amount])
        s.send(trans_data)

        response = s.recv(1024).decode("utf-8")
        print(response)
        break

def main():
    host_name = sys.argv[1]
    port = int(sys.argv[2])

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host_name, port))

            user_id = input("\nEnter your user id: ")
            password = input("Enter your password: ")

            sym_key = Fernet.generate_key()
            fernet = Fernet(sym_key)
            with open("public.pem", "rb") as f:
                public_key = rsa.PublicKey.load_pkcs1(f.read())

            encrypted_sym_key = rsa.encrypt(sym_key, public_key)
            encrypted_user_id = fernet.encrypt(user_id.encode())
            encrypted_password = fernet.encrypt(password.encode())

            data = pickle.dumps([encrypted_sym_key, encrypted_user_id, encrypted_password])
            s.send(data)

            auth_response = s.recv(1024).decode("utf-8")
            if auth_response == "1":
                while True:
                    print("\n")
                    print("="*30)
                    print("Select action:\n   1. Transfer money\n   2. Check balance\n   3. Exit")
                    print("="*30)
                    choice = input("Enter Choice:")
                    print("="*30)

                    
                    if choice == "1":
                        transfer_funds(s)
                    elif choice == "2":
                        s.send(pickle.dumps(["2"]))
                        response = s.recv(1024)
                        if response:
                            saving_balance, checking_balance = pickle.loads(response)
                            print(f"\nSavings account balance: ${saving_balance}")
                            print(f"Checking account balance: ${checking_balance}")
                        else:
                            print("\nNo balance information received from server.")
                    elif choice == "3":
                        s.send(pickle.dumps(["3"]))
                        print("\nExiting...\n")
                        print('x'*30)
                        print("\n")
                        s.close()
                        exit()
                        break
                    else:
                        print("\nInvalid choice. Please try again.")

        # continue_choice = input("Do you want to continue? (yes/no): ")
        # if continue_choice.lower() != "yes":
        #     print("Exiting...")
        #     break

if __name__ == "__main__":
    main()
