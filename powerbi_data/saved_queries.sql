#My unique JSON records
SELECT  Count(*) as total
FROM user_data ud2 
where ud2.origin_id not in (
	SELECT ud.origin_id 
	FROM user_data ud 
	GROUP BY ud.origin_id
	HAVING COUNT(ud.origin_id) = 2
) and ud2.origin = "JSON"

#My unique YML records
SELECT  Count(*) as total
FROM user_data ud2 
where ud2.origin_id not in (
	SELECT ud.origin_id 
	FROM user_data ud 
	GROUP BY ud.origin_id
	HAVING COUNT(ud.origin_id) = 2
) and ud2.origin = "YML"

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
order by total_sales DESC

#Biggest Shopper
select ei.my_id_value, CAST(udc1.first_names AS CHAR) as first_name,CAST(udc1.last_names AS CHAR) as last_name,CAST(udc1.telephones AS CHAR) as telephone, t1.total_bought 
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
join user_data_consolidated_origin_ids udcoi 
on udcoi.user_data_consolidated_id = udc1.id 
join eorigin_id ei 
on ei.id = udcoi.origin_ids_id
order by t1.total_bought DESC

#Biggest store transaction
select CAST(udc.first_names AS CHAR) as first_name,
CAST(udc.last_names AS CHAR) as last_name,
CAST(udc.telephones AS CHAR) as telephone,
t1.*
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

#Users with promotions
select ei.my_id_value,CAST(udc.first_names AS CHAR) as first_name,
CAST(udc.last_names AS CHAR) as last_name,
CAST(udc.telephones AS CHAR) as telephone, p.promotion_name
from user_data_consolidated udc 
join user_data_consolidated_origin_ids udcoi 
on udcoi.user_data_consolidated_id = udc.id 
join eorigin_id ei 
on ei.id = udcoi.origin_ids_id
join promotions p 
on (p.email = udc.emails and p.telephone_given_at_the_time_of_registration != udc.telephones) 
   or ((p.email != udc.emails and p.telephone_given_at_the_time_of_registration = udc.telephones))
   or ((p.email = udc.emails and p.telephone_given_at_the_time_of_registration = udc.telephones))
   
#User with most received dolar value received transactions
Select  CAST(udc.first_names AS CHAR) as first_name,
CAST(udc.last_names AS CHAR) as last_name,t1.receiverid ,t1.total_transfer_amount
from user_data_consolidated udc 
join user_data_consolidated_origin_ids udcoi 
on udcoi.user_data_consolidated_id = udc.id 
join eorigin_id ei 
on ei.id = udcoi.origin_ids_id
join (
	select mt.receiverid, sum(mt.amount) as total_transfer_amount
	from money_transfers mt 
	group by mt.receiverid
) t1 on t1.receiverid = ei.my_id_value
order by t1.total_transfer_amount DESC

#User with most send dolar value received transactions
Select CAST(udc.first_names AS CHAR) as first_name,
CAST(udc.last_names AS CHAR) as last_name,
t1.senderid  ,t1.total_transfer_amount
from user_data_consolidated udc 
join user_data_consolidated_origin_ids udcoi 
on udcoi.user_data_consolidated_id = udc.id 
join eorigin_id ei 
on ei.id = udcoi.origin_ids_id
join (
	select mt.senderid , sum(mt.amount) as total_transfer_amount
	from money_transfers mt 
	group by mt.senderid 
) t1 on t1.senderid  = ei.my_id_value
order by t1.total_transfer_amount DESC

#Consolidated Count Of Records
select count(*) from user_data_consolidated udc 

#Max number of promotions by user
select CAST(udc.first_names AS CHAR) as first_name,
CAST(udc.last_names AS CHAR) as last_name,
t5.*
from user_data_consolidated udc 
join user_data_consolidated_origin_ids udcoi 
on udcoi.user_data_consolidated_id = udc.id 
join eorigin_id ei 
on ei.id = udcoi.origin_ids_id
join (
	select ei.my_id_value, t1.max_number_of_promos
	from user_data_consolidated udc 
	join user_data_consolidated_origin_ids udcoi 
	on udcoi.user_data_consolidated_id = udc.id 
	join eorigin_id ei 
	on ei.id = udcoi.origin_ids_id
	join (
		select p.*, IFNULL(t2.count_of_phone_promos,0)+IFNULL(t3.count_of_email_promos,0)+IFNULL(t4.count_of_both_promos,0) as max_number_of_promos
		from promotions p 
		left join (
			select p1.telephone_given_at_the_time_of_registration, count(*) as count_of_phone_promos
			from promotions p1 
			where p1.email = ""
		group by p1.telephone_given_at_the_time_of_registration 
	)  t2 on t2.telephone_given_at_the_time_of_registration = p.telephone_given_at_the_time_of_registration 
	left join (
		select p2.email, count(*) as count_of_email_promos
		from promotions p2
		where p2.telephone_given_at_the_time_of_registration = ""
		group by p2.email 
	) t3 on t3.email = p.email
	left join (
		select p3.email, p3.telephone_given_at_the_time_of_registration, count(*) as count_of_both_promos
		from promotions p3
		where p3.telephone_given_at_the_time_of_registration != "" and p3.email != ""
			group by p3.email, p3.telephone_given_at_the_time_of_registration 
		) t4 on t4.email = p.email and t4.telephone_given_at_the_time_of_registration = t4.telephone_given_at_the_time_of_registration
	) t1 on (t1 .email = udc.emails and t1 .telephone_given_at_the_time_of_registration != udc.telephones) 
	   or (t1 .email != udc.emails and t1 .telephone_given_at_the_time_of_registration = udc.telephones)
	   or (t1 .email = udc.emails and t1 .telephone_given_at_the_time_of_registration = udc.telephones)
	group BY ei.my_id_value, t1.max_number_of_promos
) t5 on ei.my_id_value = t5.my_id_value


#Most Sold Item
SELECT  count(*)
from sale_item si
group by si.id

#Most Sold Item
select count(si.name),si.name
from `transaction` t 
join transaction_entries te 
on te.transaction_id = t.id
join item_list_entry ile 
on ile.id = te.entries_id
JOIN sale_item si 
on si.id = ile.item
group by si.name
order by count(si.name) DESC

#Most sold item by store 
select count(si.name),CONCAT(si.name,' at ',t.store_name) as item_store_name
from `transaction` t 
join transaction_entries te 
on te.transaction_id = t.id
join item_list_entry ile 
on ile.id = te.entries_id
JOIN sale_item si 
on si.id = ile.item
group by t.store_name ,si.name
order by count(si.name) DESC

#Average Item value when bougth
select AVG(ile.value_at_purchase),si.name
from `transaction` t 
join transaction_entries te 
on te.transaction_id = t.id
join item_list_entry ile 
on ile.id = te.entries_id
JOIN sale_item si 
on si.id = ile.item
group by si.name
order by AVG(ile.value_at_purchase)  DESC


