select udc.email,udc.origin  from user_data udc  group by udc.email,udc.origin HAVING COUNT(udc.email) = 1

# Best selling stores 
select t.store_name, SUM(ile.total_value) as total_sales
from user_data_consolidated udc 
join `transaction` t 
on t.user_telephone = udc.telephones
join transaction_entries te 
on te.transaction_id = t.id
join item_list_entry ile 
on ile.id = te.entries_id
group by t.store_name

#Biggest Shopper
select udc1.first_names,udc1.last_names,udc1.telephones , t1.total_bought 
from (
	select udc.id, sum(ile.total_value) total_bought
	from user_data_consolidated udc 
	join `transaction` t 
	on t.user_telephone = udc.telephones
	join transaction_entries te 
	on te.transaction_id = t.id
	join item_list_entry ile 
	on ile.id = te.entries_id
	group by udc.id
) t1
join user_data_consolidated udc1
on udc1.id = t1.id
order by t1.total_bought DESC

#Biggest transaction
select udc.first_names,udc.last_names,udc.telephones,t1.*
from user_data_consolidated udc 
join (
select t.user_telephone, t.store_name , sum(ile.total_value) as total_value
from `transaction` t 
join transaction_entries te 
on te.transaction_id = t.id
join item_list_entry ile 
on ile.id = te.entries_id
group by t.id
) t1 on t1.user_telephone = udc.telephones
order by t1.total_value DESC

#Total users with promotions
select count((udc.id)) as myid
from user_data_consolidated udc 
join promotions p 
on (p.email = udc.emails and p.telephone_given_at_the_time_of_registration != udc.telephones) 
   or ((p.email != udc.emails and p.telephone_given_at_the_time_of_registration = udc.telephones))
   or ((p.email = udc.emails and p.telephone_given_at_the_time_of_registration = udc.telephones))
   
   
