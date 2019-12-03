from datetime import datetime
from iexfinance.stocks import get_historical_intraday
import pandas

date = datetime(2019, 2, 5)

print(get_historical_intraday("BTCUSD", date, output_format='pandas'))