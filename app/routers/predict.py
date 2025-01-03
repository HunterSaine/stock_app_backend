import yfinance as yf
from fastapi import APIRouter, HTTPException
import logging
from prophet import Prophet
import pandas as pd

router = APIRouter()


@router.get("/{ticker}")
async def predict_stock_price(ticker: str):
    data = yf.Ticker(ticker).history(period="2y")
    if data.empty:
        logging.info(f"No historical data found for ticker: {ticker}")
        raise HTTPException(
            status_code=404, detail="No historical data found for the given ticker"
        )
    data = data.reset_index()
    data = data.rename(columns={'Date': 'ds', 'Close': 'y'})
    data['ds'] = pd.to_datetime(data['ds']).dt.tz_localize(None)

    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=90)

    forecast = model.predict(future)

    predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(90)
    predictions = predictions.rename(
        columns={'ds': 'Date', 'yhat': 'Predicted', 'yhat_lower': 'Lower', 'yhat_upper': 'Upper'}, )

    return predictions.to_dict(orient='records')
