CREATE TABLE IF NOT EXISTS county(
	id serial PRIMARY KEY, 
	name VARCHAR (255) UNIQUE NOT NULL,
	area INT NOT NULL CHECK (area > 0),
	density NUMERIC(6,2) NOT NULL CHECK (density > 0),
	province VARCHAR (255) NOT NULL
);
 
CREATE TABLE IF NOT EXISTS rent(
	id serial PRIMARY KEY NOT NULL,
	advert_id INT NOT NULL,
	rent_amount NUMERIC(6,2) NOT NULL CHECK (rent_amount > 0),
	rent_frequency VARCHAR (6) NOT NULL,
	address TEXT NOT NULL,
	rent_type VARCHAR (255) NOT NULL,
	facilities TEXT,
	ber VARCHAR (255),
   	ber_n INT,
	author VARCHAR (255) NOT NULL,
	description TEXT,
	url VARCHAR (255) NOT NULL, 
	created_at DATE NOT NULL,
	closed_at DATE,
	is_closed BOOLEAN NOT NULL, 
	county INT REFERENCES county (id) ON DELETE SET NULL,
	single_bedroom INT,
	double_bedroom INT,
	bathroom INT,
    furnished VARCHAR (255),
	lease VARCHAR (255),
	address_geo point NOT NULL
);

INSERT INTO county (name, area, density, province) VALUES ('Antrim', 3086, 202.9, 'Ulster'),('Armagh', 1327, 131.8, 'Ulster'),('Carlow', 897,	63.4, 'Leinster'),('Cavan', 1932,	39.3, 'Ulster'),('Clare', 3450,	34.4, 'Munster'),('Cork', 7500,	72.3, 'Munster'),('Donegal',	4861, 32.6, 'Ulster'),('Down', 2489, 215.6, 'Ulster'),('Dublin', 922,	1459.2, 'Leinster'),('Fermanagh', 1691, 36.1, 'Ulster'),('Galway', 6149, 42.0, 'Connacht'),('Kerry', 4807, 30.7, 'Munster'),('Kildare',	1695, 131.0, 'Leinster'),('Kilkenny', 2073, 47.8, 'Leinster'),('Laois', 1720,	49.3, 'Leinster'),('Leitrim', 1590, 20.1, 'Connacht'),('Limerick', 2756, 70.8, 'Munster'),('Londonderry', 2118, 119.1, 'Ulster'),('Longford', 1091, 37.4, 'Leinster'),('Louth', 826, 155.4, 'Leinster'),('Mayo', 5586, 23.3, 'Connacht'),('Meath', 2342, 83.2, 'Leinster'),('Monaghan', 1295, 47.3, 'Ulster'),('Offaly', 2001, 38.9, 'Leinster'),('Roscommon', 2548, 25.3, 'Connacht'),('Sligo', 1838, 35.5, 'Connacht'),('Tipperary', 4305, 37.2, 'Munster'),('Tyrone', 3266, 54.5, 'Ulster'),('Waterford', 1857, 62.7, 'Munster'),('Westmeath', 1840, 48.2, 'Leinster'),('Wexford',	2367, 63.2, 'Leinster'),('Wicklow',	2027, 70.2, 'Leinster');


