create table if not exists signers(
  -- identify this record
  hash text primary key,

  -- just what it says on the box
  fullname text not null,

  -- used only for confirmation
  email text not null,

  -- optional
  country text,

  -- optional
  affiliation text,

  -- YYYY-MM-DD record creation time
  created text not null,

  -- still waiting for confirmation?
  pending boolean not null
);
