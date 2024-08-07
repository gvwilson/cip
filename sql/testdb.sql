delete from signers;

insert into signers(hash, fullname, email, country, affiliation, created, pending)
values
('abc123', 'Alan Turing',       'alan@turing.org', 'UK',    'Bletchley Park', '2022-08-01', 0),
('def456', 'Grace Hopper',      'hopper@navy.gov', 'US',    'Annapolis',      '2022-08-01', 1),
('ghi789', 'Margaret Hamilton', 'mh@hamilton.com', 'US',    NULL,             '2022-08-03', 0);
