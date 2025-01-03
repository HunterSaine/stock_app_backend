from fastapi import APIRouter, Response, HTTPException
import yfinance as yf
import logging

router = APIRouter()


@router.get("/{ticker}")
async def get_stock_data(ticker: str, interval: str = "1d", period: str = "1y"):
    try:
        stock = yf.Ticker(ticker)

        if 'shortName' not in stock.info:
            logging.info(f"No valid data found for ticker: {ticker}")
            raise HTTPException(
                status_code=404, detail="No valid data found for the given ticker"
            )


        data = stock.history(interval=interval, period=period)

        if data.empty:
            logging.info(f"No historical data found for ticker: {ticker}")
            raise HTTPException(
                status_code=404, detail="No historical data found for the given ticker"
            )
        stockName = stock.info['shortName']
        data = stock.history(interval=interval, period=period)
        if data.empty:
            logging.info(f"No data found for the given ticker: {ticker}")
            return {"error": "No data found for the given ticker or not a valid ticker"}

        # Convert the DataFrame to a list of dictionaries, with each row as a dictionary
        data_list = data.reset_index().to_dict(orient='records')
        data_list.append({"stockName": stockName})
        logging.info(f"Data found for the given ticker: {ticker}")
        return data_list
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error occurred while fetching data for the ticker: {ticker}")
        return {"error": "Internal server error occurred while fetching data for the ticker"}


@router.get("/{ticker}/info")
async def get_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    return info

