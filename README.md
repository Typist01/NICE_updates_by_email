# Python script for sending e-mail notifications on updates to the National Institute for Health and Care Excellence (NICE) guidelines.



### To get started create a .env file with credentials to an e-mail to form an SMTP connection:
`MY_EMAIL="MY_EMAIL@DOMAIN.COM"`

`MY_PASSWORD="MYPASSWORD"`

Run the script to receive updates since the date written in last-checked.txt.
Script should be executed repeatedly (every day) for regular updates.
Cron Jobs in linux might be a good solution
