-- Last 5 clients with lowest deposits of a certain bank

select clientm2mbank.client_id, banks.title, accounts.current_deposit 
from clientm2mbank inner join banks
on bank_id = banks.id
inner join clients
on client_id = clients.id 
inner join accounts
on clients.id = accounts.client_id  
where banks.title = 'Bryant Ltd Bank'
order by accounts.current_deposit limit 5
