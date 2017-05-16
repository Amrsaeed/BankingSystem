delete from users where 1=1;
delete from transaction where 1=1;
delete from phonenumber where 1=1;
delete from account where 1=1;
delete from currency where 1=1;
delete from accounttype where 1=1;
delete from customer where 1=1;
drop table users;
drop table transaction;
drop table account;
drop table phonenumber;
drop table currency;
drop table accounttype;
drop table customer;
drop sequence account_seq;
drop SEQUENCE users_seq;
drop SEQUENCE transaction_seq;
CREATE TABLE customer
(
	customerID number(10) CONSTRAINT customer_customerId_pk PRIMARY KEY,
	lName varchar2(10) CONSTRAINT customer_lName_nn NOT NULL, 
	fName varchar2(10) CONSTRAINT customer_fName_nn NOT NULL,
	email varchar2(20) ,
	address varchar2(50)
);

CREATE TABLE accountType
(
	name varchar2(10) CONSTRAINT accountType_name_pk PRIMARY KEY,
	ceiling NUMBER CONSTRAINT accountType_ceiling_nn NOT NULL,
	interest NUMBER DEFAULT 0
);

CREATE TABLE currency
(
	abbreviation varchar2(3) CONSTRAINT currency_abbreviation_pk PRIMARY KEY
);
CREATE TABLE account
(
	accountNum number(10) CONSTRAINT account_accountNum_pk PRIMARY KEY,
	accountType varchar2(10),
	currency varchar2(3) ,
	customerId number(10),
	balance number DEFAULT 0,
	CONSTRAINT account_customerId_fk FOREIGN KEY(customerId) REFERENCES customer(customerId),
	CONSTRAINT account_accountType_fk FOREIGN KEY(accountType) REFERENCES accountType(name),
	CONSTRAINT account_currency_fk FOREIGN KEY(currency) REFERENCES currency(abbreviation)
);

CREATE TABLE phoneNumber
(
	customerID number(10),
	phoneNum varchar2(15) CONSTRAINT phoneNumber_phoneNum_nn NOT NULL,
	CONSTRAINT phoneNumber_Id_phoneNum_pk PRIMARY KEY(customerId,phoneNum),
	CONSTRAINT phoneNumber_customerId_fk FOREIGN KEY(customerId) REFERENCES customer(customerId)
);

CREATE TABLE transaction
(
	transNum number(10) CONSTRAINT transaction_transNum_pk PRIMARY KEY,
	type char CONSTRAINT transaction_type_nn NOT NULL,
	transDate DATE CONSTRAINT transaction_transDate_nn NOT NULL,
	amount number CONSTRAINT transaction_amnt_nn	NOT NULL,
	accountNum number(10) CONSTRAINT transaction_accountNum_nn	NOT NULL,
	CONSTRAINT transaction_accoutNum_fk FOREIGN KEY(accountNum) REFERENCES 		account(accountNum)
);

CREATE TABLE users
(
	id NUMBER(10) CONSTRAINT users_id_nn NOT NULL,
	username varchar2(20) CONSTRAINT users_username_nn NOT NULL,
	password varchar2(20) CONSTRAINT users_password_nn NOT NULL,
	type NUMBER(1,0) CONSTRAINT users_type_nn NOT NULL,
	customerID number(10) CONSTRAINT users_customerID_nn NOT NULL,
	CONSTRAINT users_customerID_fk FOREIGN KEY(customerID) REFERENCES customer(customerID),
	CONSTRAINT users_customerID_unique UNIQUE (customerID)
);



ALTER TABLE users ADD (CONSTRAINT users_id_pk PRIMARY KEY (id) );
CREATE SEQUENCE users_seq START WITH 1;

CREATE OR REPLACE TRIGGER users_bid
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
	SELECT 	users_seq.NEXTVAL
	INTO	:new.id
	FROM 	dual;
END;
/

CREATE SEQUENCE account_seq START WITH 1;

CREATE OR REPLACE TRIGGER account_bid
BEFORE INSERT ON account
FOR EACH ROW
BEGIN
	SELECT 	account_seq.NEXTVAL
	INTO	:new.accountnum
	FROM 	dual;
END;
/

CREATE SEQUENCE transaction_seq START WITH 111;

CREATE OR REPLACE TRIGGER transaction_bid
BEFORE INSERT ON transaction
FOR EACH ROW
BEGIN
	SELECT 	transaction_seq.NEXTVAL
	INTO	:new.transNum
	FROM 	dual;
END;
/
INSERT INTO accountType (name, ceiling, interest) VALUES ('Debit', 5000, 12);
INSERT INTO accountType (name, ceiling, interest) VALUES ('Current', 5000, 12);
INSERT INTO accountType (name, ceiling, interest) VALUES ('Saving', 5000, 12);
INSERT INTO currency (abbreviation) VALUES ('EGP');
INSERT INTO currency (abbreviation) VALUES ('USD');
INSERT INTO currency (abbreviation) VALUES ('EUR');
INSERT INTO customer values(1234,'ewais','ahmed','a.ewais@aucegypt.edu','egypt');
INSERT INTO customer values(12345,'saeed','amr','amr@aucegypt.edu','egypt');
insert into users values(users_seq.nextval,'3wais','password',1,1234);
insert into users values(users_seq.nextval,'amr','password',0,12345);

