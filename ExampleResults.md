# Data Format Examples

## People JSON
```json
{'id': '0001', 
'first_name': 'Jamie', 
'last_name': 'Bright', 
'telephone': '533-849-3913', 
'email': 'Jamie.Bright@example.com', 
'devices': ['Android'], (NOTE: can be ['Android', 'Iphone'])
'location': {'City': 'Montreal', 
             'Country': 'Canada'}}
```
## People YAML
```
Check if devices, email, id, and name matches with people.json
Check is City matches with Location
Maybe rename phone to telephone to match with people.json
{'Android': '1',                
'Desktop': 1,                 
'Iphone': '1',                  
'city': 'Toronto, Canada',    
'email': 'Yusra.Fletcher@example.com',
'id': '3',                      
'name': 'Yusra Fletcher',     
'phone': '385-702-8874'}      
```

## Transfers CSV
```
Check if matches with id in people.json
Check if matches with id in people.json
{
sender_id  
recipient_id  
amount   
date   
}
```

## EX PROMOTIONS.CSV
```
Check if matches with id in people.json
Might match email in people yaml and json
Check if telephone in people yaml and/or json
Promotion is store name
Responded not in bool format

{
id            
client_email  
telephone     
promotion     
responded     
}
```

## EX TRANSACTIONS.XML
```
Check if id matches with id in people.json, likely doesnt
Items will be an array of items
phone is person's phone number

{
id   
items       
phone       
store     
}
```