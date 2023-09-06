# SSG_PROJECT01

0. 시작전
0.1 install python module 
```python
pip install passlib
pip install flask_cors
pip install flask
pip install mysql
```
0.2 mysql 설치 및 데이터베이스 생성
<details>
<summary>데이터 베이스 SQL</summary>
<div markdown="1">

```sql
create database test3;

use test3;

CREATE TABLE `User` (
    `userId` int unsigned AUTO_INCREMENT NOT NULL ,
    `name` varchar(20)  NOT NULL ,
    `ID` varchar(16)  NOT NULL ,
    `password` varchar(300)  NOT NULL ,
    `phoneNumber` varchar(30)  NOT NULL ,
    `rent` varchar(20) NULL ,
    `status` varchar(10) default 'active' NOT NULL ,
    `createAt` timestamp default CURRENT_TIMESTAMP NOT NULL ,
    `updateAt` timestamp default CURRENT_TIMESTAMP NOT NULL ,
    PRIMARY KEY (
        `userId`
    )
);

CREATE TABLE `Board` (
    `boardId` int unsigned AUTO_INCREMENT NOT NULL ,
    `userId` int unsigned  NOT NULL ,
    `title` varchar(30)  NOT NULL ,
    `content` varchar(1000)  NOT NULL ,
    `location` varchar(20)  NOT NULL ,
    `status` varchar(10) default 'active' NOT NULL ,
    `createAt` timestamp default CURRENT_TIMESTAMP NOT NULL ,
    `updateAt` timestamp default CURRENT_TIMESTAMP NOT NULL ,
    PRIMARY KEY (
        `boardId`
    )
);

CREATE TABLE `Comment` (
    `commentId` int unsigned AUTO_INCREMENT NOT NULL ,
    `userId` int unsigned  NOT NULL ,
    `board_id` int unsigned  NOT NULL ,
    `content` varchar(1000)  NOT NULL ,
    `location` varchar(20)  NOT NULL ,
    `status` varchar(10) default 'active' NOT NULL ,
    `createAt` timestamp default CURRENT_TIMESTAMP NOT NULL ,
    `updateAt` timestamp default CURRENT_TIMESTAMP NOT NULL ,
    PRIMARY KEY (
        `commentId`
    )
);

ALTER TABLE `Board` ADD CONSTRAINT `fk_Board_userId` FOREIGN KEY(`userId`)
REFERENCES `User` (`userId`);

ALTER TABLE `Comment` ADD CONSTRAINT `fk_Comment_userId` FOREIGN KEY(`userId`)
REFERENCES `User` (`userId`);

ALTER TABLE `Comment` ADD CONSTRAINT `fk_Comment_board_id` FOREIGN KEY(`board_id`)
REFERENCES `Board` (`boardId`);
```

</div>
</details>

1. 시작
1-1. FLASK와 데이터 베이스 연결
pybo.py
```python
db = pymysql.connect(host="localhost", 
                     user="root", password="passwd", 
                     db="test3",
                     charset="utf8")
```
host, user, password, db는 환경에 맞춰서 변경하면 된다.


