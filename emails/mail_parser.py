__author__ = 'IronMan'
import io
import re
import email
import jsonpickle
import nlp
from nltk import word_tokenize


class MailParser:
    def __init__(self, text):
        self.text = text

    def parse_thread(self):
        msg = email.message_from_bytes(self.text)
        print(msg.as_string())
        topic = msg["subject"].strip()
        owner = msg["from"]
        date = msg["date"]
        meta = self.parse_meta(date + " , " + owner)

        results = []
        for part in msg.walk():
            if part.is_multipart() or part.get_content_type() != "text/plain":
                continue
            message = part.get_payload(decode=True).decode("utf-8")
            # return
            # print("****************************")
            # print(message)
            # messages = re.split(r'On.+wrote:|From:', message)
            # for m in messages:
            #     print("From: " + m)
            #     print("**************************************")
            results += self.parse_messages(message)
        message_thread = MessageThread(topic, meta["name"], meta["email"], meta["date"], meta["time"], results[0],
                                       results[1:])
        return message_thread

    def parse_messages(self, message):
        emails = [e.strip() for e in re.split(r'On.+wrote:|From:.+', message) if
                  "Begin forwarded message:" not in e.strip() and "Forwarded message" not in e]
        froms = re.findall(r'On.+wrote:|From:.+', message)

        froms = froms
        messages = []
        for i in range(0, len(emails)):
            message = Message()

            meta = self.parse_meta_v3(froms[i] + "\n" + emails[i])


            # print(message.content)
            # print("+++++++++++++++++++++++++++++++++")
            if meta is not None:
                message.sender_name = meta["name"]
                message.sender_address = meta["email"]
                message.time = meta["time"]
            messages.append(message)

            lines = emails[i].splitlines()
            email = []
            for line in lines:
                if line.strip() == "":
                    continue
                if line.startswith(('From', 'To', 'Sent', 'Date', 'Subject', 'Cc', 'Received')):
                    # print(line)
                    email = []
                # elif line.strip().lower() == message.sender_name.lower() or line.strip().lower() == message.sender_name.split()[0].lower():
                elif line.strip().lower() in message.sender_name.lower():
                    email.append(line)
                    break
                else:
                    email.append(line)

            # message.content = re.sub(r'(From|To|Sent|Date|Subject|Cc|Received):.+', '', emails[i], re.MULTILINE).strip()
            message.content = "\n".join(email)
            message.keywords = nlp.keywords_from_text(message.content)
        messages.reverse()
        return messages

    def parse_meta_v3(self, text):
        from commonregex import CommonRegex
        if text.startswith("From:"):
            time = re.sub(r'Date:|Sent:|Received:', "",
                          " ".join(re.findall(r'Date:.+|Sent:.+|Received:.+', text))).strip()
            name = " ".join(re.findall(r'From: [\w\s]+', text)).replace("From:", "").replace("Sent", "").strip()

            parsed = CommonRegex("".join(re.findall(r'From:.+', text)))
            emails = list(set(parsed.emails))
            email = ""
            if len(emails):
                email = emails[0]
            return {"time": time, "name": name, "email": email}
        elif text.startswith("On"):
            line = "".join(re.findall(r'On.+wrote:', text))
            parsed = CommonRegex(line)
            emails = list(set(parsed.emails))
            email = ""
            if len(emails):
                email = emails[0].strip()
            time = " ".join(parsed.times)
            if "AM" not in time and "PM" not in time:
                if "AM" in text:
                    time = time.strip() + " AM"
                else:
                    time = time.strip() + " PM"
            date = "".join(parsed.dates).strip()
            time = date + ", " + time
            names = re.findall(r'[^,]+?<', line)
            name = ""
            if len(names):
                name = names[0].replace("<", "").strip()

            return {"time": time, "name": name, "email": email}
        else:
            return {"time": "", "name": "", "email": ""}

    def parse_meta_v2(self, text):
        sender = [s.replace("From:", ",") for s in re.findall(r'From:.+$', text, re.MULTILINE)]
        date = re.findall(r'Date|Sent:.+', text)
        concatenated = [r.strip() for r in ([" , "] + sender + date)]
        meta = self.parse_meta(" ".join(concatenated))
        return meta

    def parse_meta(self, text):
        if text == "":
            return
        from commonregex import CommonRegex
        parsed_text = CommonRegex(text)
        time = " ".join(parsed_text.times)
        if "AM" not in time and "PM" not in time:
            if "AM" in text:
                time = time.strip() + " AM"
            else:
                time = time.strip() + " PM"
        meta = {
            "time": time,
            "date": " ".join(parsed_text.dates),
            "name": self.find_name(text),
            "email": " ".join(list(set(parsed_text.emails)))
        }
        # print(meta)
        return meta

    def find_name(self, line):
        if "<" not in line:
            return line.replace("From:", "").strip()
        else:
            return " ".join(
                [name.strip() for name in re.findall(r'[\s\w]+', " ".join(re.findall(r',[\s|\w]+<', line)))])


class Message:
    def __init__(self):
        self.sender_name = ""
        self.sender_address = ""
        self.subject = ""
        self.date = ""
        self.time = ""
        self.content = ""
        self.keywords = []
        self.comments = []

    def json(self):
        json = {
            "sender_name": self.sender_name,
            "sender_address": self.sender_address,
            "subject": self.subject,
            "date": self.date,
            "time": self.time,
            "content": self.content,
            "keywords": self.keywords
        }
        comments = []
        for c in self.comments:
            comments.append(c.json())
        json["comments"] = comments
        return json


class MessageThread:
    def __init__(self, topic, owner_name, owner_email, date, time, question, messages):
        self.topic = topic
        self.owner_name = owner_name
        self.owner_email = owner_email
        self.date = date
        self.time = time
        self.question = question
        self.messages = messages
    def json(self):
        json = {
            "topic": self.topic,
            "owner_name": self.owner_name,
            "owner_email": self.owner_email,
            "date": self.date,
            "time": self.time,
            "question": self.question.json(),
            "messages": [m.json() for m in self.messages]
        }
        return json
