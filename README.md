# prodmon-datavis-api
A flask based api to pull data from the prodmon database

### Methods:

#### /

  Returns Hellow World as an idiot check the server is working.

### /machine/<partnumber>
  
  Returns a json formated list of machines in the db.  If the optional partnumber is included, it lists the machines that report that part.
  
### /part/<machinenumber>
  
  Returns a json formated list of partnumbers in the db.  If the optional machine number is included, it lists the parts that recorded that machine number.
  
### /counts

  Parmeters:
  
    - machine= comma seperated list of machine numbers to include in the query
    - part= comma seperated list of part numbers to include in the query
    - start= timestamp - start of the first period
    - interval= length of each period in seconds (default 3600 - 1 hour)
    - count= number of periods to query (default 1)

  Note, At least one machine or one part number must be specified or a 400 error is returned
