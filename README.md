# ProsperityRepo
Link to wiki: https://imc-prosperity.notion.site/prosperity-4-wiki
Using backtester:

```bash
cd /path/to/imc-prosperity-4-backtester

PYTHONPATH=/path/to/imc-prosperity-4-backtester/prosperity4bt \
python3 -m prosperity4bt /path/to/your_algorithm.py <DAYS> \
  --data /path/to/your_data_root \
  --match-trades <all|worse|none> \
  --no-vis
```

`--match-trades` controls how your resting orders interact with historical tape trades: **`all`** (default), **`worse`**, or **`none`**. Omit it to use **`all`**.

Example:

```bash
PYTHONPATH=/path/to/imc-prosperity-4-backtester/prosperity4bt \
python3 -m prosperity4bt /path/to/your_algorithm.py 0 \
  --data /path/to/Prosperity4Data \
  --match-trades something \
  --no-vis
```