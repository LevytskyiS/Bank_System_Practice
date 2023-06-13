import os
import sys
import random

sys.path.append(os.path.abspath("."))

from faker import Faker

from src.database.models import Bank, Client, ClientM2MBank
from src.database.connect import session


def prep_fake_data():
    fake_names = []
    fake_last_names = []
    fake_emails = []
    fake_phones = []
    secret_words = []
    fake_passports = []
    fake_bank_titles = []
    fake_bank_codes = []
    fake_data = Faker()

    for _ in range(10000):
        fake_names.append(fake_data.name().split(" ")[0])

    for _ in range(10000):
        fake_last_names.append(fake_data.name().split(" ")[1])

    for _ in range(10000):
        fake_emails.append(fake_data.email())

    for _ in range(10000):
        fake_phones.append(fake_data.msisdn())

    for _ in range(10000):
        secret_words.append(fake_data.word())

    for _ in range(10000):
        fake_passports.append(fake_data.passport_number())

    for _ in range(200):
        fake_bank_titles.append(f"{fake_data.company()} Bank")

    for _ in range(200):
        fake_bank_codes.append(fake_data.aba())

    return (
        fake_names,
        fake_last_names,
        fake_emails,
        fake_phones,
        secret_words,
        fake_passports,
        fake_bank_titles,
        fake_bank_codes,
    )


def prep_db_objects(
    names: list,
    last_names: list,
    emails: list,
    phones: list,
    words: list,
    passports: list,
    bank_titles: list,
    bank_codes: list,
):
    for_clients = []
    for n, ln, e, p, w, pa in zip(names, last_names, emails, phones, words, passports):
        for_clients.append((n, ln, e, p, w, pa))

    for_banks = []
    for bt, bc in zip(bank_titles, bank_codes):
        for_banks.append((bt, bc))

    for_clients_m2m_banks = []
    for _ in range(10000):
        for_clients_m2m_banks.append(
            (random.randrange(1, 10000), random.randrange(1, 200))
        )

    return for_clients, for_banks, for_clients_m2m_banks


for_clients, for_banks, for_clients_m2m_banks = prep_db_objects(*prep_fake_data())


def fill_db(clients: list, banks: list, m2m: list):
    client_objs = []
    for client in clients:
        client_objs.append(
            Client(
                first_name=client[0],
                last_name=client[1],
                email=client[2],
                phone=client[3],
                secret_word=client[4],
                passport_number=client[5],
            )
        )

    session.add_all(client_objs)
    session.commit()

    bank_objs = []
    for bank in banks:
        bank_objs.append(Bank(title=bank[0], bank_code=bank[1]))

    session.add_all(bank_objs)
    session.commit()

    m2m_objs = []
    for m2m_obj in m2m:
        m2m_objs.append(ClientM2MBank(client_id=m2m_obj[0], bank_id=m2m_obj[1]))

    session.add_all(m2m_objs)
    session.commit()


fill_db(for_clients, for_banks, for_clients_m2m_banks)
