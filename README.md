# Automatic subscription to leftover vaccinations in northen jutland
For each config in subs makes a subscription for leftover vaccinations.

## subs 
```json
{
  "name": "The name of the person to subscribe for",
  "age": "The age of the person",
  "phone": "The phone number of the person",
  "email": "The email of the person"
}
```

Then we headless emulate the clicks required to fill out the form for subscribing to leftover vaccinations.

And after this have completed, then sends a mail to the person, that we've successfully subscribed them for the leftover vaccinations

## mail
An SMTP server is required to send mail (durh), currently only gmail is supported.

In the config.json file, insert your gmail account mail, and generate a applications specific password here:

https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637569503595505208-1415581680&rd=1

## Requirements
Besides the python pacakages listed in requirements.txt, the we also need xvfe to emulate a xorg server in a headless env.
(essentially so that it can be ran on a server without X installed)

debian:

`apt install xvfe`

arch:

`pacman -S xorg-server-xvfb`


## Usage
As this is a selfcontained script, all you have to do to run it.
A good way of having this running every day is to use a CRON job, or equivalent.

a jobber job could look like
```
RestVaccineScript:
     cmd: /path/to/rest-vac/venv/bin/python /path/to/rest-vac/main.py
     time: '0 0 8 * * *'
     onError: Backoff
```

A cron job could look like:
```
0 8 * * * /path/to/rest-vac/venv/bin/python /path/to/rest-vac/main.py
```


