drop table if exists comments;
create table comments (
    id integer primary key autoincrement,
    date string not null,
    update_name string not null,
    text string not null,
    user string not null,
    karma string not null,
    email string not null
);

