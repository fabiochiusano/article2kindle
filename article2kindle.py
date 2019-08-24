from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os
import sys
import getpass
import pdfkit
import argparse
import json
import shutil

def read_conf(conf_filename):
    """Read conf from conf file"""
    print("Trying to read {} file...".format(conf_filename))
    try:
        with open(conf_filename) as conf_file:
            conf = json.load(conf_file)
    except EnvironmentError as e:
        print("Couldn't find {} file.".format(conf_filename))
        print(str(e))
        sys.exit(1)
    return conf

def get_email_connection(conf):
    """Connect to email server and check credentials"""
    email_from = conf["email_from"]
    password = getpass.getpass("Insert email password: ")
    email_from_smtp_host = conf["email_from_smtp_host"]
    email_from_smtp_port = conf["email_from_smtp_port"]

    # Check information correctness
    print("Checking if email information are ok...")
    try:
        connection = smtplib.SMTP(host=email_from_smtp_host, port=email_from_smtp_port)
        connection.ehlo()
        connection.starttls()
        connection.login(email_from, password)
    except Exception as e:
        print("Something is wrong with the email information you provided.")
        print(str(e))
        sys.exit(1)

    return connection

def read_urls_and_titles(urls_filename):
    print("Trying to read {} file...".format(urls_filename))
    try:
        urls_and_names = [line.rstrip().split(" ") for line in open(urls_filename, "r")]
    except EnvironmentError as e:
        print("Couldn't find {} file.".format(urls_filename))
        print(str(e))
        sys.exit(1)
    return urls_and_names

def get_pdfkit_conf(conf):
    print("Trying to parse wkhtmltopdf configuration at path {}...".format(conf["wkhtmltopdf_path"]))
    try:
        pdfkit_conf = pdfkit.configuration(wkhtmltopdf=conf["wkhtmltopdf_path"])
    except Exception as e:
        print("Couldn't read wkhtmltopdf configuration at path {}.".format(conf["wkhtmltopdf_path"]))
        print(str(e))
        sys.exit(1)
    return pdfkit_conf

def from_html_to_pdf(conf):
    """Convert HTML pages to PDFs"""
    # Reading urls and titles
    urls_and_names = read_urls_and_titles(conf["urls_filename"])

    # Checking pdfkit configuration
    pdfkit_conf = get_pdfkit_conf(conf)

    # Visiting and transforming HTML pages to PDFs
    print("Visiting HTML pages...")
    for pair in urls_and_names:
        url, name = pair[0], pair[1]
        filename = name + '.pdf'

        print("Trying to convert page {}...".format(url))
        try:
            pdfkit.from_url(url, conf["pdfs_directory_name"] + "/" + filename, configuration=pdfkit_conf, options={'quiet': ''})
        except Exception as e:
            print("Couldn't convert {} to a PDF.".format(url))
            print(str(e))
            continue

        print("Created {filename}".format(filename=filename))

def get_pdf_filenames(pdfs_directory_name):
    filenames = [f for f in os.listdir(pdfs_directory_name) if os.path.isfile(os.path.join(pdfs_directory_name, f))] # list files in the "pdfs" directory
    filenames = [f for f in filenames if f[-4:] == ".pdf"] # send only files whose name ends with ".pdf"
    return filenames

def from_pdf_to_email(conf, connection):
    """Send PDFs to Kindle by email"""
    filenames = get_pdf_filenames(conf["pdfs_directory_name"])
    for filename in filenames:
        complete_filename = conf["pdfs_directory_name"] + "/" + filename
        # Creating message.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "article2kindle - {filename}".format(filename=filename)
        msg['From'] = conf["email_from"]
        msg['To'] = conf["email_to"]

        # The MIME types for text/html
        text = ""
        HTML_Contents = MIMEText(text, 'html')

        # Adding attachments
        print("Trying to read {}...".format(complete_filename))
        try:
            fo = open(complete_filename, 'rb')
            attach = MIMEApplication(fo.read(), _subtype="pdf")
            attach.add_header('Content-Disposition','attachment', filename=filename)
            msg.attach(attach)
            fo.close()
        except Exception as e:
            print("Coulnd't read PDF file {}.".format(complete_filename))
            print(str(e))
            continue

        # Adding body
        msg.attach(HTML_Contents)

        # Send email
        print("Trying to send email...")
        try:
            connection.sendmail(msg['From'], msg['To'], msg.as_string())
        except Exception as e:
            print("Couldn't send email.")
            print(str(e))
            continue

        print("Sent {}.".format(filename))

def clean_pdf_directory(conf):
    shutil.rmtree(conf["pdfs_directory_name"])
    os.makedirs(conf["pdfs_directory_name"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML pages to PDFs and send them to your Kindle by email.")
    parser.add_argument("--html2pdf", action='store_true',
                        help="Convert HTML pages to PDFs.")
    parser.add_argument("--pdf2email", action='store_true',
                        help="Send PDFs to Kindle by email.")
    parser.add_argument("--clean", action='store_true',
                        help="Remove all the PDFs from their directory.")
    args = parser.parse_args()

    conf_filename = "conf.json"

    if args.pdf2email or args.html2pdf or args.clean:
        conf = read_conf(conf_filename)
    if args.pdf2email:
        connection = get_email_connection(conf)
    if args.html2pdf:
        from_html_to_pdf(conf)
    if args.pdf2email:
        from_pdf_to_email(conf, connection)
        connection.quit()
    if args.clean:
        clean_pdf_directory(conf)
