DROP DATABASE IF EXISTS homework_help;
CREATE DATABASE homework_help;
USE homework_help;

-- Create user table
CREATE TABLE IF NOT EXISTS app_user (
    account_id INT AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    user_password  VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (account_id)
);

-- Create post table
CREATE TABLE IF NOT EXISTS post (
    post_id INT AUTO_INCREMENT,
    account_id INT NOT NULL,
    date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255) NOT NULL,
    subject_tag VARCHAR(255) NOT NULL,
    main_text VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (account_id) REFERENCES app_user(account_id)
);

-- Create reply table
CREATE TABLE IF NOT EXISTS reply (
    reply_id INT AUTO_INCREMENT,
    main_text VARCHAR(255) NOT NULL,
    post_id INT NOT NULL,
    account_id INT NOT NULL,
    PRIMARY KEY (reply_id),
    FOREIGN KEY(post_id) REFERENCES post(post_id),
    FOREIGN KEY(account_id) REFERENCES app_user(account_id)
);
