# Negadys
## In-Memory Key-Value Database

### What is an In-Memory Key-Value Database?
A key-value database is a type of non-relational database that 
uses a simple key-value method to store data. 
A key-value database stores data as a collection of key-value pairs 
in which a key serves as a unique identifier. 
Source: [AWS Docs](https://aws.amazon.com/nosql/key-value/#:~:text=A%20key-value%20database%20is,objects%20to%20complex%20compound%20objects.)

### How to run the program
This program is written in Python version 3.8.
To start the service, run the following command in the main directory of the project:

`python main.py`

### Accepted Commands
The accepted commands are all the requested commands in the interview task description.

`set key value`, `get key`, `del key`, `keys regex`, 
`use db_name`, `list`, `dump db_name path`, `load path db_name`, and `exit`.

*Note:* For `dump` command, if path is not assigned to the command, 
the default path from `config.py` will be used.

### Dependencies
The program requires no more than Python 3.8 and its default packages.

### Unittest
Most of the implemented methods has been tested by unittest. 
You can find the test cases in the `test/unit/` directory.

### What next?
- The program can be extended to support more commands by 
making changes to `server_handler.py`.
- The dump files could be hashed to avoid unauthorized access.
- Right now, the program works for single simultaneous access. In case concurrency is needed, the program should be altered to support `async IO`. 
- In case of multiple simultaneous access to the server, a re-design may be needed. 
It may be easier to design the program with frameworks such as `Fast API`.# negadys project
