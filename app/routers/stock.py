from fastapi import APIRouter
import yfinance as yf
import logging

router = APIRouter()


@router.get("/{ticker}")
async def get_stock_data(ticker: str, interval: str = "1d", period: str = "1y"):
    stock = yf.Ticker(ticker)
    stockName = stock.info['shortName']
    data = stock.history(interval=interval, period=period)
    if data.empty:
        logging.info(f"No data found for the given ticker: {ticker}")
        return {"error": "No data found for the given ticker or not a valid ticker"}

    # Convert the DataFrame to a list of dictionaries, with each row as a dictionary
    data_list = data.reset_index().to_dict(orient='records')
    data_list.append({"stockName": stockName})
    print(data_list)
    logging.info(f"Data found for the given ticker: {ticker}")
    return data_list

@router.get("/{ticker}/info")
async def get_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

