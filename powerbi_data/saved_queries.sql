select ud.email,ud.origin  from user_data ud  group by ud.email,ud.origin HAVING COUNT(ud.email) = 1

# Best selling stores 
select t.store_name, SUM(ile.total_value) as total_sales
from user_data ud 
join `transaction` t 
on t.user_telephone = ud.telephone
join transaction_entries te 
on te.transaction_id = t.id
join item_list_entry ile 
on ile.id = te.entries_id
group by t.store_name

#Biggest Shopper
select ud1.first_name,ud1.last_name,ud1.telephone, t1.total_bought 
from (
	select ud.id, sum(ile.total_value) total_bought
	from user_data ud 
	join `transaction` t 
	on t.user_telephone = ud.telephone
	join transaction_entries te 
	on te.transaction_id = t.id
	join item_list_entry ile 
	on ile.id = te.entries_id
	group by ud.id
) t1
join user_data ud1
on ud1.id = t1.id

#Biggest transaction
select ud.first_name,ud.last_name,ud.telephone,t1.*
from user_data ud 
join (
select t.user_telephone, t.store_name , sum(ile.total_value) as total_value
from `transaction` t 
join transaction_entries te 
on te.transaction_id = t.id
join item_list_entry ile 
on ile.id = te.entries_id
group by t.id
) t1 on t1.user_telephone = ud.telephone 
order by t1.total_value DESC

#