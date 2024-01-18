### Python script for sending e-mail notifications on updates to the National Institute for Health and Care Excellence (NICE) guidelines.



#### To get started create a .env file with credentials to an e-mail to form an SMTP connection:
`MY_EMAIL="MY_EMAIL@DOMAIN.COM"`

`MY_PASSWORD="MYPASSWORD"`

Run the script with to receive updates.
Script should be executed repeatedly (every day) for regular updates using Cron Jobs in Linux for example, or using automation on an external server.
