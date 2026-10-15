CREATE TABLE persist (
domein VARCHAR(70) ,
botskey VARCHAR(64) ,
content TEXT ,
ts timestamp NOT NULL DEFAULT (datetime('now','localtime')),
PRIMARY KEY (domein, botskey)
);
