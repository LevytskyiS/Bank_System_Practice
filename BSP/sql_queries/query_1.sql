-- Top 5 clients with biggest deposits

select current_deposit, clients.id, clients.first_name, clients.last_name
from accounts inner join clients
on accounts.client_id = clients.id 
group by current_deposit, clients.id
order by current_deposit desc limit 5