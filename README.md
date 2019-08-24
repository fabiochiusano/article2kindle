# article2kindle
Small python script that converts HTML pages into PDFs and send them by email to your [Kindle](https://it.wikipedia.org/wiki/Amazon_Kindle).

## Installation
The simplest way is by importing the provided [Anaconda](https://www.anaconda.com/) environment `env.yaml`:
```
$ conda env create -f env.yml
$ source activate kindle
```
Moreover it is required to install [wkhtmltopdf](https://wkhtmltopdf.org/) on your system.
- [Mac OSX](http://macappstore.org/wkhtmltopdf/)

Finally, open the `conf` file and fill the `wkhtmltopdf_path` variable with the path of the wkhtmltopdf installation on your system.

## How to use it
### Convert a web page to a PDF and transfer it on your Kindle
#### 1. Find articles that you like
Suppose you see this [OpenAI article](https://openai.com/blog/gpt-2-6-month-follow-up) and this [DeepMind article](https://deepmind.com/blog/article/unsupervised-learning) and you want to read them.
#### 2. Get url and choose a title for that article
Open the url file and write the following:
```
https://openai.com/blog/gpt-2-6-month-follow-up openai_gpt2_follow_up
https://deepmind.com/blog/article/unsupervised-learning deepmind_unsupervised_learning
```
#### 3. ...
