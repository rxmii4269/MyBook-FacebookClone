DROP DATABASE IF EXISTS comp3161;
CREATE DATABASE comp3161;
USE comp3161;
CREATE TABLE user(
  user_id int NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL,
  email_address VARCHAR(80) NOT NULL,
  telephone VARCHAR(20) NOT NULL,
  dob DATE NOT NULL,
  gender VARCHAR(20) NOT NULL DEFAULT 'Other',
  PRIMARY KEY(user_id),
  CONSTRAINT UC_User UNIQUE(user_id, email_address, telephone)
);
CREATE TABLE profile(
  user_id int NOT NULL,
  profile_id int NOT NULL AUTO_INCREMENT,
  filename VARCHAR(255) DEFAULT 'default.jpg',
  PRIMARY KEY(profile_id, user_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE login(
  user_id int NOT NULL AUTO_INCREMENT,
  username VARCHAR(80) NOT NULL,
  password VARCHAR(255) NOT NULL,
  login_date DATE NOT NULL,
  PRIMARY KEY(username, user_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT UC_Login UNIQUE(user_id, username, password),
  UNIQUE(username)
);
CREATE TABLE friends(
  user_id int NOT NULL,
  friend_id int NOT NULL,
  PRIMARY KEY(user_id, friend_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(friend_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE post(
  user_id int NOT NULL,
  post_id int NOT NULL AUTO_INCREMENT,
  description TEXT NOT NULL,
  PRIMARY KEY(post_id, user_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) CHARSET = utf8mb4 COLLATE utf8mb4_general_ci;


CREATE TABLE photos(
  user_id int NOT NULL,
  photo_id int NOT NULL AUTO_INCREMENT,
  description TEXT NOT NULL,
  filename VARCHAR(255) NOT NULL,
  PRIMARY KEY(photo_id, user_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) CHARSET = utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE photo_comments(
  user_id int NOT NULL,
  photo_id int NOT NULL,
  comment TEXT NOT NULL,
  FOREIGN KEY(photo_id) REFERENCES photos(photo_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) CHARSET = utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE comments(
  user_id int NOT NULL,
  post_id int NOT NULL,
  comment TEXT NOT NULL,
  FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE ON UPDATE CASCADE
) CHARSET = utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE `group`(
  group_id int NOT NULL AUTO_INCREMENT,
  group_name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  PRIMARY KEY(group_id)
);


CREATE TABLE group_members(
  user_id int NOT NULL,
  group_id int NOT NULL,
  role VARCHAR(30) NOT NULL DEFAULT 'member',
  PRIMARY KEY(user_id, group_id),
  FOREIGN KEY(user_id) REFERENCES user(user_id),
  FOREIGN KEY(group_id) REFERENCES `group`(group_id)
);
LOAD DATA LOCAL INFILE 'login.csv' INTO TABLE login FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'friends.csv' INTO TABLE friends FIELDS TERMINATED BY ',' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'posts.csv' INTO TABLE post FIELDS TERMINATED BY ',' IGNORE 1 LINES;



-- Triggers
DELIMITER $$ 
CREATE TRIGGER get_id
AFTER INSERT ON user FOR EACH ROW 
BEGIN
INSERT INTO profile(user_id)
VALUES(new.user_id);
END $$ 
DELIMITER;




DELIMITER $$
CREATE PROCEDURE getAllUsersInformation()
BEGIN
SELECT user.* ,login.username, profile.filename FROM login,user,profile WHERE login.user_id=user.user_id
        AND profile.user_id=user.user_id;
END $$
DELIMITER;

DELIMITER $$
CREATE PROCEDURE getAllUsersGroups(IN user_Id int )
BEGIN
SELECT * FROM `group` where group_id IN (SELECT group_id FROM group_members WHERE user_id=user_Id);
END $$
DELIMITER;

DELIMITER $$
CREATE PROCEDURE regUser(IN firstname varchar(30), IN lastname varchar(30), IN password varchar(20), IN email varchar(40))
BEGIN
INSERT INTO users(firstname,lastname,password,email) values(IN firstname,lastname,password,email);
END $$
DELIMITER;