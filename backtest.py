import shioaji as sj
import pandas as pd
from datetime import datetime, timedelta

# 1. 登入 (抓資料專用)
api = sj.Shioaji()
api.login(
    api_key="DFbgCMEgWu33MHoegpLrFm1Je7EZPgu9tmxt9FBUDoPV",        
    secret_key="E38SPi4RQXeEqkcnp3hx66ZeD1Syv5xNKz3ZtJtFGrFb"
)

# 2. 設定要回測的股票：台積電 (2330)
stock_code = "2330"
print(f"⏳ 正在計算 {stock_code} 過去一年的獲利能力...")

# 3. 抓取一年份資料
kbars = api.kbars(
    contract=api.Contracts.Stocks[stock_code], 
    start=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"), 
    end=datetime.now().strftime("%Y-%m-%d")
)
df = pd.DataFrame({**kbars})
df.ts = pd.to_datetime(df.ts)

# 4. 寫策略 (黃金交叉策略)
# 計算 5日線(短線) 和 20日線(月線)
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()

# 產生訊號：當 MA5 > MA20 時買進 (持有=1)，否則空手 (持有=0)
df['Hold'] = (df['MA5'] > df['MA20']).astype(int)

# 5. 計算獲利
# 今天的漲跌幅 = (今天收盤 - 昨天收盤) / 昨天收盤
df['Return'] = df['Close'].pct_change()
# 你的獲利 = 昨天的持有狀態 * 今天的漲跌幅
df['Strategy_Return'] = df['Hold'].shift(1) * df['Return']

# 累積報酬率 (複利計算)
total_return = (1 + df['Strategy_Return']).cumprod().iloc[-1] - 1

print("----------------------------------")
print(f"📊 回測結果出爐！({stock_code})")
print(f"💰 如果你這一年都用 MA5 > MA20 策略操作...")
print(f"📈 總報酬率：{total_return * 100:.2f}%")
print("----------------------------------")

# 簡單比較：如果你是「買了就不動 (Buy and Hold)」
buy_and_hold_return = (df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1
print(f"🐢 對照組 (買進持有)：{buy_and_hold_return * 100:.2f}%")
print("----------------------------------")