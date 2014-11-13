create database iot_project;
use iot_project;

create table sensor_info(
	rfid varchar(100),
	latitude decimal(6,2),
	longitude decimal(6,2),
	record_time datetime
);

create table boundary(
	latitude decimal(6,2),
	longitude decimal(6,2)
);

create table tiger_info(
	tiger_rfid varchar(100),
	dob date
);

commit;