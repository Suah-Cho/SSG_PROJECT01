## SSG_PROJECT01
#### FLASK를 이용한 CURD기능 만들기

## 서비스 소개
필요한 물품 혹은 필요 없는 물품을 서로 공유하며 더 좋은 세상으로 한 걸음 나아가는 커뮤니티입니다.

- [배포 URL](https://first-step.shop)
- [기획서](https://docs.google.com/document/d/11NMLUzRPwFe9vcNbvCp-_t1hVwUOghqN/edit?usp=drive_link&ouid=116282982421138719470&rtpof=true&sd=true)
- [발표 자료](https://drive.google.com/file/d/1LlYdZ1EYSi-Gk7nqZf_WpNbB_drjYU8F/view?usp=drive_link)
  
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
![Static Badge](https://img.shields.io/badge/Python3-3776AB?logo=Python&logoColor=%23FFFFFF) ![Static Badge](https://img.shields.io/badge/HTML5-E34F26?logo=HTML5&logoColor=%23FFFFFF) ![Static Badge](https://img.shields.io/badge/Flask-000000?logo=Flask&logoColor=%23FFFFFF) ![Static Badge](https://img.shields.io/badge/AWS-FF9900?logo=Amazon%20AWS&logoColor=%23FFFFFF) <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=MySQL&logoColor=white"/>

## 개발 환경
- OS : ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
- Editor : ![Static Badge](https://img.shields.io/badge/VSCode-007ACC?logo=Visual%20Studio%20Code&logoColor=%23FFFFFF)

## System Architecture
<img src='/architecture.png' />

## 순서도
<img src='/flow.jpg' />


## ERD
<img src='/ERD.png' />

## 설치 가이드
1. <br>
    1.1 install python module 
    ```python
    pip install -r requirements.txt
    ```
    <br>
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

    CREATE TABLE `ToyBoard` (
    	`boardId` int unsigned AUTO_INCREMENT NOT NULL , 
    	`userId` int unsigned NOT NULL, 
    	`title` varchar(100) NOT NULL, 
    	`content` varchar(1000) NOT NULL, 
    	`userage` varchar(20) NOT NULL, 
    	`area` varchar(20) NOT NULL, 
    	`phoneNumber` varchar(30) NOT NULL,  
    	`rent` varchar(20) default '가능' NOT NULL, 
    	`status` varchar(10) default 'active' NOT NULL,
    	`createAt` timestamp default CURRENT_TIMESTAMP NOT NULL, 
    	`updateAt` timestamp default CURRENT_TIMESTAMP NOT NULL, 
    	PRIMARY KEY( `boardId` )
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

    1-3. 공공데이터 csv 데이터베이스에 저장하기
   ```python
     toy = pd.read_csv('SSG_PROJECT01/전북 진안군_장난감 보유 현황.csv', sep=',', index_col=0)

    #데이터베이스에 csv정보 저장
    for i in range(1, len(toy)+1) :
      list = toy.loc[i].str.split('   ').str[0].tolist()
      curosr.execute("INSERT INTO ToyBoard (userId, title, content, userage, area, phoneNumber) VALUES (1, CONCAT(%s,' - ',%s), %s, %s, '전북 진안군', %s);", 
                          (list[0], list[2], list[4], list[3], list[6]))
      curosr.connection.commit()
   ```

3. <br>
    2-1. FLASK와 데이터 베이스 연결<br>
    pybo.py <br><br>
    
    ```python
    db = pymysql.connect(host="localhost", 
                         user="root", password="passwd", 
                         db="test3",
                         charset="utf8")
    ```
   
    host, user, password, db는 환경에 맞춰서 변경하면 된다.



- 참고 레퍼런스
  - 부트텐트  https://boottent.sayun.studio/camps
  - 희망장난감 https://www.yctoy.or.kr/
    
    
## 수정사항
1. 제목, 지역 수정가능하게 하기
   - board delete했을 때 해당 url로 갈 수 있으므 -> '삭제된 게시물입니다.'alert띄워보기
   - edit.html에서 text대신 textarea로 받아보기 -> 해결
   - view.html에서 본문 textarea를 수정안되게 만들 수 있는 지 확인해보기 -> 해결
