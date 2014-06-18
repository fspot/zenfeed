ZenFeed
=======

Zen feed reader − inspired by zencancan.


Screenshots
-----------

Feed list :

![feed_list](https://cdn.mediacru.sh/85fg1zEf8fQR.png)

Feed view :

![feed_view](https://cdn.mediacru.sh/pX8d2iWXpHI6.png)

Article view :

![article_view](https://cdn.mediacru.sh/3iiUrJfCRFql.png)

Layout on smartphones :

![layout_mobile](https://cdn.mediacru.sh/2qFVC52hgB6X.png)

Installation
------------

```
$ pip install zenfeed
```


Usage
---

```
$ zenfeed -h
Zen RSS feed reader.

Usage:
  zenfeed [--database URI --favicons PATH -p PORT --log LOG --lang LANG
           --tz TIMEZONE --prefix PREFIX --no-cache --debug]
  zenfeed genstatic PATH
  zenfeed -h | --help
  zenfeed -v | --version

Options:
  -h --help           Show this screen.
  -v --version        Show version.
  -d --database URI   Specify database URI (SQLAlchemy format).
                      For SQLite, this is just a file name.
                      [default: ./zenfeed.db]
  -f --favicons PATH  Specify where favicons will be put.
                      [default: ./]
  -p --port PORT      Specify on which port to listen.
                      [default: 5000]
  --prefix PREFIX     If zenfeed is not alone in its domain/subdomain,
                      specify its path prefix. E.g: /zenfeed/
                      [default: /]
  --log LOG           Specify where to log messages, and which level to set.
                      Can be "stderr", "syslog", or a filename, followed by the level.
                      [default: stderr:INFO]
  --lang LANG         Fix the language instead of let it depend on the browser's value.
                      The language needs to be supported. E.g: en
                      [default: browser]
  --tz TIMEZONE       Specify which timezone to use, to adjust date and time display.
                      For french timezone : "--tz Europe/Paris"
                      [default: GMT]
  --no-cache          Disable cache on index and feed pages.
  --debug             Debug mode, do not use.
```


Todo
----

- Complete this README
