# AutoCompleteSystem
## 1. Instruction:
   Please follow the instruction step by step.
   ### 1.1 
   Run ```python main.py```  
   ### 1.2
  #### 1.2.1 GET
   Run ```curl http://127.0.0.1:8000/query?item=```  
   Example:   
   ![image](https://github.com/VictoriaZJZhao/AutoCompleteSystem/blob/main/example/query.png)
  #### 1.2.2 POST 
   1. First, you should login to get the admin access. Otherwise, you can't get the access to update the dictionary. And you can get an access token which will be expired after 2 minutes.  
   Run ```curl -H "Content-Type: application/json" -X POST  -d '{"username":"admin","password":"123456"}' http://localhost:8000/login```   
   2. Second, update the dictionary as you want.  
       ##### ADD 
       Run ```curl -i -X POST -H 'Authorization:Bearer access_token' http://127.0.0.1:8000/add?location=``` 
       ##### DELETE
       Run ```curl -i -X POST -H 'Authorization:Bearer access_token' http://127.0.0.1:8000/delete?location=```   
   Example:
   ![image](https://github.com/VictoriaZJZhao/AutoCompleteSystem/blob/main/example/add.png)
   ![image](https://github.com/VictoriaZJZhao/AutoCompleteSystem/blob/main/example/delete.png)
## 2. Assumptions and tradeoff:
   ### 2.1 Assumptions  
     This system is designed for autocomplete in English version and it is supported by insensitvie search of upper letters and lower letters.  
     It's built by flask.  
     1. Storage  
     It's stored in the a trie tree structure.  
     2. Security  
     It's supported by JWT. So when a user wants to update the word, the user needs to get the access token from admin account.  
     3. Cache  
     To respond faster, the system would store cache and last for 100 seconds.
     4. Rate Limit
     To limit rate, the user could only use the autocomplete system 2000 times per day and 50 times per hour.
     5. Concurrency
     To ensure concurrency, the readwriter lock is designed. Only one user could write at the same time but many users could read at the same time. Write and read are exclusive. And the readers have higher priority.
   ### 2.2 Tradeoff   
     1. There are many kinds of languages in the file, I couldn't handle all situations due to my limited time and limited language knowledge. For example, the transfermation between Chinese Simplified and Chinese Traditional, Japanese Katakana and Japanese Hiragana. Only the English part can be handled. 
     2. This system is stored in the memory because of its size, higher effiency and immediate use. The tradeoff is that it would loss all data once the program stops to excute. 
     3. For CAP theorem, this system tried its best to ensure availability and Partition tolerance. Because availability and consistency could only contain at most one simultaneously. And according to the cache mechanism, availability has higher priority so the lock is designed for higher priority for readers. The tradeoff is consistency. The worst situation is that users couldn't get the latest result and starvation of writers.  
     4. For security part, it is much more dangerous to use basic auth and put the account information in the request each time. So JWT token is designed but the tradeoff is inconvenience.
     
     
   
