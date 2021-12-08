"""Command line contact management app."""

import csv
import os
import re
import pyinputplus as pyip

PHONE_NUMBER_REGEX = r"^(\([0-9]{3}\) ?|[0-9]{3}-)[0-9]{3}-[0-9]{4}$"


def alert_user():
    print("\n'contacts.csv' is empty")
    print("Let's add some contacts")
    add_contact()


def avoid_duplicate_email_addresses(dct):
    email_addresses = build_list_of_email_addresses(dct)
    while True:
        email_address = pyip.inputEmail("\nemail address: ")
        if email_address in email_addresses:
            print("duplicate email address")
        else:
            return email_address


def avoid_duplicate_phone_numbers(dct):
    phone_numbers = build_list_of_phone_numbers(dct)
    while True:
        phone_number = validate_phone_number()
        if phone_number in phone_numbers:
            print("duplicate phone number")
        else:
            return phone_number


def build_list_of_domain_contacts(dct, lst2):
    user_choice = pyip.inputInt("> ")
    selected_domain = dct[user_choice]
    lst1 = []
    print(f"\n{selected_domain}")
    for contact in lst2:
        if contact.endswith(selected_domain):
            lst1.append(contact)

    return lst1


def build_list_of_domains():
    print("\n> list contacts by domain")
    dct = import_csv()
    email_addresses = dct.keys()
    domains = []
    for email in email_addresses:
        domain = email.split("@")[1]
        domains.append(domain)

    return dct, list(set(domains))


def build_list_of_email_addresses(dct):
    return list(dct.keys())


def build_list_of_phone_numbers(dct):
    lst = []
    for contact in dct.values():
        current_phone_number = contact[2]
        lst.append(current_phone_number)

    return lst


def capture_attributes(dct1, dct2):
    while True:
        email = avoid_duplicate_email_addresses(dct1)
        first_name = pyip.inputStr("first name: ")
        last_name = pyip.inputStr("last name: ")
        phone_number = avoid_duplicate_phone_numbers(dct1)
        contact_details = [first_name, last_name, phone_number]
        dct2[email] = contact_details
        all_contacts = {**dct1, **dct2}

        write_dictionary_to_csv("contacts.csv", all_contacts)

        add_another = pyip.inputYesNo("\nWould you like to add another "
                                      "(yes/no)? ")

        if add_another != "yes":
            break


def edit_email(email_address, lst):
    print("\nupdate value or enter nothing to keep current value")
    while True:
        print(f"\ncurrent email: {email_address}")
        edited_email = pyip.inputEmail("> ", blank=True)
        if edited_email in lst:
            print("duplicate email address")
        elif edited_email == "":
            edited_email = email_address
            break
        else:
            break

    return edited_email


def edit_phone_number(dct, phone):
    phone_numbers = build_list_of_phone_numbers(dct)
    while True:
        print(f"current phone number {phone} ")
        edited_phone_number = input("> ")
        if edited_phone_number == "":
            edited_phone_number = phone
            break
        if edited_phone_number in phone_numbers:
            print("duplicate phone number")
        elif not re.match(PHONE_NUMBER_REGEX, edited_phone_number):
            print("invalid number")
        else:
            break

    return edited_phone_number


def enumerate_contacts(dct1):
    dct2 = {}
    for number, (email, contact_attributes) in enumerate(dct1.items(), 1):
        dct2[number] = [email, *contact_attributes]

    return dct2


