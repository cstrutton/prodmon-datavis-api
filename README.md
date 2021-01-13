# prodmon-datavis-api
A flask based api to pull data from the prodmon database

### Methods:

#### /
  Returns Hellow World as an idiot check the server is working.

### /machine/<partnumber>
  Returns a json formated list of machines in the db.  If the optional partnumber is included, it lists the machines that report that part.
  
### /part/<machinenumber>
  Returns a json formated list of partnumbers in the db.  If the optional machine number is included, it lists the parts that recorded that machine number.
  
### /counts?machine=/[machine numbers/]&part=/[part numbers/]
