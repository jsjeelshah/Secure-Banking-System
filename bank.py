import socket
import pickle
import rsa
import hashlib
from cryptography.fernet import Fernet
import csv
import sys

def handle_transfer_request(client_socket, user_id, trans_data, account_balances):
    account_type, recipient_id, amount = trans_data[1:4]
    amount = int(amount)

    if recipient_id not in account_balances:
        client_socket.send("\n****** The recipient's ID does not exist.******".encode())
        return

    sender_savings, sender_checking = map(int, account_balances[user_id])
    recipient_savings, recipient_checking = map(int, account_balances[recipient_id])

    if (account_type == "1" and sender_savings >= amount) or (account_type == "2" and sender_checking >= amount):
        if account_type == "1":
            sender_savings -= amount
            recipient_savings += amount
        else:
            sender_checking -= amount
            recipient_checking += amount

        account_balances[user_id] = (str(sender_savings), str(sender_checking))
        account_balances[recipient_id] = (str(recipient_savings), str(recipient_checking))
        with open("balance.csv", 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in account_balances.items():
                writer.writerow([key, value[0], value[1]])

        client_socket.send("\n****** Your transaction is successful.******\n".encode())
    else:
        client_socket.send("\n****** Your account does not have enough funds.*******\n".encode())

def main():
    port = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port))
    print('\nListening...')
    s.listen(5)

    while True:
        client_socket, address = s.accept()
        print('\n')
        print(f"Connection from {address} has been established!!!")
        account_balances = {}

        with open("balance.csv", newline='') as text1:
            csv_read1 = csv.reader(text1)
            for row in csv_read1:
                account_balances[row[0]] = (row[1], row[2])

        try:
            while True:
                recd_data1 = client_socket.recv(1024)
                if not recd_data1:
                    break
                recd_data = pickle.loads(recd_data1)
                with open("private.pem", "rb") as f:
                    private_key = rsa.PrivateKey.load_pkcs1(f.read())

                sym_key = rsa.decrypt(recd_data[0], private_key)
                fernet = Fernet(sym_key)
                user_id = fernet.decrypt(recd_data[1]).decode()
                password = fernet.decrypt(recd_data[2]).decode()

                # hash_pass = hashlib.md5(password.encode())
                # hash_pass_hex = hash_pass.hexdigest()
                dict_pass = {}
                with open("passwd.csv", newline='') as text:
                    csv_read = csv.reader(text)
                    for row in csv_read:
                        dict_pass[row[0]] = row[1]

                if user_id in dict_pass and dict_pass[user_id] == password:
                    client_socket.send("1".encode())

                    while True:
                        trans_data1 = client_socket.recv(1024)
                        trans_data = pickle.loads(trans_data1)

                        if trans_data[0] == "1":
                            handle_transfer_request(client_socket, user_id, trans_data, account_balances)

                        elif trans_data[0] == "2":
                            saving_balance, checking_balance = account_balances.get(user_id, ("0", "0"))
                            client_socket.send(pickle.dumps((saving_balance, checking_balance)))

                        elif trans_data[0] == "3":
                            print('\nExiting...\n')
                            print(""*30)
                            print("\n")
                            exit()
                            break
                else:
                    client_socket.send("0".encode())
        except OSError as e:
            print(f"Socket error: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
