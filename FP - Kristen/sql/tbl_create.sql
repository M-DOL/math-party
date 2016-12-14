CREATE TABLE  Class(
     name VARCHAR(20) NOT NULL,
     num_correct INT,
     num_attempted INT,
     avg_time INT,
     right_in_a_row INT,
     badge_1 Boolean,
     badge_2 Boolean,
     badge_3 Boolean,
     PRIMARY KEY(name)
);