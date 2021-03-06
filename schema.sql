create table svn_info(
    s_path_id integer primary key autoincrement,
    s_path_url string not null,
    s_start_revision integer,
    s_last_revision integer
);
create table svn_history (
    id integer primary key autoincrement,
    s_path_id integer,
    s_revision integer,
    s_id text not null,
    s_time text not null,
    s_comment text not null,
    FOREIGN KEY(s_path_id) REFERENCES svn_info(s_path_id)
);
create table svn_history_file(
    id integer primary key autoincrement,
    svn_id INTEGER ,
    file_action text,
    file_path text,
    file_diff text,
    FOREIGN KEY(svn_id) REFERENCES svn_history(id)
);
