"TRUNCATE TABLE clients, accounts, creditcards, managers RESTART IDENTITY; - To reset ids"

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

"""
select clients.id, accounts.account_number, accounts.current_deposit
from clients inner join accounts
on clients.id = accounts.client_id 
order by accounts.current_deposit desc 
limit 5 

select clients.id, accounts.account_number, accounts.current_deposit, creditcards.card_number 
from clients inner join accounts
on clients.id = accounts.client_id 
inner join creditcards
on accounts.id = creditcards.account_id 
where clients.id = 9898
order by accounts.current_deposit desc 
limit 5 
"""
