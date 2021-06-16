CREATE database IF NOT EXISTS sql6417659;

use sql6417659;

CREATE TABLE IF NOT EXISTS login(
EmployeeID BIGINT PRIMARY KEY NOT NULL AUTO_INCREMENT,
email_id varchar(255) not null,
user_password varchar(255) not null
);
ALTER TABLE login auto_increment=501;




create table if not exists employee(
EmployeeID bigint,
Employee_FName varchar(55) not null,
Employee_LName varchar(55) not null,
dob date not null,
foreign key (EmployeeID) references login(EmployeeID)
);

CREATE TABLE IF NOT EXISTS timesheet_TGT(
                  TimeSheetID BIGINT NOT NULL
                  ,EmployeeID BIGINT
                  ,Day_1 INT
                  ,Day_2 INT
                  ,Day_3 INT
                  ,Day_4 INT
                  ,Day_5 INT
                  ,Day_6 INT
                  ,Day_7 INT
                  ,WeekID BIGINT
                  ,START_DATE DATETIME
                  ,END_DATE DATETIME
                  ,ACTIVE_FLAG CHAR(1) default 'Y'
                  ,FOREIGN KEY (EmployeeID) references login(EmployeeID)
);

-- CREATE TABLE IF NOT EXISTS timesheet_STG
-- (
--                   EmployeeID BIGINT
--                   ,Day_1 INT
--                   ,Day_2 INT
--                   ,Day_3 INT
--                   ,Day_4 INT
--                   ,Day_5 INT
--                   ,Day_6 INT
--                   ,Day_7 INT
--                   ,WeekID BIGINT
--                   ,FOREIGN KEY (EmployeeID) references login(EmployeeID)
-- );
