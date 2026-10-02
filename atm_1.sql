CREATE DATABASE atm_1;
USE atm_1;

CREATE TABLE accounts (
    account_number BIGINT PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    bank VARCHAR(20),
    pin INT NOT NULL,
    balance INT DEFAULT 0
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number BIGINT NOT NULL,
    type VARCHAR(20),
    amount INT,
    balance_after INT,                                  
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES accounts(account_number)
);


CREATE TABLE transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_account BIGINT,
    receiver_account BIGINT,
    amount INT,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_account) REFERENCES accounts(account_number),
    FOREIGN KEY (receiver_account) REFERENCES accounts(account_number)
);

INSERT INTO accounts (account_number, customer_name, bank, pin, balance) VALUES
(1234567890, 'Vinod Raj', 'SBI', 2406, 10000),
(9876543210, 'Anita Sharma', 'SBI', 1111, 5000),
(1122334455, 'Kiran Rao', 'ICICI', 2222, 25000),
(2233445566, 'Priya Nair', 'PNB', 3333, 8000),
(3344556677, 'Arjun Mehta', 'CANARA', 4444, 15000),
(4455667788, 'Sneha Reddy', 'AXIS', 5555, 32000),
(5566778899, 'Rahul Verma', 'HDFC', 6666, 12000),
(6677889900, 'Divya Iyer', 'SBI', 7777, 4500),
(7788990011, 'Manoj Das', 'ICICI', 8888, 60000),
(8899001122, 'Lakshmi Pillai', 'HDFC', 9999, 20000);

INSERT INTO transactions (account_number, type, amount) VALUES
(1234567890, 'Deposit', 500),
(1234567890, 'Withdrawal', 200),
(1234567890, 'Transfer', 1000),
(9876543210, 'Deposit', 2000),
(1122334455, 'Withdrawal', 5000),
(2233445566, 'Deposit', 1500),
(3344556677, 'Transfer', 750),
(4455667788, 'Withdrawal', 3000),
(5566778899, 'Deposit', 1200),
(7788990011, 'Transfer', 10000);


UPDATE transactions t JOIN accounts a ON t.account_number = a.account_number
SET t.balance_after = a.balance WHERE t.id > 0;

SELECT * FROM accounts;
SELECT * FROM transactions;   
SELECT account_number, pin FROM accounts;