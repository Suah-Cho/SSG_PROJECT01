## SSG_PROJECT01
#### FLASK를 이용한 CURD기능 만들기

## 서비스 소개
###     소외 계층을 위한 통합 플랫폼
- 참고 레퍼런스
  - 부트텐트  https://boottent.sayun.studio/camps
  - 희망장난감 https://www.yctoy.or.kr/
## 팀원
|이름|포지션|
|:---:|---|
|김기성|로그인기능, 발표자료 담당|
|김서연|팀장, DB table SQL, EC2, 회원 가입 기능|
|신명호|회원 탈퇴 기능, 게시판 기능, 기획서 작성|
|조수아|게시글 페이징, 게시글 작성 및 수정, HTML/CSS|

## 목적 및 필요성

## 핵심 기능

## 기술 스택
<details>
    <summary>Front-end</summary>
    <div markdown='1'>
        
    </div>
</details>
<details>
    <summary>Back-end</summary>
    <div markdown='1'>
        
    </div>
</details>
<details>
    <summary>Infra</summary>
    <div markdown='1'>
        
    </div>
</details>


## System Architecture
<img src='/architecture.png' />

## CI/CD Process

## ERD
<img src='/ERD.png' />

## 개발 과정
1. 시작전<br>
    1.1 install python module 
    ```python
    pip install -r requirements.txt
    ```
    1.2 mysql 설치 및 데이터베이스 생성
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

2. 시작<br>
    2-1. FLASK와 데이터 베이스 연결
    pybo.py
    ```python
    db = pymysql.connect(host="localhost", 
                         user="root", password="passwd", 
                         db="test3",
                         charset="utf8")
    ```
    host, user, password, db는 환경에 맞춰서 변경하면 된다.

3. 이후<br>
    
    
    
