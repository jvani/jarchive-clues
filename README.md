<h1 align="center" style="border-bottom: none;">jarchive-clues</h1>
<p align="center">
  <img src=https://github.com/jvani/jarchive-clues/workflows/Database%20Update/badge.svg />
</p>

Jeopardy clues from [j-archive.com](http://j-archive.com). Clues are collected with Scrapy, saved to sqlite, and updated daily via GitHub actions.

This project is not affiliated with, sponsored by, or operated by j-archive.com.

## Tables
Two tables are included: `game` and `question`.

```sql
sqlite> SELECT * FROM game LIMIT 3;
id,season,url,description,players,crawled
1,"Season 37",http://www.j-archive.com/showgame.php?game_id=6895,"#8305, aired 2020-12-18","Brayden Smith vs. Amanda Barkley-Levenson vs. Devon Cromwell","2020-12-27 09:53:13.065339"
2,"Season 18",http://www.j-archive.com/showgame.php?game_id=1669,"#4135, aired 2002-07-19","Ron Ellison vs. David Bitkower vs. Lauren Kostas","2020-12-27 10:15:18.243836"
3,"Season 18",http://www.j-archive.com/showgame.php?game_id=1668,"#4134, aired 2002-07-18","Amy Ellis vs. Kate Quillian vs. Ron Ellison","2020-12-27 10:15:18.051032"

sqlite> SELECT * FROM question LIMIT 3;
id,identifier,url,order,value,round,daily_double,category,clue,answer
1,clue_J_1_1,http://www.j-archive.com/showgame.php?game_id=6895,10,200,1,0,"STATES BY COUNTY","Kern, Imperial, Lassen",California
2,clue_J_2_1,http://www.j-archive.com/showgame.php?game_id=6895,23,200,1,0,"RUTH BADER GINSBURG (Alex: A whole category devoted to the late justice.)","Always in style, Justice Ginsburg was famous for wearing ""dissent"" these; a famous one came from Banana Republic","dissent collar"
3,clue_J_3_1,http://www.j-archive.com/showgame.php?game_id=6895,30,200,1,0,"DONATING THEIR WINNINGS","After winning a 2020 tennis tourney in Auckland, Serena Williams donated her winnings to those affected by this nearby disaster","the Australian fires"
```

<details>
<summary>Schema</summary>
<p>

```sql
sqlite> pragma table_info('game');
cid  name         type          notnull  dflt_value  pk  
---  -----------  ----------    -------  ----------  --
0    id           INTEGER       1                    1   
1    season       VARCHAR(255)  1                    0         
2    url          VARCHAR(255)  1                    0         
3    description  VARCHAR(255)  1                    0         
4    players      VARCHAR(255)  1                    0         
5    crawled      DATETIME      0                    0    

sqlite> pragma table_info('question');
cid  name          type          notnull  dflt_value  pk        
---  ------------  ----------    -------  ----------  --
0    id            INTEGER       1                    1         
1    identifier    VARCHAR(255)  1                    0         
2    url           VARCHAR(255)  1                    0         
3    order         INTEGER       0                    0         
4    value         INTEGER       0                    0         
5    round         INTEGER       1                    0         
6    daily_double  INTEGER       1                    0         
7    category      VARCHAR(255)  1                    0         
8    clue          VARCHAR(255)  1                    0         
9    answer        VARCHAR(255)  1                    0
```

</p>
</details>

## Roadmap
See the [open issues](https://github.com/jvani/jarchive-clues/issues) for a list of proposed features (and known issues).

## License
Distributed under the MIT License. See `LICENSE` for more information.
