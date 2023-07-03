CREATE SCHEMA sales_source;

SET search_path TO sales_source;


DROP TABLE IF EXISTS sales_source.sales_data;
CREATE TABLE IF NOT EXISTS sales_source.sales_data
(
    id serial primary key,
    item text,
    price double precision,
    CONSTRAINT unique_constraint_for_upsert_boxscores UNIQUE (id)
);

INSERT INTO sales_source.sales_data(item, price)
VALUES ('Shoes', 30),
       ('Sandals', 25),
       ('Hat', 5);

DROP TABLE IF EXISTS sales_source.feature_flags;
CREATE TABLE IF NOT EXISTS sales_source.feature_flags
(
	id serial primary key,
	flag text,
	is_enabled integer,
	created_at timestamp without time zone default now(),
	modified_at timestamp without time zone default now(),
    CONSTRAINT flag_unique UNIQUE (flag)
);
INSERT INTO sales_source.feature_flags(flag, is_enabled)
VALUES ('season', 1),
       ('playoffs', 1),
       ('pbp', 1),
       ('twitter', 1),
       ('reddit_posts', 1),
       ('reddit_comments', 1),
       ('boxscores', 1),
       ('injuries', 1),
       ('transactions', 1),
       ('stats', 1),
       ('adv_stats', 1),
       ('opp_stats', 1),
       ('odds', 1),
       ('schedule', 1),
       ('shooting_stats', 1),
       ('fake', 0);