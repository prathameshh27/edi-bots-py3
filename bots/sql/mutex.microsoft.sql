CREATE TABLE mutex (
mutexk integer PRIMARY KEY NOT NULL,
mutexer integer DEFAULT 0,
ts datetime2 NOT NULL DEFAULT CURRENT_TIMESTAMP
);
