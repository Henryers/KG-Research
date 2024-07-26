create database kg_01;
use kg_01;
create table kg_users(
    `id` int not null auto_increment,
    `username` varchar(255) not null,
    `password` varchar(255) not null,
    `nickname` varchar(255) null,
    `email` varchar(255) null,
    `user_pic` text null,
    primary key (`id`),
    unique index `id_unique` (`id` asc) visible,
    unique index `username_unique` (`username` asc) visible
) comment = '用户信息表';
