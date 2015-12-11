import email, imaplib
from mail_parser import MailParser
import io
import nlp
import json
import jsonpickle
import es

def getEmail():
    user = "letswikit"
    pwd = "wikitrocks"

    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user, pwd)
    # m.select("[Gmail]/INBOX") # here you a can choose a mail box like INBOX instead
    # m.select("[Gmail]/All Mail")
    m.select("inbox")
    # use m.list() to get all the mailboxes

    resp, items = m.search(None,
                           "UNSEEN")  # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    items = items[0].split()

    if len(items) == 0:
        return

    # Get last email
    text = ""
    resp, data = m.fetch(items[-1],
                         "(RFC822)")  # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    raw_email = data[0][1]  # getting the mail content
    # mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

    m.close()
    m.logout()
    text = raw_email
    # with io.open("file", "+w") as file:
    #     file.write(email.message_from_bytes(raw_email))
    #     return
    #
    # Parse email
    parser = MailParser(text)
    results = parser.parse_thread()
    question = results.question

    print(results.json())

    # Run NLP
    keywords = nlp.keywords_from_text(question.content)
    messages = nlp.compute_tf_idf(question, results.messages)
    results.messages = messages
    es.store_thread(results)
    print("All saved");
    # Dump results
    # for m in messages:
    #     print(jsonpickle.encode(m))
