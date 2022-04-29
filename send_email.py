import yagmail

port = 465  # For SSL

with open('pass.txt') as f:
    password = f.read()
yag = yagmail.SMTP('appdev.hasanshami@gmail.com', password)


def send_emails(category, content):
    yag.send('hsn.shami@gmail.com', subject="There's been an update in player {}!".format(category), contents=content)
    yag.send('tarek-ko@hotmail.com', subject="There's been an update in player {}!".format(category), contents=content)

