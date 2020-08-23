# Parse Gmail Account

Create an Application to pull emails from mailbox and parse them to extract some information.

* Pull Emails from mailbox where sender is abc@gmail.com (it can be any email).
* Save information from email into the database. Include minimum these fields:
    From, CC, To, Subject, Body
* After saving information, run an async job to parse content from email body.
* Check below sample Email Body and expected output.
* Save extracted information in the database table.
* Make the application extendible so that we can use it to extract/parse information from different kinds of emails coming from different email id.


## Enable IMAP in gmail settings.

![alt text](https://github.com/rsharma093/gmail_parser_apis/blob/master/project/resources/enable-imap.png?raw=true)

## Turn on less secure app settings.

![alt text](https://github.com/rsharma093/gmail_parser_apis/blob/master/project/resources/gmail-allow-less-secure-apps.png?raw=true)


[click here](https://myaccount.google.com/lesssecureapps) to turn on.


## Building
Install Redis
```sh
$ brew install redis
```

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv -p python3.7 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Run Server
Run the server.
```sh
$ python manage.py runserver
```

## Run Celery Broker
Run the server.
```sh
$ ../venv/bin/celery -A project.celery_config worker -l info
```

## API Documentation

This API uses `POST` request to parse gmail data. All responses come in standard JSON. All requests must include a `content-type` of `application/json` and the body must be valid JSON.

### Parse Data API

**Request:**
```json
POST /api/accounts/ HTTP/1.1
Accept: application/json
Content-Type: application/json

{
    "user": "your-mail@gmail.com",
    "password": "your-password",
    "sender": "abc@gmail.com"
}
```
**Successful Response:**
```json
HTTP/1.1 201 OK
Content-Type: application/json
{
    "id": 15,
    "created_at": "2020-08-23T14:40:24.631444+05:30",
    "updated_at": "2020-08-23T14:40:24.631626+05:30",
    "user": "your-mail@gmail.com",
    "sender": "abc@gmail.com",
    "parsed_data": [
        {
            "id": 37,
            "created_at": "2020-08-23T14:40:24.658594+05:30",
            "updated_at": "2020-08-23T14:40:24.658633+05:30",
            "message_id": "<wegheiwuufgvewtycgweibsWhgPo6xTMCvvwhr=qA@mail.gmail.com>",
            "from_email": "abc@gmail.com",
            "to_emails": "your-mail@gmail.com",
            "cc_emails": "john@gmail.com,rayn@gmail.com",
            "subject": "Test 123",
            "body": "Phone Number: 979739XXXX\r\n\r\n----------------------------------------------------------\r\n\r\nNumber of submissions received\r\n\r\n15/500 this month\r\n\r\nJuly 17th – August 16th\r\n\r\n\r\n--",
            "date": "2020-08-22T23:31:43+05:30",
            "parsed_body_content": {},
            "account": 15
        },
        {
            "id": 36,
            "created_at": "2020-08-23T14:40:24.654758+05:30",
            "updated_at": "2020-08-23T14:40:24.654801+05:30",
            "message_id": "<qewgdicwhfbEIwfbhDVNLsjYVJOTxsiD_RHhEaVTA@mail.gmail.com>",
            "from_email": "abc@gmail.com",
            "to_emails": "your-mail@gmail.com",
            "cc_emails": null,
            "subject": "Test1234",
            "body": "Email: abc@gmail.com\r\n\r\n----------------------------------------------------------\r\n\r\nNumber of submissions received\r\n\r\n15/500 this month\r\n\r\nJuly 17th – August 16th\r\n\r\n\r\n--",
            "date": "2020-08-23T13:19:31+05:30",
            "parsed_body_content": {},
            "account": 15
        },
    ]
}
```

if no new mail available from sender then response:
```json
{
    "message": "No New Record Found."
}
```
if sender is not found in message list then response:
```json
{
    "message": "No Record Found."
}
```

### List Accounts

**Request:**
```json
GET /api/accounts/ HTTP/1.1
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 15,
            "created_at": "2020-08-23T14:40:24.631444+05:30",
            "updated_at": "2020-08-23T14:40:24.631626+05:30",
            "user": "your-mail@gmail.com",
            "sender": "abc@gmail.com"
        }
    ]
}
```

### Retrieve Account API
After fetching the message information an async task is push in queue and we parse content from email body and save it in **parsed_body_content** field.

**Request:**
```json
POST /api/accounts/<account:id>/?expand=parsed_data HTTP/1.1
```
**Successful Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json
{
    "id": 15,
    "created_at": "2020-08-23T14:40:24.631444+05:30",
    "updated_at": "2020-08-23T14:40:24.631626+05:30",
    "user": "your-mail@gmail.com",
    "sender": "abc@gmail.com",
    "parsed_data": [
        {
            "id": 37,
            "created_at": "2020-08-23T14:40:24.658594+05:30",
            "updated_at": "2020-08-23T14:40:25.027061+05:30",
            "message_id": "<erjniewjnicewkjnewCSTs6-4-EWhgPo6xTMCvvwhr=qA@mail.gmail.com>",
            "from_email": "abc@gmail.com",
            "to_emails": "your-mail@gmail.com",
            "cc_emails": "john@gmail.com,rayn@gmail.com",
            "subject": "Test 123",
            "date": "2020-08-22T23:31:43+05:30",
            "body": "Phone Number: 979739XXXX\r\n\r\n----------------------------------------------------------\r\n\r\nNumber of submissions received\r\n\r\n15/500 this month\r\n\r\nJuly 17th – August 16th\r\n\r\n\r\n--",
            "parsed_body_content": {
                "phone": "979739XXXX",
                "email": null
            },
            "account": 15
        },
        {
            "id": 36,
            "created_at": "2020-08-23T14:40:24.654758+05:30",
            "updated_at": "2020-08-23T14:40:25.031274+05:30",
            "message_id": "<fhvjnerikjnriekjfnvirenfisiD_RHhEaVTA@mail.gmail.com>",
            "from_email": "abc@gmail.com",
            "to_emails": "your-mail@gmail.com",
            "cc_emails": null,
            "subject": "Test1234",
            "body": "Email: abc@gmail.com\r\n\r\n----------------------------------------------------------\r\n\r\nNumber of submissions received\r\n\r\n15/500 this month\r\n\r\nJuly 17th – August 16th\r\n\r\n\r\n--",
            "date": "2020-08-23T13:19:31+05:30",
            "parsed_body_content": {
                "phone": null,
                "email": "abc@gmail.com"
            },
            "account": 15
        },
 
```
 
## Postman Collection
Please check the [postman collection](https://github.com/rsharma093/gmail_parser_apis/blob/master/Gmail_Parser.postman_collection.json) to run APIs.
