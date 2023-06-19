"TRUNCATE TABLE clients, accounts, creditcards RESTART IDENTITY; - To reset ids"

"""
select clientm2mbank.client_id, clientm2mbank.bank_id, banks.title, accounts.current_deposit, creditcards.card_number 
from clientm2mbank inner join banks
on clientm2mbank.bank_id = banks.id 
inner join clients 
on clientm2mbank.client_id = clients.id 
inner join accounts
on clients.id = accounts.client_id 
inner join creditcards
on accounts.id = creditcards.account_id
where accounts.current_deposit >= 7000000 and clientm2mbank.bank_id = 14
"""
