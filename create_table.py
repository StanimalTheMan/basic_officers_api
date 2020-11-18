import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# fields (year - for assignments, rank, position title, mos (military occupational specialties)) that are made to be tables since data known beforehand
create_ranks_table = "CREATE TABLE IF NOT EXISTS ranks (id INTEGER PRIMARY KEY, officer_rank TEXT NOT NULL UNIQUE)"
create_position_titles_table = "CREATE TABLE IF NOT EXISTS position_titles (id INTEGER PRIMARY KEY, officer_position_title TEXT NOT NULL UNIQUE)"
create_mos_table = "CREATE TABLE IF NOT EXISTS mos (id INTEGER PRIMARY KEY, mos_job_field TEXT NOT NULL UNIQUE)"

# table for primary resource officers
create_officers_table = "CREATE TABLE IF NOT EXISTS officers (id INTEGER PRIMARY KEY, first_name VARCHAR(20) NOT NULL, last_name VARCHAR(20) NOT NULL, \
                        rank_id INTEGER NOT NULL, position_id INTEGER NOT NULL, mos_id INTEGER NOT NULL, \
                        FOREIGN KEY (rank_id) \
                        REFERENCES ranks (id) \
                          ON UPDATE CASCADE \
                          ON DELETE CASCADE, \
                        FOREIGN KEY (position_id) \
                        REFERENCES position_titles (id) \
                          ON UPDATE CASCADE \
                          ON DELETE CASCADE, \
                        FOREIGN KEY (mos_id) \
                        REFERENCES mos (id) \
                          ON UPDATE CASCADE \
                          ON DELETE CASCADE \
                        )"

create_years_table = "CREATE TABLE IF NOT EXISTS years (id INTEGER PRIMARY KEY, academic_year VARCHAR(10) NOT NULL UNIQUE)"

# basic table for assignments
# probably will have to make tables for fields with known options such as CMU, Assigned Personnel (is personnel officer?), Academic Year, Requirement
# only select fields for now
# in screenshot, fields were:
# - CMU
# - ASSIGNED PERSONNEL 
# - ACADEMIC YEAR 
# - ACADEMIC YR. SEGMENT 
# - REQUIREMENT 
# - OVER HIRE 
# - REMARKS
create_assignments_table = "CREATE TABLE IF NOT EXISTS assignments (id INTEGER PRIMARY KEY, overhire BOOLEAN NOT NULL, remarks TEXT, \
                            officer_id INTEGER NOT NULL, year_id INTEGER NOT NULL, \
                            FOREIGN KEY (officer_id) \
                            REFERENCES officers (id) \
                              ON UPDATE CASCADE \
                              ON DELETE CASCADE, \
                            FOREIGN KEY (year_id) \
                            REFERENCES years (id) \
                              ON UPDATE CASCADE \
                              ON DELETE CASCADE \
                            )"

# table for users aka admins (atm not thinking about different roles separating normal users from admins)
# passwords are plaintext for prototyping purposes
create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, first_name VARCHAR(20) NOT NULL, last_name VARCHAR(20) NOT NULL)"


cursor.execute(create_ranks_table)
cursor.execute(create_position_titles_table)
cursor.execute(create_mos_table)
cursor.execute(create_years_table)
cursor.execute(create_officers_table)
cursor.execute(create_assignments_table)
cursor.execute(create_users_table)

# add default officer ranks
rank_records = [
                  ('Second Lieutenant',),
                  ('First Lieutenant',),
                  ('Captain',),
                  ('Major',),
                  ('Lieutenant Colonel',),
                  ('Colonel',),
                  ('Brigadier General',),
                  ('Major General',),
                  ('Lieutenant General',),
                  ('General',),
                  ('General of the Army',)
                ]
add_ranks_query = "INSERT INTO ranks VALUES (NULL, ?)"
cursor.executemany(add_ranks_query, rank_records)

# add default position titles
position_title_records = [
                            ('DEAN PROFESSOR',),
                            ('VICE DEAN FOR RSRCS',),
                            ('VICE DEAN FOR OPS',) 
                          ]
add_position_titles_query = "INSERT INTO position_titles VALUES (NULL, ?)"
cursor.executemany(add_position_titles_query, position_title_records)

# add default mos fields
mos_records = [
                  ('Native Language Speaker',),
                  ('Infantry',),
                  ('Corps of Engineers',),
                  ('Field Artillery',),
                  ('Air Defense Artillery',),
                  ('Aviation',),
                  ('Cyber Operations Specialist',),
                  ('Special Forces',),
                  ('Armor',),
                  ('Signal Corps',),
                  ('Judge Advocate General\'s Corps',),
                  ('Electronic Warfare',),
                  ('Military Police',),
                  ('Military Intelligence',),
                  ('Financial Management',),
                  ('Psychological Operations',),
                  ('Civil Affairs',),
                  ('Adjutant General\'s Corps',),
                  ('Public Affairs',),
                  ('Acquisition Corps',),
                  ('Chaplain',),
                  ('Medical CMF',),
                  ('Recruiting and Retention',),
                  ('Transportation',),
                  ('Ammunition',),
                  ('Mechanical Maintenance',),
                  ('Quartermaster Corps',),
                  ('Electronic/Missile Maintenance',)
                ]
add_mos_query = "INSERT INTO mos VALUES (NULL, ?)"
cursor.executemany(add_mos_query, mos_records)

connection.commit()
connection.close()

