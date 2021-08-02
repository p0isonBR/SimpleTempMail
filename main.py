# Autor:    p0isonBR
# GitHub:   https://github.com/p0isonBR
# Email:    poisonbr@pm.me
# Contato:  https://t.me/p0isonBR
#
# -There is no knowledge that is not power-

import tempmail
import random
import string
import time
import requests
from os import system
from faker import Faker


def main():
    print("""Welcome to SimpleTempMail! Choose operation to proceed:
[ 1 ] New Temp Mail.
[ 2 ] Login with credentials.""")

    op = input("Input operation key (1 or 2): ")

    while op not in ["1", "2"] or not op.isdigit():
        op = input("\nPlease, select a valid key: ")

    if op == "1":
        get_dom = tempmail.domains()

        print("\nAvailable domains: ", len(get_dom))
        dom_list = list()

        for c in range(len(get_dom)):
            dom_list.append(get_dom[c].get('domain'))
            print(f"\n[ {c} ] {dom_list[c]}\n")

        sel_dom = input("Choose domain key: ")

        while not sel_dom.isdigit() and int(sel_dom) not in range(len(dom_list)):
            sel_dom = input("Please, select a valid key: ")

        domain_mail = "@" + dom_list[int(sel_dom)]

        username = input("\nSet username for temp mail (username only, enter for random): ")

        if len(username) == 0:
            address = fake.user_name() + "_" + fake.user_name() + domain_mail
        else:
            address = username + domain_mail

        password = input("Set a password (enter for random): ")
        if len(password) == 0:
            password = ''.join([random.choice(string.ascii_lowercase + string.digits) for _ in range(11)])

        system("clear")
        print(f"Generating your new TempMail with credentials: \nE-Mail: {address} \nPassword: {password}")
        mail(address, password)


def mail(address, password):
    my_mail = tempmail.TempMail(address, password)

    try:
        account = my_mail.generate()

    except tempmail.GenerateError as error:
        print(f"{error}, restarting TempMail...")
        input("Press enter to restart.")
        system("clear")
        main()

    else:
        print("\nSuccess! Account info:\n")
        for key, value in account.items():
            print(f"{key}: {value}")
        print("\nOpen your inbox... ", end="")

        inbox_mails = my_mail.get_messages()
        print("Inbox messages:", len(inbox_mails))
        print("\nWaiting for new mails...\n")

        while True:
            new_mail = my_mail.get_messages()

            if len(new_mail) > len(inbox_mails):
                input("+1 New mail received! Press enter to open:\n")

                _id = new_mail[0]["id"]
                for k, v in new_mail[0].items():

                    if type(v) == dict:
                        for key, value in v.items():
                            print(f'{key}: {value}')

                    elif type(v) == list:
                        for s in v:
                            for x, y in s.items():
                                print(f'{x}: {y}')

                    else:
                        print(f'{k}: {v}')
                dl = input("Want you download full message? [N/y]: ")

                if dl.lower() == "y":
                    header = ({"Authorization": "Bearer " + my_mail._token})
                    html = requests.get("https://api.mail.tm/messages/" + _id, headers=header).json()["html"][0]
                    open('inbox/' + _id + '.html', 'w').write(html)
                    print('Full message saved in: inbox/' + _id + '.html')

                inbox_mails = new_mail
                print("\nWaiting for new mails...\n")
            time.sleep(5)


if __name__ == "__main__":
    fake = Faker()
    main()