def import_csv():
    dct = {}

    with open("contacts.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dct[row["email"]] = [row["first_name"], row["last_name"], \
                                 row["phone_number"]]

    return dct


def output_added_contacts(header, dct):
    print(header)
    for email_address, contract_attributes in dct.items():
        print(f"\n{email_address}")
        for attribute in contract_attributes:
            print(attribute)


def output_contacts(dct):
    for number, contact_attributes in dct.items():
        email = contact_attributes[0]
        first_name = contact_attributes[1]
        last_name = contact_attributes[2]
        phone_number = contact_attributes[3]
        print(f"{number}. {email}, {first_name}, {last_name}, {phone_number}")



def output_contacts_by_domain(lst):
    if len(lst) > 1:
        for number, contact in enumerate(lst, 1):
            print(f"{number}. {contact}")
    else:
        print(*lst)


def populate_dictionary(dct2):
    dct1 = {}
    for user_attribute in dct2.values():
        email = user_attribute[0]
        first_name = user_attribute[1]
        last_name = user_attribute[2]
        phone_number = user_attribute[3]
        dct1[email] = [first_name, last_name, phone_number]

    return dct1


def update_contacts(dct1, dct2):
    dct1 = {}
    for contact_attributes in dct2.values():
        email = contact_attributes[0]
        first_name = contact_attributes[1]
        last_name = contact_attributes[2]
        phone_number = contact_attributes[3]
        dct1[email] = [first_name, last_name, phone_number]

    write_dictionary_to_csv("contacts.csv", dct1)


def validate_name(attribute, name):
    print("current", attribute, name)
    updated_first_name = pyip.inputStr("> ", blank=True)
    if updated_first_name == "":
        updated_first_name = name

    return updated_first_name


def validate_phone_number():
    while True:
        phone_number = input("phone number (xxx-xxx-xxxx): ")
        if not re.match(PHONE_NUMBER_REGEX, phone_number):
            print("invalid number")
        break

    return phone_number


def write_dictionary_to_csv(contacts_csv, dct):
    with open(contacts_csv, "w") as out_file:
        out_csv = csv.writer(out_file)
        out_csv.writerow(["email","first_name","last_name","phone_number"])
        for email, contact_details in dct.items():
            keys_values = (email, *contact_details)
            out_csv.writerow(keys_values)


def create_contacts_csv_if_one_does_not_exist():
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

    numbered_options = list(main_menu.keys())

    while True:
        print("\nPlease select an option below or nothing to exit\n")
        for num, option in main_menu.items():
            print(f"{num}. {option[0]}")
        user_choice = pyip.inputInt("> ", min=1, blank=True)
        if user_choice != "":
            if user_choice not in numbered_options:
                print("\ninvalid choice")
            else:
                main_menu[user_choice][1]()
        else:
            print("\nsession complete\n")
            break


def add_contact():
    print("\n> add contact")
    contacts = import_csv()
    contacts_to_add = {}
    capture_attributes(contacts, contacts_to_add)

    if contacts_to_add:
        if len(contacts_to_add) > 1:
            output_added_contacts("\nthe following contacts were added",
                                  contacts_to_add)
        else:
            output_added_contacts("\nthe following contact was added",
                                  contacts_to_add)


def delete_contact():
    print("\n> delete contact")
    updated_contacts = {}
    while True:
        print("\nselect a contact to delete or enter nothing to exit")
        contacts = import_csv()
        enumerated_contacts = enumerate_contacts(contacts)
        for number, attributes in enumerated_contacts.items():
            email = attributes[0]
            print(f"{number}. {email}")
        select_contact = pyip.inputInt("> ", min=1, blank=True)

        if select_contact == "":
            break

        attributes = enumerated_contacts[select_contact]

        print(f"\ndelete {email} (yes or no)?")
        confirm_delete = pyip.inputYesNo("> ")

        if confirm_delete == "yes":
            del enumerated_contacts[select_contact]
            print("\nthe following contact was deleted")
            for attribute in attributes:
                print(attribute)

        updated_contacts = populate_dictionary(enumerated_contacts)
        write_dictionary_to_csv("contacts.csv", updated_contacts)

        print("\nwould you like to delete another (yes or no)?")
        delete_another = pyip.inputYesNo("> ")
        if delete_another == "no":
            break


def edit_contact():
    print("\n> edit contact")
    contacts = import_csv()
    if not contacts:
        alert_user()

    while True:
        print("\nselect a contact to edit or enter nothing to exit")
        email_addresses = build_list_of_email_addresses(contacts)
        enumerated_contacts = enumerate_contacts(contacts)
        output_contacts(enumerated_contacts)
        select_contact = pyip.inputInt("> ", min=1, blank=True)
        if select_contact == "":
            break

        selected_contact_attributes = enumerated_contacts[select_contact]

        email = selected_contact_attributes[0]
        first_name = selected_contact_attributes[1]
        last_name = selected_contact_attributes[2]
        phone_number = selected_contact_attributes[3]

        updated_email = edit_email(email, email_addresses)
        updated_first_name = validate_name("first name:", first_name)
        updated_last_name = validate_name("last name:", last_name)
        updated_phone_number = edit_phone_number(contacts, phone_number)

        enumerated_contacts[select_contact] = [updated_email, \
                                               updated_first_name, \
                                               updated_last_name, \
                                               updated_phone_number]

        update_contacts("updated_contacts", enumerated_contacts)

        edit_another = pyip.inputYesNo("\nWould you like to edit another "
                                       "(yes/no)? ")

        if edit_another != "yes":
            break


def list_contacts_by_domain():
    contacts, unique_domains = build_list_of_domains()
    enumerated_domains = {}
    while True:
        if unique_domains:
            if len(unique_domains) > 1:
                print("\nselect one of the domains below")
                for number, domain in enumerate(unique_domains, 1):
                    enumerated_domains[number] = domain
            else:
                print("\ndomain")
                print(unique_domains[0])
                for number, contact in enumerate(contacts, 1):
                    print(f"{number}. {contact}")
                break
        else:
            print("\nno domains")
            break

        for number, domain in enumerated_domains.items():
            print(f"{number}. {domain}")

        domain_contacts = build_list_of_domain_contacts(enumerated_domains,
                                                        contacts)

        output_contacts_by_domain(domain_contacts)

        print("\nwould you like to select another (yes or no?")
        another_domain = pyip.inputYesNo("> ")
        if another_domain != "yes":
            break


def list_all_contacts():
    print("\n> list all contacts\n")
    contacts = import_csv()
    if contacts:
        if len(contacts) > 1:
            for number, (email) in enumerate(sorted(contacts.keys()), 1):
                print(f"{number}. {email}")
        else:
            print(*contacts)
    else:
        print("no contacts found")
        alert_user()


def output_contacts_to_csv():
    print("\n> output contacts to csv")
    contacts = import_csv()
    write_dictionary_to_csv("exported_contacts.csv", contacts)
    print('\n"exported_contacts.csv" exported successfully')


create_contacts_csv_if_one_does_not_exist()
prompt_user()
