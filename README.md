# gptfdw  

PostreSQL FDW for ChatGPT (BotHub).  
- This FDW supports single requests to OpenAI ChatGPT;
- Model is gpt-3.5-turbo-16k;
- You need to apply your own access token on <a href='https://bothub.chat/'>BotHub</a>;
## Installation (Ubuntu)
This FDW is based on <a href='https://github.com/pgsql-io/multicorn2'>Multicorn2</a>.  
Installation is pretty easy, just follow the steps below:
1. Firstly you need to install <a href='https://github.com/pgsql-io/multicorn2'>Multicorn2</a>.   
2. Then clone this repo:
```
$ git clone https://github.com/infimum05772/gptfdw
```
3. After that copy **gptfdw.py** into your multicorn folder:
```
$ cp gptfdw/gptfdw.py [multicorn folder]
```
## PostgresSQL
- Replace access token with your token.
```
create extension multicorn;

CREATE SERVER gptfdw_srv FOREIGN DATA WRAPPER multicorn 
OPTIONS ( wrapper 'multicorn.gptfdw.gptfdw', 
                   access_token 'your token' );
                  
CREATE FOREIGN TABLE gptfdw ( 
  query text,
  temp numeric,
  model text, 
  content text, 
  prompt_tokens int,   
  completion_tokens int,
  total_tokens int,
  error text
) SERVER gptfdw_srv;
```
## Sample queries
```
SELECT * FROM gptfdw WHERE query='hello';
 query | temp |         model          |              content               | prompt_tokens | completion_tokens | total_tokens | error
-------+------+------------------------+------------------------------------+---------------+-------------------+--------------+-------
 hello |  0.7 | gpt-3.5-turbo-16k-0613 | Hello! How can I assist you today? |             8 |                 9 |           17 |
```
```
SELECT * FROM gptfdw WHERE query='give me some cat names' and temp=1.7;
         query          | temp |         model          |   content   | prompt_tokens | completion_tokens | total_tokens | error
------------------------+------+------------------------+-------------+---------------+-------------------+--------------+-------
 give me some cat names |  1.7 | gpt-3.5-turbo-16k-0613 | 1. Luna    +|            12 |                85 |           97 |
                        |      |                        | 2. Oliver  +|               |                   |              |
                        |      |                        | 3. Whiskers+|               |                   |              |
                        |      |                        | 4. Lily    +|               |                   |              |
                        |      |                        | 5. Leo     +|               |                   |              |
                        |      |                        | 6. Tigger  +|               |                   |              |
                        |      |                        | 7. Daisy   +|               |                   |              |
                        |      |                        | 8. Charlie +|               |                   |              |
                        |      |                        | 9. Chloe   +|               |                   |              |
                        |      |                        | 10. Shadow +|               |                   |              |
                        |      |                        | 11. Max    +|               |                   |              |
                        |      |                        | 12. Bella  +|               |                   |              |
                        |      |                        | 13. Mochi  +|               |                   |              |
                        |      |                        | 14. Milo   +|               |                   |              |
                        |      |                        | 15. Nala   +|               |                   |              |
                        |      |                        | 16. Simon  +|               |                   |              |
                        |      |                        | 17. Coco   +|               |                   |              |
                        |      |                        | 18. Finn   +|               |                   |              |
                        |      |                        | 19. Hazel  +|               |                   |              |
                        |      |                        | 20. Oscar   |               |                   |              |
```
