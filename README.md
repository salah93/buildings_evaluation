# Evaluate Point of Interest
An app built for [crosscompute]('https://crosscompute.com/docs')

Use google places api to search for nearby places on a queried address.

Must have google places api key saved as environment variable `GOOGLE_KEY`

I built this app to evaluate buildings (looking for schools and metro nearby)

## Requirements
+ python2
+ pip

## Steps
```
# update cc.ini accordingly
$ export GOOGLE_KEY="your-api-key"
$ pip install -r requirements.txt
$ crosscompute run
$ crosscompute serve
```
