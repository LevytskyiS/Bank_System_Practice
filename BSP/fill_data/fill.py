import os
import sys
import random

sys.path.append(os.path.abspath("."))

from faker import Faker

from src.database.models import Client, Account, CreditCard, Manager
from src.database.connect import session

SEX = ["male", "female"]
ROLES = ["admin", "director", "team_leader", "manager"]
CITIES = [
    "London",
    "Kyiv",
    "Prague",
    "Paris",
    "Berlin",
    "Liverpool",
    "Lisbon",
    # "Dortmund",
    # "Munich",
    # "Zadar",
    # "Lviv",
    # "Madrid",
    # "Barcelona",
    # "LA",
    # "Detroit",
    # "Ohio",
    # "Toronto",
    # "Valencia",
    # "Milan",
    # "Rome",
    # "Amsterdam",
    # "Vienna",
    # "Warsaw",
]
fast_fake = Faker()


def prep_fake_data():
    fake_names = []
    fake_last_names = []
    fake_tax_numbers = []
    fake_emails = []
    fake_phones = []
    secret_words = []
    fake_passports = []
    # fake_bank_titles = []
    # fake_bank_codes = []
    fake_accounts = []
    fake_credit_cards = []
    fake_data = Faker()

    for _ in range(10000):
        fake_names.append(fake_data.name().split(" ")[0])

    for _ in range(10000):
        fake_last_names.append(fake_data.name().split(" ")[1])

    while len(fake_tax_numbers) != 100000:
        fake_tn = random.randrange(1000000, 9999999)
        if fake_tn in fake_tax_numbers:
            continue
        else:
            fake_tax_numbers.append(fake_tn)

    # for _ in range(10000):
    #     fake_emails.append(fake_data.email())

    while len(fake_emails) != 10000:
        fake_email = fake_data.email()
        if fake_email in fake_emails:
            continue
        else:
            fake_emails.append(fake_email)

    # for _ in range(10000):
    #     fake_phones.append(fake_data.msisdn())

    while len(fake_phones) != 10000:
        fake_phone = fake_data.msisdn()
        if fake_phone in fake_phones:
            continue
        else:
            fake_phones.append(fake_phone)

    for _ in range(10000):
        secret_words.append(fake_data.word())

    # for _ in range(10000):
    #     fake_passports.append(fake_data.passport_number())

    while len(fake_passports) != 10000:
        fake_passport = fake_data.passport_number()
        if fake_passport in fake_passports:
            continue
        else:
            fake_passports.append(fake_passport)

    # for _ in range(200):
    #     fake_bank_titles.append(f"{fake_data.company()} Bank")

    # for _ in range(200):
    #     fake_bank_codes.append(fake_data.aba())

    for _ in range(10000):
        fake_accounts.append(fake_data.iban())

    for _ in range(10000):
        fake_credit_cards.append(fake_data.credit_card_number())

    return (
        fake_names,
        fake_last_names,
        fake_tax_numbers,
        fake_emails,
        fake_phones,
        secret_words,
        fake_passports,
        # fake_bank_titles,
        # fake_bank_codes,
        fake_accounts,
        fake_credit_cards,
    )


def prep_db_objects(
    names: list,
    last_names: list,
    tax_numbers: list,
    emails: list,
    phones: list,
    words: list,
    passports: list,
    # bank_titles: list,
    # bank_codes: list,
    accounts: list,
    credit_cards: list,
):
    for_clients = []
    for n, ln, tn, e, p, w, pa in zip(
        names, last_names, tax_numbers, emails, phones, words, passports
    ):
        for_clients.append((n, ln, tn, e, p, w, pa))

    # for_banks = []
    # for bt, bc in zip(bank_titles, bank_codes):
    #     for_banks.append((bt, bc))

    for_clients_m2m_banks = []
    for _ in range(10000):
        for_clients_m2m_banks.append(
            (random.randrange(1, 10000), random.randrange(1, 200))
        )

    for_accounts = []
    for a in accounts:
        for_accounts.append(
            (a, random.randrange(0, 9999999), random.randrange(1, 10000))
        )

    for_credit_cards = []
    for card in credit_cards:
        for_credit_cards.append(
            (card, random.randrange(1000, 9999), random.randrange(1, 10000))
        )

    return (
        for_clients,
        # for_banks,
        # for_clients_m2m_banks,
        for_accounts,
        for_credit_cards,
    )


(
    for_clients,
    # for_banks,
    # for_clients_m2m_banks,
    for_accounts,
    for_credit_cards,
) = prep_db_objects(*prep_fake_data())


def fill_db(
    clients: list,
    # banks: list,
    # m2m: list,
    accounts: list,
    cards: list,
):
    client_objs = []
    for client in clients:
        client_objs.append(
            Client(
                first_name=client[0],
                last_name=client[1],
                tax_number=client[2],
                email=client[3],
                # city=fast_fake.city(),
                city=random.choice(CITIES),
                phone=client[4],
                secret_word=client[5],
                passport_number=client[6],
                sex=random.choice(SEX),
            )
        )
    session.add_all(client_objs)
    session.commit()

    # bank_objs = []
    # for bank in banks:
    #     bank_objs.append(Bank(title=bank[0], bank_code=bank[1]))

    # session.add_all(bank_objs)
    # session.commit()

    # m2m_objs = []
    # for m2m_obj in m2m:
    #     m2m_objs.append(ClientM2MBank(client_id=m2m_obj[0], bank_id=m2m_obj[1]))

    # session.add_all(m2m_objs)
    # session.commit()

    accounts_objs = []
    for acc in accounts:
        accounts_objs.append(
            Account(account_number=acc[0], current_deposit=acc[1], client_id=acc[2])
        )

    session.add_all(accounts_objs)
    session.commit()

    card_objs = []
    for card in cards:
        card_objs.append(
            CreditCard(card_number=card[0], pin_code=card[1], account_id=card[2])
        )

    session.add_all(card_objs)
    session.commit()


fill_db(
    for_clients,
    # for_banks,
    # for_clients_m2m_banks,
    for_accounts,
    for_credit_cards,
)


def create_manager_db():
    managers = []
    for i in range(10):
        man = Manager(
            first_name=fast_fake.name().split(" ")[0],
            last_name=fast_fake.name().split(" ")[1],
            email=f"test{i}@kuku.com",
            phone=f"+380123123{i}",
            roles=random.choice(ROLES),
            password=random.choice(ROLES),
        )
        managers.append(man)
    session.add_all(managers)
    session.commit()


create_manager_db()
