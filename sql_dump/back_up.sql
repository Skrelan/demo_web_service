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

Select * from products where designer = 'Sperry'

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

