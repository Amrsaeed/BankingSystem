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

INSERT INTO currency (abbreviation) VALUES ('EGP');
INSERT INTO currency (abbreviation) VALUES ('USD');
INSERT INTO currency (abbreviation) VALUES ('EUR');


