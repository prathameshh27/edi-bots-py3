CREATE TABLE persist (
domein nvarchar(70) NOT NULL,
botskey nvarchar(64) NOT NULL,
content nvarchar(max) ,
ts datetime2 NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (domein, botskey)
);
