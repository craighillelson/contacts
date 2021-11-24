"""Command line contact management app."""

import csv
import os
import re
import pyinputplus as pyip


phone_number_regex = "\d{3}-\d{3}-\d{4}"


def create_contacts_file_if_one_does_not_exist():
    if os.path.exists("contacts.csv"):
        pass
    else:
        open("contacts.csv", "w")


def prompt_user():
    main_menu = {
        1: ["add contact", add_contact],
        2: ["delete contact", delete_contact],
        3: ["edit contact", edit_contact],
        4: ["list contacts by domain", list_contacts_by_domain],
        5: ["list all contacts", list_all_contacts],
        6: ["output contacts to csv", output_contacts_to_csv],
    }

    keys = list(main_menu.keys())

    while True:
        print("\nPlease select an option below or nothing to exit\n")
        for num, option in main_menu.items():
            print(f"{num}. {option[0]}")
        user_choice = pyip.inputInt("> ", min=1, blank=True)
        if user_choice != "":
            if user_choice not in keys:
                print("\ninvalid choice")
            else:
                main_menu[user_choice][1]()
        else:
            break


def import_csv():
    dct = {}

    with open("contacts.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dct[row["email"]] = [row["first_name"], row["last_name"], \
                                 row["phone_number"]]

    return dct


def write_dictionary_to_csv(dct):
    with open("contacts.csv", "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["email","first_name","last_name","phone_number"])
        for email, contact_details in dct.items():
            keys_values = (email, *contact_details)
            out_csv.writerow(keys_values)


def add_or_edit_another():
    print("\nwould you like to edit another contact (yes or no) ?")
    return pyip.inputYesNo("> ")


def validate_input(name, label):
    while True:
        name = pyip.inputStr(label)
        if not re.match("^[a-zA-Z,-]*$", name):
            print("names may not include numbers")
        else:
            return name


def build_contacts_menu(dct1):
    dct2 = {}
    for num, (email_address, contact_details) in enumerate(dct1.items(), 1):
        dct2[num] = [email_address, contact_details]

    return dct2


def alert_user():
    print("\n'contacts.csv' is empty")
    print("Let's add some contacts")
    add_contact()


def output_contacts_menu(dct):
    print("\nselect a contact below to edit")
    for num, contact_details in dct.items():
        email_address = contact_details[0]
        first_name = contact_details[1][0]
        last_name = contact_details[1][1]
        phone_number = contact_details[1][2]
        print(f"{num}. {email_address}, {first_name}, {last_name}, "
              f"{phone_number}")


def avoid_duplicate_email_addresses(dct):
    email_addresses = create_a_list_of_email_addresses(dct)
    while True:
        email_address = pyip.inputEmail("email address: ")
        if email_address in email_addresses:
            print("duplicate email address")
        else:
            return email_address


def validate_phone_number():
    while True:
        phone_number = input("phone number: ")
        if not re.search(phone_number_regex, phone_number):
            print("invalid phone number")
        else:
            return phone_number


def avoid_duplicate_phone_numbers(dct):
    phone_numbers = create_a_list_of_phone_numbers(dct)
    while True:
        phone_number = validate_phone_number()
        if phone_number in phone_numbers:
            print("duplicate phone number")
        else:
            return phone_number


def extract_domain(email):
    return email.split("@")[1]


def create_a_list_of_email_addresses(dct):
    return list(dct.keys())


def create_a_list_of_phone_numbers(dct):
    contact_details = list(dct.values())
    lst = []
    for first_last_phone in contact_details:
        lst.append(first_last_phone[2])

    return lst


def add_contact():
    print("\n> add contact")
    while True:
        contacts = import_csv()
        first_name = validate_input("first_name", "\nfirst name: ")
        last_name = validate_input("last name", "last name: ")
        email_address = avoid_duplicate_email_addresses(contacts)
        phone_number = avoid_duplicate_phone_numbers(contacts)
        contact_to_add = {}
        contact_details = [first_name, last_name, phone_number]
        contact_to_add[email_address] = contact_details
        all_contacts = {**contacts, **contact_to_add}

        write_dictionary_to_csv(all_contacts)

        print("\nthe following contact was added")
        print(first_name, last_name)
        print(email_address)
        print(phone_number)

        user_choice = add_or_edit_another()

        if user_choice != "yes":
            break


def delete_contact():
    contacts = import_csv()
    if contacts:
        print("\n> delete contact")
        contacts_numbered = build_contacts_menu(contacts)
        keys = list(contacts_numbered.keys())
        while True:
            print("\nselect a contact to delete")
            for num, contact_details in contacts_numbered.items():
                email_address = contact_details[0]
                print(f"{num}. {email_address}")
            contact_to_delete = int(input("> "))
            if contact_to_delete not in keys:
                print("\ninvalid entry")
            else:
                selected_contact = contacts_numbered[contact_to_delete]
                email_address = selected_contact[0]
                print("\ndelete the following contact (yes or no)?")
                print(email_address)
                contact_details = selected_contact[1]
                first_name = contact_details[0]
                last_name = contact_details[1]
                phone_number = contact_details[2]
                print(first_name, last_name)
                print(phone_number)
                confirm_delete = pyip.inputYesNo("> ")
                if confirm_delete == "yes":
                    print(confirm_delete)
                    del contacts[email_address]
                    write_dictionary_to_csv(contacts)
                    print(f"\n{email_address} was deleted successfully")
                else:
                    print("\ncontact deletion cancelled")
            break
    else:
        alert_user()


def select_contact():
    contacts = import_csv()
    if contacts:
        contacts_menu = build_contacts_menu(contacts)
        keys = contacts_menu.keys()
        print("\n> edit contact")
        while True:
            output_contacts_menu(contacts_menu)
            user_choice = pyip.inputInt("> ", blank=True)
            if user_choice not in keys or user_choice == "":
                print("\nplease select from the options below")
            else:
                selected_contact = contacts_menu[user_choice]
                email_address = selected_contact[0]
                first_name = selected_contact[1][0]
                last_name = selected_contact[1][1]
                phone_number = selected_contact[1][2]
                contact = (email_address, first_name, last_name, phone_number)
                break
    else:
        print("no contacts")

    return contact, user_choice


def edit_email_address(selected_contact):
    email_address = selected_contact[0]
    print(f"\nedit email address {email_address}")
    edited_email_address = pyip.inputEmail("> ", blank=True)
    if edited_email_address == "":
        edited_email_address = email_address

    return edited_email_address


def edit_name(selected_contact, i, header):
    name = selected_contact[i]
    print(header.format(name))
    edited_name = pyip.inputStr("> ", blank=True)
    if edited_name == "":
        edited_name = name

    return edited_name


def edit_phone_number(selected_contact):
    phone_number = selected_contact[3]
    contacts = import_csv()
    phone_numbers = create_a_list_of_phone_numbers(contacts)
    phone_numbers.remove(phone_number)
    while True:
        print(f"\nedit phone number {phone_number}")
        edited_phone_number = pyip.inputStr("> ", blank=True)
        if edited_phone_number == "":
            edited_phone_number = phone_number
        if edited_phone_number in phone_numbers:
            print("duplicate phone number")
        elif not re.search(phone_number_regex, edited_phone_number):
            print("invalid phone number")
        else:
            break

    return edited_phone_number


def edit_contact():
    selected_contact, user_choice = select_contact()
    updated_email_address = edit_email_address(selected_contact)
    updated_first_name = edit_name(selected_contact, 1, "\nedit first name {}")
    updated_last_name = edit_name(selected_contact, 2, "\nedit last name {}")
    updated_phone_number = edit_phone_number(selected_contact)

    dct = {}
    updated_contact = [updated_email_address, [updated_first_name, \
                       updated_last_name, updated_phone_number]]

    contacts = import_csv()
    dct = build_contacts_menu(contacts)
    dct.update({user_choice: updated_contact})

    print("\n")
    merged_contacts = list(dct.values())
    contacts_to_output = {}
    for i in merged_contacts:
        email_address = i[0]
        first_name = i[1][0]
        last_name = i[1][1]
        phone_number = i[1][2]
        contacts_to_output[email_address] = [first_name, last_name,
                                             phone_number]

    write_dictionary_to_csv(contacts_to_output)

    return dct


def list_contacts_by_domain():
    contacts = import_csv()
    if contacts:
        print("\n> list contacts by domain")
        email_addresses = create_a_list_of_email_addresses(contacts)
        domains = []
        for email_address in email_addresses:
            domain = extract_domain(email_address)
            domains.append(domain)
        unique_domains = set(domains)

        if len(unique_domains) > 1:
            domains_menu = {}
            for num, domain in enumerate(sorted(unique_domains), 1):
                domains_menu[num] = domain

            print("\nselect a domain from the list below")
            for num, domain in domains_menu.items():
                print(f"{num}. {domain}")

            user_choice = int(input("> "))
            selected_domain = domains_menu[user_choice]
            print(f"\n> results for {selected_domain}")
            for email_address, contact_details in sorted(contacts.items()):
                domain = extract_domain(email_address)
                if selected_domain == domain:
                    first_name = contact_details[0]
                    last_name = contact_details[1]
                    phone_number = contact_details[2]
                    print(f"\n{email_address}")
                    print(first_name, last_name)
                    print(phone_number)
        else:
            for email_address, contact_details in sorted(contacts.items()):
                first_name = contact_details[0]
                last_name = contact_details[1]
                phone_number = contact_details[2]
                print(f"\n{email_address}")
                print(first_name, last_name)
                print(phone_number)
    else:
        alert_user()


def list_all_contacts():
    contacts = import_csv()
    if contacts:
        print("\n> all contacts")
        for email_address, contact_details in sorted(contacts.items()):
            first_name = contact_details[0]
            last_name = contact_details[1]
            phone_number = contact_details[2]
            print(f"\n{first_name} {last_name}")
            print(email_address)
            print(phone_number)
    else:
        alert_user()


def output_contacts_to_csv():
    print("\n> output contacts")
    contacts = import_csv()
    lst = []
    for email_address, name_and_phone_number in sorted(contacts.items()):
        first_name = name_and_phone_number[0]
        last_name = name_and_phone_number[1]
        phone_number = name_and_phone_number[2]
        name_email_phone = [first_name, last_name, email_address, phone_number]
        lst.append(name_email_phone)

    filename = "exported_contacts.csv"
    with open(filename, "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["email","first_name","last_name","phone_number"])
        for name_email_phone in lst:
            out_csv.writerow(name_email_phone)

    print(f"\n{filename} exported successfully")


create_contacts_file_if_one_does_not_exist()
prompt_user()
