import shioaji as sj

# ==========================================
# ⚙️ 設定區 (只要改這裡，就能切換模式)
# ==========================================
MODE = "SIMULATION"  # 選項: "SIMULATION" (模擬) 或 "REAL" (真倉)
Buy_Stock = "2890"   # 想買的股票
Buy_Price = 1500     # 想買的價格 (模擬用漲停價)
Buy_Qty = 1          # 想買幾張
# ==========================================

print(f"🚀 啟動程式... 目前模式：{MODE}")

# 1. 登入與憑證 (自動判斷模式)
if MODE == "SIMULATION":
    api = sj.Shioaji(simulation=True) 
    print("⚠️ 注意：現在是模擬環境，不會扣錢。")
else:
    api = sj.Shioaji(simulation=False)
    print("🚨 警告：現在是正式環境，下單會真的成交！")

api.login(
    api_key="DFbgCMEgWu33MHoegpLrFm1Je7EZPgu9tmxt9FBUDoPV",        
    secret_key="E38SPi4RQXeEqkcnp3hx66ZeD1Syv5xNKz3ZtJtFGrFb"
)

# 不管是模擬還是正式，都要啟用憑證比較保險
api.activate_ca(
    ca_path="./Sinopac.pfx",
    ca_passwd="A131680155",
    person_id="A131680155"
)

# 2. 執行下單
contract = api.Contracts.Stocks[Buy_Stock]
order = api.Order(
    price=Buy_Price,
    quantity=Buy_Qty,
    action=sj.constant.Action.Buy,
    price_type=sj.constant.StockPriceType.LMT,
    order_type=sj.constant.OrderType.ROD,
    account=api.stock_account
)

# 3. 送出與回報
trade = api.place_order(contract, order)
print(f"✅ {Buy_Stock} 訂單已送出！狀態：{trade.status.status}")

# 4. 順便檢查一下所有委託單
print("------------------------------")
api.update_status()
print("📋 目前帳戶所有委託單：")
for t in api.list_trades():
    print(f"股票：{t.contract.code} | 狀態：{t.status.status}")
print("------------------------------")