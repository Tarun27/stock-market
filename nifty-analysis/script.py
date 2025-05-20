import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

end   = datetime(2025, 5, 20)
start = end - timedelta(days=365)

df   = yf.download("^NSEI", start=start, end=end, interval="1d", auto_adjust=False)
col  = "Adj Close" if "Adj Close" in df.columns else "Close"

pct   = df[col].pct_change().mul(100)
drops = pct[pct <= -1].dropna()

# ---------- per-day detail ----------
detail = (
    pd.DataFrame({
        "Date"     : drops.index.date,
        "Month"    : pd.to_datetime(drops.index).to_period("M"),
        "PctDrop%" : drops.values.flatten().round(2)
    })
    .sort_values("Date")
)
detail.to_csv("nifty_drops_detail_1yr.csv", index=False)   # per-day list

# ---------- month summary ----------
summary = (
    detail.groupby("Month")
          .agg(
              Count = ("Date", "size"),
              Dates = ("Date", lambda s: ", ".join(d.strftime("%d-%b") for d in s)),
              Drops = ("PctDrop%", lambda s: ", ".join(f"{d:.2f}%" for d in s))
          )
          .reset_index()
          .loc[:, ["Month", "Count", "Dates", "Drops"]]
)
summary.to_csv("nifty_drops_summary_1yr.csv", index=False) # month-wise roll-up

print("Files written:")
print("  nifty_drops_detail_1yr.csv   # every drop with exact %")
print("  nifty_drops_summary_1yr.csv  # Month | Count | Dates | Drops")
