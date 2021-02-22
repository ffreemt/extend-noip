# extend-noip
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/extend-noip.svg)](https://badge.fury.io/py/extend-noip)

Extend dns expiry date on noip.com

## Installtion

```bash
pip install extend-noip
```
or clone [https://github.com/ffreemt/extend-noip](https://github.com/ffreemt/extend-noip) and install from the repo.

## Usage
### Supply noip `username` and `password` from the command line:
```bash
python -m extend-noip -u your_noip_username -p password
```
or use directly the ``extend-noip`` script:
```bash
extend-noip -u your_noip_username -p password
```

### Use environment variables `NOIP_USERNAME` and `NOIP_PASSWORD`
*   Set username/password from the command line:
	```bash
	set NOIP_USERNAME=your_noip_username  # export in Linux or iOS
	set NOIP_PASSWORD=password
	```
*   Or set username/password  in .env, e.g.,
	```bash
	# .env
	NOIP_USERNAME=your_noip_username
	NOIP_USERNAME=password

Run `extend-noip` or `python -m  extend_noip`:

```bash
extend-noip
```

or

```bash
python -m extend_noip
```

### Check information only

```bash
extend-noip -i
```

or

```bash
python -m extend_noip -i
```

###  Print debug info

```bash
extend-noip -d
```

or

```bash
python -m extend_noip -d
```

### Brief Help

```bash
extend-noip --helpshort
```

or

```bash
python -m extend_noip --helpshort
```

### Turn off Headless Mode (Show the browser in action)

You can configure `NOIP_HEADFUL`, `NOIP_DEBUG` and `NOIP_PROXY` in the `.env` file in the working directory or any of its parent directoreis. For example,

```bash
# .env
NOIP_HEADFUL=1
NOIP_DEBUG=true
# NOIP_PROXY
```

### Automation via Github Actions

It's straightforward to setup `extend-noip` to run via Github Actions, best with an infrequent crontab.
*   Fork this repo
*   Setup `Actions secrets` via `Settings/Add repository secrets`:

|Name | Value |
|--    | --    |
|NOIP_USERNAME:| your_noip_username|
|NOIP_PASSWORD:| your_noip_password |

For example, in `.github/workflows/schedule-extend-noip.yml`
```bash
name: schedule-extend-noip

on:
  push:
  schedule:
    - cron: '10,40 3 */9 * *'
...
setup, e.g. pip install -r requirements.txt or
poetry install --no-dev
...

      - name: Testrun
        env:
          NOIP_USERNAME: ${{ secrets.NOIP_USERNAME }}
          NOIP_PASSWORD: ${{ secrets.NOIP_PASSWORD }}
        run: |
          python -m extend_noip -d -i

```