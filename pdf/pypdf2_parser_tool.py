import PyPDF2
from datetime import datetime

trades = {}
mapping = {}

def parse(content):
    lines = content.splitlines()
    for line in lines:
        if 'CUSIP:' in line and ('Buy' in line or 'Sell' in line):
            cusip_index = line.find('CUSIP:')
            line = line[cusip_index:]
            # print(line)
            data = line.split()
            cusip = data[1][:9]
            symbol = data[1][9:]
            if not symbol.isupper():
                continue
            if symbol == 'FB':
                symbol = 'META'
            type = data[3]
            date = data[4]
            qty = float(data[5].replace(',', ''))
            price = float(data[6][1:].replace(',', ''))
        
            if cusip not in mapping:
                mapping[cusip] = symbol
            else:
                if mapping[cusip] != symbol:
                    print(f'Error: {cusip} {mapping[cusip]} v.s. {symbol}')
                    return False
            
            if symbol not in trades:
                trades[symbol] = []
            trades[symbol].append((type, date, qty, price))
            
            # print(f'{cusip} {symbol} {type} {date} {qty} {price}')
    return True

def process():
    folder = 'stock'
    years = ['2021', '2022']
    months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    for year in years:
        for month in months:
            try:
                with open(f'{folder}/{year}-{month}.pdf', 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page_num in range(len(pdf_reader.pages)):
                        page_obj = pdf_reader.pages[page_num]
                        content = page_obj.extract_text()
                        if not parse(content):
                            return False
                    pdf_file.close()
            except FileNotFoundError:
                print(f'{folder}/{year}-{month}.pdf not found')
    
    return True

def parse_date(date):
    return datetime.strptime(date, '%m/%d/%Y')

def stock_split(stock, time, qty, price):
    time = parse_date(time)
    if stock == 'SSO':
        if time > parse_date('10/01/2022'):
            qty /= 2
            price *= 2
    elif stock == 'UPRO':
        if time > parse_date('10/01/2022'):
            qty /= 2
            price *= 2
    elif stock == 'TQQQ':
        if time > parse_date('01/15/2022'):
            qty /= 2
            price *= 2
    elif stock == 'TSLA':
        if time > parse_date('10/01/2022'):
            qty /= 3
            price *= 3
    return [time, qty, price]

def calculate(stock, trade):
    buy = []
    sell = []
    for transaction in trade:
        if transaction[0] == 'Buy':
            buy.append(stock_split(stock, transaction[1], transaction[2], transaction[3]))
        else:
            sell.append(stock_split(stock, transaction[1], transaction[2], transaction[3]))
    print(buy, sell)
    buy_amount, sell_amount = 0, 0
    i, j = 0, 0
    while j < len(sell):
        sell_time, sell_qty, sell_price = sell[j][0], sell[j][1], sell[j][2]
        while i < len(buy) and buy[i][0] <= sell_time and sell_qty > 0:
            buy_qty, buy_price = buy[i][1], buy[i][2]
            qty = min(buy_qty, sell_qty)
            if sell_time.year == 2022:
                buy_amount += qty * buy_price
                sell_amount += qty * sell_price
            sell_qty -= qty
            buy[i][1] -= qty
            if buy[i][1] == 0:
                i += 1
        j += 1
    return buy_amount, sell_amount
            
if process():
    print('Done')
    buy_total, sell_total = 0, 0
    for stock, trade in trades.items():
        if '2022' not in trade[-1][1]:
            continue
        print(f'{stock}: ')
        print('Before calculate', trade)
        buy_amount, sell_amount = calculate(stock, trade)
        buy_total += buy_amount
        sell_total += sell_amount
    print(f'Buy: {buy_total}, Sell: {sell_total}, Gain: {sell_total - buy_total}')
else:
    print('Failed')