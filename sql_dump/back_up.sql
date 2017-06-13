CREATE TABLE advertiser (
	id SERIAL primary key,
	advertiser_name TEXT);

CREATE TABLE products(
	id SERIAL primary key,
	product_id TEXT,
	product_name TEXT,
	product_url TEXT,
	advertiser_id integer references advertiser(id), 
	designer TEXT,
	image_url TEXT,
	price NUMERIC(10,2),
	commission NUMERIC(10,2));

Select * from advertiser

Select count(*) from products

Select * from products where product_name = 'Sperry'

Select * from products where product_name Like '%Shoe%' OFFSET 100 LIMIT 100 

Select  P.product_id,
	P.product_name,
	P.product_url,
	A.advertiser_name, 
	P.designer,
	P.image_url,
	P.price,
	P.commission
from products as P 
INNER JOIN advertiser as A 
ON A.id = P.advertiser_id 
where P.price < 10 
AND A.advertiser_name = 'TJ Maxx' 
OFFSET 100 LIMIT 100 

drop table advertiser;

drop table products;

insert into advertiser(advertiser_name) VALUES('Nordstorm Rack');

insert into products(
	product_id,
	product_name,
	product_url,
	advertiser_id, 
	designer,
	image_url,
	price,
	commission) VALUES (
	'8b7a15975779e7c8d7c7e2e98d1b861d',
	'Straight  Fit  Jean  -  30-34"  Inseam',
	'http://rstyle.me/dynamic?t=MD5-YOUR-OAUTH-TOKEN&p=8b7a15975779e7c8d7c7e2e98d1b861d',
	1,
	'Seven7',
	'https://www.hautelookcdn.com/products/SN1885/catalog/5171476.jpg',
	'3084.97',
	'4.20')

SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

DELETE FROM advertiser WHERE advertiser_name = 'Beachbody'
DELETE from products
DELETE FROM advertiser

DELETE FROM advertiser WHERE id = 26
DELETE from products WHERE advertiser_id = 26
SELECT  
									P.product_id,
									P.product_name,
									P.product_url,
									A.advertiser_name, 
									P.designer,
									P.image_url,
									P.price,
									P.commission
								FROM products AS P 
								INNER JOIN advertiser AS A 
								ON A.id = P.advertiser_id 
								where A.advertiser_name LIKE '%Lamborghini%' AND P.designer LIKE '%Suryaa Kumara Relan%' AND P.price <= 100000.0 AND P.price >= 300000.0
								LIMIT 1000 OFFSET 1
