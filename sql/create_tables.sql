create database if not exists dict_online;

use dict_online;

create table if not exists words(
    id int primary key auto_increment,
    word varchar(32) unique not null,
    mean varchar(1024)
);

create table if not exists users(
    id int primary key auto_increment,
    name varchar(32) unique not null,
    password char(64)
);

create table if not exists history(
    id int primary key auto_increment,
    users_id int,
    words_id int,
    time DATETIME default now(),
    foreign key(users_id) references users(id)
    on delete cascade on update cascade,
    foreign key(words_id) references words(id)
);

