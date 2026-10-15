CREATE TABLE persist (
domein VARCHAR(70) ,
botskey VARCHAR(64) ,
content TEXT ,
ts timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (domein, botskey)
);
