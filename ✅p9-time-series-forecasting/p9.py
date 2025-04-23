import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
from sklearn.metrics import mean_squared_error
from statsmodels.datasets import co2

# Load the CO2 dataset
data = co2.load().data
df = pd.DataFrame(data)

# Data preprocessing
# Convert to datetime and set as index
df['date'] = pd.date_range(start='1958-03-29', periods=len(df), freq='W-SAT')
df.set_index('date', inplace=True)
df.dropna(inplace=True)  # Remove any NaN values

# Plot the original data
plt.figure(figsize=(12, 6))
plt.plot(df['co2'])
plt.title('CO2 Measurements at Mauna Loa')
plt.ylabel('CO2 (ppm)')
plt.xlabel('Date')
plt.grid(True)
plt.tight_layout()
plt.show()

# Data smoothing
df['smoothed_7'] = df['co2'].rolling(window=7).mean()  # 7-week moving average
df['smoothed_52'] = df['co2'].rolling(window=52).mean()  # 52-week moving average

# Plot the smoothed data
plt.figure(figsize=(12, 6))
plt.plot(df['co2'], label='Original', alpha=0.5)
plt.plot(df['smoothed_7'], label='7-Week MA')
plt.plot(df['smoothed_52'], label='52-Week MA', linewidth=2)
plt.title('CO2 Data with Moving Average Smoothing')
plt.ylabel('CO2 (ppm)')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train = df[:train_size].copy()
test = df[train_size:].copy()

print(f"Training data from {train.index[0]} to {train.index[-1]}")
print(f"Testing data from {test.index[0]} to {test.index[-1]}")
print(f"Training set size: {len(train)}")
print(f"Testing set size: {len(test)}")

# METHOD 1: ARIMA Forecasting
# Find best parameters (p,d,q) for ARIMA
# For simplicity, we'll use ARIMA(2,1,2) but you can use auto_arima for parameter selection
print("\nFitting ARIMA model...")
try:
    arima_model = ARIMA(train['co2'], order=(2, 1, 2))
    arima_fit = arima_model.fit()
    print(arima_fit.summary())
    
    # Forecast with ARIMA
    arima_forecast = arima_fit.forecast(steps=len(test))
    
    # Calculate error metrics for ARIMA
    arima_mse = mean_squared_error(test['co2'], arima_forecast)
    arima_rmse = np.sqrt(arima_mse)
    print(f"ARIMA RMSE: {arima_rmse:.4f}")
except Exception as e:
    print(f"Error with ARIMA model: {e}")
    # Fallback to simpler ARIMA model if there's an error
    arima_model = ARIMA(train['co2'], order=(1, 1, 0))
    arima_fit = arima_model.fit()
    arima_forecast = arima_fit.forecast(steps=len(test))
    arima_mse = mean_squared_error(test['co2'], arima_forecast)
    arima_rmse = np.sqrt(arima_mse)
    print(f"Fallback ARIMA RMSE: {arima_rmse:.4f}")

# METHOD 2: Prophet Forecasting
print("\nFitting Prophet model...")
# Prepare data for Prophet (requires 'ds' and 'y' columns)
prophet_train = train.reset_index().rename(columns={'date': 'ds', 'co2': 'y'})
prophet_test = test.reset_index().rename(columns={'date': 'ds', 'co2': 'y'})

# Initialize and fit Prophet model
prophet_model = Prophet(yearly_seasonality=True, weekly_seasonality=False)
prophet_model.fit(prophet_train)

# Create future dataframe for prediction period
future = prophet_model.make_future_dataframe(periods=len(test), freq='W')
prophet_forecast = prophet_model.predict(future)

# Extract forecast for test period
prophet_predictions = prophet_forecast.tail(len(test))

# Calculate error metrics for Prophet
prophet_mse = mean_squared_error(prophet_test['y'], prophet_predictions['yhat'])
prophet_rmse = np.sqrt(prophet_mse)
print(f"Prophet RMSE: {prophet_rmse:.4f}")

# Plot Prophet components
prophet_fig = prophet_model.plot_components(prophet_forecast)
plt.tight_layout()
plt.show()

# METHOD 3: Exponential Smoothing (Holt-Winters)
print("\nFitting Exponential Smoothing model...")
hw_model = ExponentialSmoothing(
    train['co2'], 
    trend='add',
    seasonal='add',
    seasonal_periods=52
)
hw_fit = hw_model.fit(optimized=True)
hw_forecast = hw_fit.forecast(len(test))

