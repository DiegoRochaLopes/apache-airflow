\connect db_origem

CREATE TABLE tb1
(
    id int NOT NULL,
    dummy varchar,
    CONSTRAINT tb1_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

insert into tb1
select
    i,
    md5(random()::varchar)
from generate_series(1, 1000000) s(i);