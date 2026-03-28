# ProsperityRepo
Link to wiki: https://imc-prosperity.notion.site/prosperity-4-wiki
Using backtester:
cd /path/to/imc-prosperity-4-backtester

PYTHONPATH=/path/to/imc-prosperity-4-backtester/prosperity4bt \
python3 -m prosperity4bt /path/to/your_algorithm.py <DAYS> \
  --data /path/to/your_data_root \
  --no-vis