# article2kindle
Small python script that converts HTML pages into PDFs and send them by email to your [Kindle](https://it.wikipedia.org/wiki/Amazon_Kindle). Surf the Internet, write down the urls of the most interesting articles, call the python script and read the articles on your Kindle.

Tested with Python 3.7.
## Installation
The simplest way is by importing the provided [Anaconda](https://www.anaconda.com/) environment `env.yaml`:
```
$ conda env create -f env.yml
$ source activate kindle
```
Moreover it is required to install [wkhtmltopdf](https://wkhtmltopdf.org/) on your system.
- [Mac OSX](http://macappstore.org/wkhtmltopdf/)
- [Windows](https://pypi.org/project/pdfkit/)
- [Debian/Ubuntu](https://pypi.org/project/pdfkit/)

Finally, open the `conf` file and fill the `wkhtmltopdf_path` variable with the path of the wkhtmltopdf installation on your system.

## How to use it
### Convert web pages to a PDFs and transfer them to your Kindle
#### 1. Find articles that you like
Suppose you see this [OpenAI article](https://openai.com/blog/gpt-2-6-month-follow-up) and this [DeepMind article](https://deepmind.com/blog/article/unsupervised-learning) and you want to read them on your Kindle.
#### 2. Get url and choose a title for that articles
Open the url file and write the following:
```
https://openai.com/blog/gpt-2-6-month-follow-up openai_gpt2_follow_up
https://deepmind.com/blog/article/unsupervised-learning deepmind_unsupervised_learning
```
#### 3. Fill the conf file with your email configurations
Open the conf file and complete with your information:
```
"email_from": "exampleemail@hotmail.it",
"email_from_smtp_host": "smtp.live.com",
"email_from_smtp_port": 587,
"email_to": "kindleemail@kindle.com"
```
You can find [here](https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html) a list of SMTP hosts and ports for several email service providers. As port, choose the one under `StartTLS` authentication.
#### 4. Call python script
Call:
```
python article2kindle.py --html2pdf --pdf2email
```
The script will visit the web pages specified in the url file, convert them to PDF and send emails to your Kindle email account with the PDFs as attachments. If your Kindle is connected to your WIFI, you will see the articles coming to your Kindle in a few moments. They will be called `openai_gpt2_follow_up.pdf` and `deepmind_unsupervised_learning.pdf`.
### Just send some PDFs to my Kindle
Follow the steps 2, 3 and 4.