# Calculate error metrics for Holt-Winters
hw_mse = mean_squared_error(test['co2'], hw_forecast)
hw_rmse = np.sqrt(hw_mse)
print(f"Holt-Winters RMSE: {hw_rmse:.4f}")

# Compare forecasts visually
plt.figure(figsize=(14, 8))
plt.plot(train.index, train['co2'], label='Training Data', color='black')
plt.plot(test.index, test['co2'], label='Actual Test Data', color='red')
plt.plot(test.index, arima_forecast, label=f'ARIMA Forecast (RMSE: {arima_rmse:.2f})', color='blue')
plt.plot(test.index, prophet_predictions['yhat'], label=f'Prophet Forecast (RMSE: {prophet_rmse:.2f})', color='green')
plt.plot(test.index, hw_forecast, label=f'Holt-Winters Forecast (RMSE: {hw_rmse:.2f})', color='purple')
plt.title('CO2 Time Series Forecast Comparison')
plt.ylabel('CO2 (ppm)')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Table of comparison metrics
print("\nModel Comparison:")
comparison = pd.DataFrame({
    'Model': ['ARIMA', 'Prophet', 'Holt-Winters'],
    'RMSE': [arima_rmse, prophet_rmse, hw_rmse]
})
print(comparison)

# Calculate forecast errors
arima_errors = test['co2'].values - arima_forecast
prophet_errors = test['co2'].values - prophet_predictions['yhat'].values
hw_errors = test['co2'].values - hw_forecast.values

# Plot forecast errors
plt.figure(figsize=(14, 6))
plt.plot(test.index, arima_errors, label='ARIMA Error', alpha=0.7)
plt.plot(test.index, prophet_errors, label='Prophet Error', alpha=0.7)
plt.plot(test.index, hw_errors, label='Holt-Winters Error', alpha=0.7)
plt.axhline(y=0, color='r', linestyle='-')
plt.title('Forecast Errors Comparison')
plt.ylabel('Error (Actual - Forecast)')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Generate future forecasts with the best-performing model
# Determine the best model based on RMSE
rmse_values = [arima_rmse, prophet_rmse, hw_rmse]
best_model_index = np.argmin(rmse_values)
best_models = ['ARIMA', 'Prophet', 'Holt-Winters']
best_model = best_models[best_model_index]
print(f"\nBest performing model: {best_model} with RMSE: {min(rmse_values):.4f}")

# Generate future forecast with the best model (next 52 weeks)
future_periods = 52

if best_model == 'ARIMA':
    # Refit ARIMA on the entire dataset
    full_arima_model = ARIMA(df['co2'], order=(2, 1, 2))
    full_arima_fit = full_arima_model.fit()
    future_forecast = full_arima_fit.forecast(steps=future_periods)
    future_dates = pd.date_range(start=df.index[-1], periods=future_periods+1, freq='W')[1:]
    
elif best_model == 'Prophet':
    # Refit Prophet on the entire dataset
    full_prophet_data = df.reset_index().rename(columns={'date': 'ds', 'co2': 'y'})
    full_prophet_model = Prophet(yearly_seasonality=True, weekly_seasonality=False)
    full_prophet_model.fit(full_prophet_data)
    future = full_prophet_model.make_future_dataframe(periods=future_periods, freq='W')
    future_forecast_df = full_prophet_model.predict(future)
    future_forecast = future_forecast_df.tail(future_periods)['yhat'].values
    future_dates = future_forecast_df.tail(future_periods)['ds'].values
    
else:  # Holt-Winters
    # Refit Holt-Winters on the entire dataset
    full_hw_model = ExponentialSmoothing(
        df['co2'], 
        trend='add',
        seasonal='add',
        seasonal_periods=52
    )
    full_hw_fit = full_hw_model.fit(optimized=True)
    future_forecast = full_hw_fit.forecast(future_periods)
    future_dates = pd.date_range(start=df.index[-1], periods=future_periods+1, freq='W')[1:]

# Plot historical data with future forecast from the best model
plt.figure(figsize=(14, 7))
plt.plot(df.index, df['co2'], label='Historical Data', color='blue')
plt.plot(future_dates, future_forecast, label=f'Future Forecast ({best_model})', color='red', linestyle='--')
plt.title(f'CO2 Levels: Historical Data and Future Forecast using {best_model}')
plt.ylabel('CO2 (ppm)')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()