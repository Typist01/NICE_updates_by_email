import datetime

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
URL = "https://www.nice.org.uk/guidance/published?ndt=Guidance&ndt=Quality%20standard"
root_URL = "https://www.nice.org.uk"

# headers_dict = {
#     "User-Agent": "Defined",
#     "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
# }

with open("last_checked.txt") as f:
    lines = f.readlines()
    try:
        last_checked_date = datetime.datetime.strptime(lines[0], "%d/%m/%Y")
    except:
        last_checked_date = False;


def send_message(data_list):
    list_string = ""
    for x in data_list:
        list_string += (f'<br> <p> <a href="{x["link"]}"> {x["name"]} </a> published @  {x["published"]} last updated @  {x["last_updated"]} </p> <br>');
    # Create message container - the correct MIME type is multipart/alternative.
    my_email = os.getenv("MY_EMAIL")
    my_password = os.getenv("MY_PASSWORD")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = os.getenv("MY_EMAIL")
    # msg['To'] = "testing.mmn2@gmail.com"

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = f"""\
    <html>
      <head></head>
      <body>
        <p>Hi! here are the latest updates {f"since {last_checked_date} " if (last_checked_date) else ""}from NICE
           {list_string}
        </p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    print("before connection")
    with smtplib.SMTP("smtp-mail.outlook.com") as connection:
        connection.ehlo();
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs="testing.mmn2@gmail.com", msg=msg.as_string())



def get_data():
    data_list = []
    response = requests.get(url=URL)
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    section = soup.find(name="tbody")
    data = soup.find_all("tr")

    for x in data[1:]:
        name = (x.td.a.text)
        link = root_URL + (x.td.a.get("href"))
        published = datetime.datetime.strptime(x.find_all("td")[2].time["data-shortdate"], "%d/%m/%Y")
        last_updated = datetime.datetime.strptime(x.find_all("td")[3].time["data-shortdate"], "%d/%m/%Y")  # date
        if (last_checked_date==False or last_checked_date < last_updated):
            item = {"name" : name, "link": link, "published":published.strftime("%d/%m/%Y"), "last_updated": last_updated.strftime("%d/%m/%Y")}
            data_list.append(item);
            f = open("last_checked.txt", "w")
            f.write(datetime.datetime.now().strftime("%d/%m/%Y"))
            f.close()
    return data_list


def run_app():
    data = get_data();
    if (len(data) > 0 ):
        send_message(data)


run_app()