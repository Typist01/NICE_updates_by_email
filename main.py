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
        last_checked_date = datetime.datetime.strptime(lines[0].strip(), "%d/%m/%Y")
    except:
        last_checked_date = False;


def send_message(data_list):
    list_string = ""
    for x in data_list:
        list_string += (f'<li class="guide-list-item"><a href="{x["link"]}">{x["name"]}</a><span class="date-text"> updated @ {x["published"]} posted @ {x["last_updated"]}</span> </li>')

    # Create message container - the correct MIME type is multipart/alternative.
    my_email = os.getenv("MY_EMAIL")
    my_password = os.getenv("MY_PASSWORD")
    recipient_name = os.getenv("RECIPIENT_NAME")
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = my_email
    msg['To'] = recipient_email

    styles = """
    *{
      margin: 0;
      padding: 0;
      color: #33C0B0;
    }
    .main-wrapper{
      padding: 3% 7%;
      background-color: #264653;
    }
    .main{
      width: 800px;
      margin: auto;
    }
    .main .heading{
      font-size: 2rem;
    }
    .main .sub-heading{
      font-size: 1.2rem;
    }
    a{
      text-decoration: none;
    }


    .guide-update-list a:link, .guide-update-list a:visited{
      color: #E24E29;
    }
    a:hover{
      text-decoration: underline;
    }

    .guide-update-list{
      margin-top: 50px;
    }


  .guide-list-item a{
    font-size: 1.4rem;
    display: inline-block;
  }
    .guide-list-item{
      list-style-type: none;
      margin-top: 15px;
      border-radius: 6px;
      width: 600px;
      padding: 20px 15px;
      background-color: #F7EAC9;
    }
    .date-text{
      display: block;
      margin-top: 10px;
      color: #1E7067;

    }
        """
    html = f"""\
<html>
  <head>
    <meta charset="utf-8">
    <title> </title>
    <style> 
    {styles}
    </style>
  </head>
  <body style="background-color: #264653;padding: 3% 7%;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
        <td align="center">
  <div class="main-wrapper>
    <div class="main" style="margin:auto;">
    <h1 class="heading"> Hi {recipient_name}</h1>
    <p class="sub-heading">Here is your NICE update</p>
    <ul class="guide-update-list">
{list_string}
    </ul>
  </div>
  </div>
        </td>
    </tr>
</table>
  </body>
</html>
    """


    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=recipient_email, msg=msg.as_string())


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
        if last_checked_date is False or last_checked_date < last_updated:
            print(last_checked_date)
            print(last_updated)
            print(last_checked_date<last_updated)
            item = {"name" : name, "link": link, "published":published.strftime("%d/%m/%Y"), "last_updated": last_updated.strftime("%d/%m/%Y")}
            data_list.append(item)
            f = open("last_checked.txt", "w")
            f.write(datetime.datetime.now().strftime("%d/%m/%Y"))
            f.close()
    return data_list


def run_app():
    data = get_data()

    if len(data) > 0:
        send_message(data)


if __name__ == "__main__":
    run_app()

