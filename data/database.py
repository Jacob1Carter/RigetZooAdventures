SQLite format 3   @                                                                     .O}� � ���Vf�                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              �=''�9tableuser_feedbackuser_feedbackCREATE TABLE user_feedback (
	id INTEGER NOT NULL, 
	question VARCHAR NOT NULL, 
	answer VARCHAR NOT NULL, 
	date_added DATETIME, 
	PRIMARY KEY (id)
)��utableanimalanimalCREATE TABLE animal (
	id INTEGER NOT NULL, 
	species_name VARCHAR(120) NOT NULL, 
	api_name VARCHAR(120) NOT NULL, 
	info VARCHAR, 
	individual_details JSON NOT NULL, 
	image VARCHAR(120) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (species_name)
)+? indexsqlite_autoindex_animal_1animal�!�tableticketticketCREATE TABLE ticket (
	id INTEGER NOT NULL, 
	ticket_holder_id INTEGER NOT NULL, 
	ticket_type VARCHAR(120) NOT NULL, 
	date_added DATETIME, 
	date_expires DATETIME NOT NULL, 
	admit JSON NOT NULL, 
	hotel_rooms VARCHAR, 
	cost FLOAT NOT NULL, 
	PRIMARY KEY (id)
)��tableuseruserCREATE TABLE user (
	id INTEGER NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password_md5 VARCHAR(120) NOT NULL, 
	tickets VARCHAR, 
	is_member BOOLEAN, 
	date_added DATETIME, 
	loyalty_points FLOAT, 
	is_admin BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (email)
)'; indexsqlite_autoindex_user_1user          D �Q��D                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Z	 ;MAbarneyberinger@mail.comebb266a618176c76a58cb23d179eafab2024-04-25 11:09:00.501004X	 7MAdanielalorri@mail.comdbf6691ce92aab1b42d0977c90cc2a852024-04-25 11:09:00.501004U	 1MAreedheath@mail.coma90a19ff7d481d3b267c7ed35d5991252024-04-25 11:09:00.501004V	 3M	ARenaBisset@mail.com597ada0609de4bb72237c3d22d99d2c92024-04-25 11:09:00.501004U	 1M	A	superuser@mail.com82a3f212c95c1516907f27e1220c6f132024-04-25 11:09:00.501004
   � �����                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ;barneyberinger@mail.com7danielalorri@mail.com1reedheath@mail.com3RenaBisset@mail.com1	superuser@mail.com                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 � �
��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              �	 �[�+GiraffegiraffeLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.{"example-name": {"species": "Giraffe", "gender": "male", "birth_date": "20160523000000", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "image": "placeholder.png"}}placeholder.png�	 �[�+TigertigerLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.{"example-name": {"species": "Tiger", "gender": "female", "birth_date": "20160523000000", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "image": "placeholder.png"}}placeholder.png�	 �[�)+ElephantelephantLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.{"example-name1": {"species": "Elephant", "gender": "male", "birth_date": "20160523000000", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "image": "placeholder.png"}, "example-name2": {"species": "elephant", "gender": "female", "birth_date": "20141202000000", "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "image": "placeholder.png"}}placeholder.png
   � ���                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Giraffe	Tiger	Elephant                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         