# 附录 A：形态学指标一览

## 零、导入及公共函数

```python
import numpy as np
import pandas as pd

def _candle_parts(df):
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]
    body = (c - o).abs()
    upper = h - np.maximum(o, c)
    lower = np.minimum(o, c) - l
    rng = (h - l).replace(0, np.nan)
    return body, upper, lower, rng

def _as_bool(mask):
    return mask.fillna(False).astype(bool)
```

---

## 一、单根 K 线形态

### 1. 锤子线（Hammer）

下跌末端出现，小实体、长下影、短上影，空方打压后被多方拉回。

```python
def hammer(df, metric_col="hammer", in_place=False,
           body_max=0.3, lower_min=0.6, upper_max=0.1, lookback=5):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (lower/rng >= lower_min) &
        (upper/rng <= upper_max) & (df["close"].pct_change(lookback) < 0)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 2. 上吊线（Hanging Man）

形状同锤子线，但出现在上涨末端，长下影在顶部变为承接乏力的看跌信号。

```python
def hanging_man(df, metric_col="hanging_man", in_place=False,
                body_max=0.3, lower_min=0.6, upper_max=0.1, lookback=5):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (lower/rng >= lower_min) &
        (upper/rng <= upper_max) & (df["close"].pct_change(lookback) > 0)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 3. 倒锤子线（Inverted Hammer）

下跌末端出现，小实体、长上影、短下影，多方试探性上攻。

```python
def inverted_hammer(df, metric_col="inverted_hammer", in_place=False,
                    body_max=0.3, upper_min=0.6, lower_max=0.1, lookback=5):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (upper/rng >= upper_min) &
        (lower/rng <= lower_max) & (df["close"].pct_change(lookback) < 0)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 4. 射击之星 / 流星线（Shooting Star）

形状同倒锤子，但出现在上涨末端，冲高回落，看跌反转。

```python
def shooting_star(df, metric_col="shooting_star", in_place=False,
                  body_max=0.3, upper_min=0.6, lower_max=0.1, lookback=5):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (upper/rng >= upper_min) &
        (lower/rng <= lower_max) & (df["close"].pct_change(lookback) > 0)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 5. 十字星（Doji）

开盘与收盘几乎相等，实体极小，多空均衡。

```python
def doji(df, metric_col="doji", in_place=False, body_max=0.1):
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(body / rng <= body_max)
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 6. 蜻蜓十字星（Dragonfly Doji）

十字星且只有长下影、几乎无上影，偏看涨。

```python
def dragonfly_doji(df, metric_col="dragonfly_doji", in_place=False,
                   body_max=0.1, lower_min=0.7, upper_max=0.05):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (lower/rng >= lower_min) & (upper/rng <= upper_max)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 7. 墓碑十字星（Gravestone Doji）

十字星且只有长上影、几乎无下影，偏看跌。

```python
def gravestone_doji(df, metric_col="gravestone_doji", in_place=False,
                    body_max=0.1, upper_min=0.7, lower_max=0.05):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (upper/rng >= upper_min) & (lower/rng <= lower_max)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 8. 长腿十字星 / 黄包车夫线（Long-Legged Doji）

实体极小，上下影线都很长，多空激烈争夺后回到原点。

```python
def long_legged_doji(df, metric_col="long_legged_doji", in_place=False,
                     body_max=0.1, shadow_min=0.3):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (upper/rng >= shadow_min) & (lower/rng >= shadow_min)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 9. 纺锤线（Spinning Top）

小实体、上下影线均较长，多空犹豫，动能减弱。

```python
def spinning_top(df, metric_col="spinning_top", in_place=False,
                 body_max=0.3, shadow_min=0.25):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (upper/rng >= shadow_min) & (lower/rng >= shadow_min)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 10. 光头光脚阳线（Bullish Marubozu）

无上下影线的大阳线，多方完全控盘，看涨持续。

```python
def bullish_marubozu(df, metric_col="bullish_marubozu", in_place=False,
                     body_min=0.9, shadow_max=0.05):
    o, c = df["open"], df["close"]
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (c > o) & (body/rng >= body_min) &
        (upper/rng <= shadow_max) & (lower/rng <= shadow_max)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 11. 光头光脚阴线（Bearish Marubozu）

无上下影线的大阴线，空方完全控盘，看跌持续。

```python
def bearish_marubozu(df, metric_col="bearish_marubozu", in_place=False,
                     body_min=0.9, shadow_max=0.05):
    o, c = df["open"], df["close"]
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (c < o) & (body/rng >= body_min) &
        (upper/rng <= shadow_max) & (lower/rng <= shadow_max)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 12. 收盘光头光脚（Closing Marubozu）

收盘价等于最高或最低，一端无影线；方向取决于哪一端收盘。

```python
def closing_marubozu(df, metric_col="closing_marubozu", in_place=False,
                     body_min=0.7):
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng >= body_min) &
        (((c == h) & (l < o)) | ((c == l) & (h > o)))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 13. 开盘光头光脚（Opening Marubozu）

开盘价等于最高或最低，一端无影线；方向取决于哪一端开盘。

```python
def opening_marubozu(df, metric_col="opening_marubozu", in_place=False,
                     body_min=0.7):
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng >= body_min) &
        (((o == l) & (c > o)) | ((o == h) & (c < o)))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 14. 看涨捉腰带线（Bullish Belt Hold）

大阳线，开盘即最低，无下影，下跌末端出现为看涨反转。

```python
def bullish_belt_hold(df, metric_col="belt_bull", in_place=False,
                      body_min=0.6, lower_max=0.05, lookback=5):
    o, c = df["open"], df["close"]
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (c > o) & (body/rng >= body_min) & (lower/rng <= lower_max) &
        (df["close"].pct_change(lookback) < 0)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 15. 看跌捉腰带线（Bearish Belt Hold）

大阴线，开盘即最高，无上影，上涨末端出现为看跌反转。

```python
def bearish_belt_hold(df, metric_col="belt_bear", in_place=False,
                      body_min=0.6, upper_max=0.05, lookback=5):
    o, c = df["open"], df["close"]
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (c < o) & (body/rng >= body_min) & (upper/rng <= upper_max) &
        (df["close"].pct_change(lookback) > 0)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 16. 高浪线（High-Wave Candle）

实体小、上下影线都很长，但实体比长腿十字星稍大，激烈争夺。

```python
def high_wave(df, metric_col="high_wave", in_place=False,
              body_max=0.3, shadow_min=0.3):
    body, upper, lower, rng = _candle_parts(df)
    mask = _as_bool(
        (body/rng <= body_max) & (upper/rng >= shadow_min) & (lower/rng >= shadow_min)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

---

## 二、双根 K 线形态

### 17. 看涨吞没（Bullish Engulfing）

前阴后阳，阳线实体完全吞没前阴实体。

```python
def bullish_engulfing(df, metric_col="bull_engulf", in_place=False):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (c > o) &
        (o <= c.shift(1)) & (c >= o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 18. 看跌吞没（Bearish Engulfing）

前阳后阴，阴线实体完全吞没前阳实体。

```python
def bearish_engulfing(df, metric_col="bear_engulf", in_place=False):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) > o.shift(1)) & (c < o) &
        (o >= c.shift(1)) & (c <= o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 19. 看涨孕线（Bullish Harami）

前长阴，后小阳且完全被前实体包含。

```python
def bullish_harami(df, metric_col="bull_harami", in_place=False,
                   long_min=0.5, small_max=0.3):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min) &
        (c > o) & (body/rng <= small_max) &
        (o >= c.shift(1)) & (c <= o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 20. 看跌孕线（Bearish Harami）

前长阳，后小阴且完全被前实体包含。

```python
def bearish_harami(df, metric_col="bear_harami", in_place=False,
                   long_min=0.5, small_max=0.3):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(1) > o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min) &
        (c < o) & (body/rng <= small_max) &
        (o <= c.shift(1)) & (c >= o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 21. 看涨十字孕线（Bullish Harami Cross）

孕线中第二根为十字星，反转信号更强。

```python
def bull_harami_cross(df, metric_col="bull_harami_cross", in_place=False,
                      long_min=0.5, doji_max=0.1):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min) &
        (body/rng <= doji_max) &
        (o >= c.shift(1)) & (c <= o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 22. 看跌十字孕线（Bearish Harami Cross）

看跌孕线中第二根为十字星。

```python
def bear_harami_cross(df, metric_col="bear_harami_cross", in_place=False,
                      long_min=0.5, doji_max=0.1):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(1) > o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min) &
        (body/rng <= doji_max) &
        (o <= c.shift(1)) & (c >= o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 23. 刺透线 / 穿刺线（Piercing Line）

前阴后阳，今开低于前收，今收深入前阴实体上半部。

```python
def piercing_line(df, metric_col="piercing", in_place=False):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (c > o) & (o < c.shift(1)) &
        (c > (o.shift(1) + c.shift(1)) / 2) & (c < o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 24. 乌云盖顶（Dark Cloud Cover）

前阳后阴，今开高于前收，今收深入前阳实体下半部。

```python
def dark_cloud_cover(df, metric_col="dark_cloud", in_place=False):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) > o.shift(1)) & (c < o) & (o > c.shift(1)) &
        (c < (o.shift(1) + c.shift(1)) / 2) & (c > o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 25. 镊子底 / 平底（Tweezer Bottom）

两根 K 线最低价几乎相同，形成水平支撑。

```python
def tweezer_bottom(df, metric_col="tweezer_bottom", in_place=False, tol=0.002):
    l = df["low"]
    mask = _as_bool(np.abs(l - l.shift(1)) / l <= tol)
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 26. 镊子顶 / 平顶（Tweezer Top）

两根 K 线最高价几乎相同，形成水平阻力。

```python
def tweezer_top(df, metric_col="tweezer_top", in_place=False, tol=0.002):
    h = df["high"]
    mask = _as_bool(np.abs(h - h.shift(1)) / h <= tol)
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 27. 看涨反击线（Bullish Counterattack / Meeting Lines）

前阴后阳，两根收盘价几乎相同。

```python
def bull_counterattack(df, metric_col="bull_counterattack", in_place=False, tol=0.002):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (c > o) &
        (np.abs(c - c.shift(1)) / c.shift(1) <= tol)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 28. 看跌反击线（Bearish Counterattack）

前阳后阴，两根收盘价几乎相同。

```python
def bear_counterattack(df, metric_col="bear_counterattack", in_place=False, tol=0.002):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) > o.shift(1)) & (c < o) &
        (np.abs(c - c.shift(1)) / c.shift(1) <= tol)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 29. 看涨分手线（Bullish Separating Lines）

两根开盘价相同，第二根为阳线且顺原趋势。

```python
def bull_separating(df, metric_col="bull_separating", in_place=False, tol=0.002):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (np.abs(o - o.shift(1)) / o.shift(1) <= tol) &
        (c.shift(1) < o.shift(1)) & (c > o)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 30. 看跌分手线（Bearish Separating Lines）

两根开盘价相同，第二根为阴线且顺原趋势。

```python
def bear_separating(df, metric_col="bear_separating", in_place=False, tol=0.002):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (np.abs(o - o.shift(1)) / o.shift(1) <= tol) &
        (c.shift(1) > o.shift(1)) & (c < o)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 31. 颈内线（In-Neck）

前长阴，后小阳，阳线收盘仅略高于前阴收盘，弱势反弹。

```python
def in_neck(df, metric_col="in_neck", in_place=False,
            long_min=0.5, small_max=0.3, tol=0.005):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min) &
        (c > o) & (body/rng <= small_max) &
        (c > c.shift(1)) & (c <= c.shift(1) * (1 + tol))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 32. 颈上线 / 入颈线（On-Neck）

前长阴，后小阳，阳线收盘与前阴收盘基本相同。

```python
def on_neck(df, metric_col="on_neck", in_place=False,
            long_min=0.5, small_max=0.3, tol=0.002):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min) &
        (c > o) & (body/rng <= small_max) &
        (np.abs(c - c.shift(1)) / c.shift(1) <= tol)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 33. 刺入线 / 插入线（Thrusting）

前阴后阳，阳线收盘进入前阴实体但未过半，力度弱于刺透线。

```python
def thrusting(df, metric_col="thrusting", in_place=False):
    o, c = df["open"], df["close"]
    mid_prev = (o.shift(1) + c.shift(1)) / 2
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (c > o) & (o < c.shift(1)) &
        (c > c.shift(1)) & (c < mid_prev)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 34. 相同低价（Matching Low）

两根阴线收盘价几乎相同，下跌后可能形成支撑。

```python
def matching_low(df, metric_col="matching_low", in_place=False, tol=0.002):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (c < o) &
        (np.abs(c - c.shift(1)) / c.shift(1) <= tol)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 35. 好友反攻（Homing Pigeon）

前长阴，后小阴且被前实体完全包含。

```python
def homing_pigeon(df, metric_col="homing_pigeon", in_place=False, long_min=0.5):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min) &
        (c < o) & (o >= c.shift(1)) & (c <= o.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 36. 反冲 / 跳空并列（Kicking）

两根光头光脚 K 线之间有跳空缺口，趋势强烈。

```python
def kicking(df, metric_col=("kicking_bull", "kicking_bear"), in_place=False):
    bull_col, bear_col = metric_col
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]
    body, upper, lower, rng = _candle_parts(df)
    marubozu = _as_bool((upper/rng <= 0.05) & (lower/rng <= 0.05))

    bull = marubozu & marubozu.shift(1) & (c.shift(1) < o.shift(1)) & (c > o) & (l > h.shift(1))
    bear = marubozu & marubozu.shift(1) & (c.shift(1) > o.shift(1)) & (c < o) & (h < l.shift(1))

    if not in_place: df = df.copy()
    df[bull_col] = _as_bool(bull)
    df[bear_col] = _as_bool(bear)
    return df
```

### 37. 跳空并列阳线（上跳 / 下跳 Side-by-Side White Lines）

跳空后两根开盘价接近的阳线，缺口方向决定持续方向。

```python
def side_by_side_white(df, metric_col=("sbw_up", "sbw_down"), in_place=False,
                        tol=0.005):
    up_col, down_col = metric_col
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]

    up = _as_bool(
        (c.shift(1) > o.shift(1)) & (c > o) &
        (l.shift(1) > h.shift(2)) &
        (np.abs(o - o.shift(1)) / o.shift(1) <= tol)
    )
    down = _as_bool(
        (c.shift(1) > o.shift(1)) & (c > o) &
        (h.shift(1) < l.shift(2)) &
        (np.abs(o - o.shift(1)) / o.shift(1) <= tol)
    )

    if not in_place: df = df.copy()
    df[up_col] = up
    df[down_col] = down
    return df
```

### 38. 脱离形态（Breakaway, Bullish / Bearish）

五根反转：长 K 线 → 跳空 → 延续 → 反向长 K 线回补缺口。

```python
def breakaway(df, metric_col=("breakaway_bull", "breakaway_bear"), in_place=False):
    bull_col, bear_col = metric_col
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]
    body, _, _, rng = _candle_parts(df)

    bull = _as_bool(
        (c.shift(4) < o.shift(4)) & (body.shift(4)/rng.shift(4) >= 0.5) &
        (h.shift(3) < l.shift(4)) &
        (c.shift(2) < o.shift(2)) & (c.shift(1) < o.shift(1)) &
        (c > o) & (body/rng >= 0.5) & (c > h.shift(3))
    )
    bear = _as_bool(
        (c.shift(4) > o.shift(4)) & (body.shift(4)/rng.shift(4) >= 0.5) &
        (l.shift(3) > h.shift(4)) &
        (c.shift(2) > o.shift(2)) & (c.shift(1) > o.shift(1)) &
        (c < o) & (body/rng >= 0.5) & (c < l.shift(3))
    )

    if not in_place: df = df.copy()
    df[bull_col] = bull
    df[bear_col] = bear
    return df
```

### 39. 切入线（Hikkake, Bullish / Bearish）

内包线后出现假突破陷阱：向下假突破为看涨，向上假突破为看跌。

```python
def hikkake(df, metric_col=("hikkake_bull", "hikkake_bear"), in_place=False):
    bull_col, bear_col = metric_col
    h, l = df["high"], df["low"]

    inside = (h.shift(1) <= h.shift(2)) & (l.shift(1) >= l.shift(2))

    # 看涨：内包线后向下假突破，然后收回
    bull_setup = inside & (l < l.shift(1)) & (df["close"] > l.shift(1))
    # 看跌：内包线后向上假突破，然后收回
    bear_setup = inside & (h > h.shift(1)) & (df["close"] < h.shift(1))

    if not in_place: df = df.copy()
    df[bull_col] = _as_bool(bull_setup)
    df[bear_col] = _as_bool(bear_setup)
    return df
```

### 40. 修正切入线（Hikkake Modified）

四根组合：两根连续收窄的内包线后突破，第二根收盘靠近区间一端。此处提供简化版：内包线后假突破且收盘方向确认。

```python
def hikkake_modified(df, metric_col=("hikkake_mod_bull", "hikkake_mod_bear"),
                     in_place=False):
    bull_col, bear_col = metric_col
    h, l = df["high"], df["low"]

    inside2 = (h.shift(2) <= h.shift(3)) & (l.shift(2) >= l.shift(3))
    inside1 = (h.shift(1) <= h.shift(2)) & (l.shift(1) >= l.shift(2))

    # 看涨修正：连续内包后向下假突破，且收盘收回
    bull = inside2 & inside1 & (l < l.shift(1)) & (df["close"] > l.shift(1))
    # 看跌修正：连续内包后向上假突破，且收盘收回
    bear = inside2 & inside1 & (h > h.shift(1)) & (df["close"] < h.shift(1))

    if not in_place: df = df.copy()
    df[bull_col] = _as_bool(bull)
    df[bear_col] = _as_bool(bear)
    return df
```

### 41. 双鸦（Two Crows / Upside-Gap Two Crows）

两根阴线，第二根跳空高开但收低，顶部看跌反转。

```python
def two_crows(df, metric_col="two_crows", in_place=False):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(1) < o.shift(1)) & (c < o) &
        (o > c.shift(1)) & (c < c.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 42. 前方受阻 / 阻挡形态（Advance Block）

连续三根阳线，实体逐根缩短、上影线拉长，上涨动能衰竭。

```python
def advance_block(df, metric_col="advance_block", in_place=False):
    o, c = df["open"], df["close"]
    body, upper, _, rng = _candle_parts(df)

    all_bull    = (c > o) & (c.shift(1) > o.shift(1)) & (c.shift(2) > o.shift(2))
    body_shrink = (body < body.shift(1)) & (body.shift(1) < body.shift(2))
    upper_grow  = (upper > upper.shift(1)) | (upper / rng > 0.4)

    mask = _as_bool(all_bull & body_shrink & upper_grow)
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

---

## 三、三根 K 线形态

### 43. 早晨之星 / 晨星（Morning Star）

长阴 + 小实体 + 长阳，底部反转。

```python
def morning_star(df, metric_col="morning_star", in_place=False,
                 long_min=0.5, small_max=0.3):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(2) < o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        (body.shift(1)/rng.shift(1) <= small_max) &
        (c > o) & (body/rng >= long_min) &
        (c > (o.shift(2) + c.shift(2)) / 2)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 44. 早晨十字星（Morning Doji Star）

晨星中间为十字星，反转信号更强。

```python
def morning_doji_star(df, metric_col="morning_doji_star", in_place=False,
                      long_min=0.5, doji_max=0.1):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(2) < o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        (body.shift(1)/rng.shift(1) <= doji_max) &
        (c > o) & (body/rng >= long_min) &
        (c > (o.shift(2) + c.shift(2)) / 2)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 45. 黄昏之星 / 暮星（Evening Star）

长阳 + 小实体 + 长阴，顶部反转。

```python
def evening_star(df, metric_col="evening_star", in_place=False,
                 long_min=0.5, small_max=0.3):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(2) > o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        (body.shift(1)/rng.shift(1) <= small_max) &
        (c < o) & (body/rng >= long_min) &
        (c < (o.shift(2) + c.shift(2)) / 2)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 46. 黄昏十字星（Evening Doji Star）

黄昏星中间为十字星。

```python
def evening_doji_star(df, metric_col="evening_doji_star", in_place=False,
                      long_min=0.5, doji_max=0.1):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(2) > o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        (body.shift(1)/rng.shift(1) <= doji_max) &
        (c < o) & (body/rng >= long_min) &
        (c < (o.shift(2) + c.shift(2)) / 2)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 47. 三白兵 / 红三兵（Three White Soldiers）

连续三根大阳线，收盘逐根抬高，每根开盘在前一根实体内。

```python
def three_white_soldiers(df, metric_col="three_white_soldiers", in_place=False,
                          body_min=0.5):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(2) > o.shift(2)) & (c.shift(1) > o.shift(1)) & (c > o) &
        (body.shift(2)/rng.shift(2) >= body_min) &
        (body.shift(1)/rng.shift(1) >= body_min) &
        (body/rng >= body_min) &
        (c.shift(1) > c.shift(2)) & (c > c.shift(1)) &
        (o.shift(1) >= o.shift(2)) & (o.shift(1) <= c.shift(2)) &
        (o >= o.shift(1)) & (o <= c.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 48. 三黑鸦 / 黑三鸦（Three Black Crows）

三白兵镜像，连续三根大阴线，收盘逐根走低。

```python
def three_black_crows(df, metric_col="three_black_crows", in_place=False,
                       body_min=0.5):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(2) < o.shift(2)) & (c.shift(1) < o.shift(1)) & (c < o) &
        (body.shift(2)/rng.shift(2) >= body_min) &
        (body.shift(1)/rng.shift(1) >= body_min) &
        (body/rng >= body_min) &
        (c.shift(1) < c.shift(2)) & (c < c.shift(1)) &
        (o.shift(1) <= o.shift(2)) & (o.shift(1) >= c.shift(2)) &
        (o <= o.shift(1)) & (o >= c.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 49. 相同三鸦（Identical Three Crows）

三根阴线，每根开盘价等于前一根收盘价。

```python
def identical_three_crows(df, metric_col="identical_3crows", in_place=False,
                           tol=0.002):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(2) < o.shift(2)) & (c.shift(1) < o.shift(1)) & (c < o) &
        (np.abs(o.shift(1) - c.shift(2)) / c.shift(2) <= tol) &
        (np.abs(o - c.shift(1)) / c.shift(1) <= tol)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 50. 三内部上涨 / 下跌（Three Inside Up / Down）

孕线 + 第三根同向确认。

```python
def three_inside(df, metric_col=("three_inside_up", "three_inside_down"),
                 in_place=False, long_min=0.5, small_max=0.3):
    up_col, down_col = metric_col
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)

    harami_bull = _as_bool(
        (c.shift(2) < o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        (body.shift(1)/rng.shift(1) <= small_max) &
        (o.shift(1) >= c.shift(2)) & (c.shift(1) <= o.shift(2))
    )
    harami_bear = _as_bool(
        (c.shift(2) > o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        (body.shift(1)/rng.shift(1) <= small_max) &
        (o.shift(1) <= c.shift(2)) & (c.shift(1) >= o.shift(2))
    )

    up = harami_bull & (c > o) & (c > c.shift(1))
    down = harami_bear & (c < o) & (c < c.shift(1))

    if not in_place: df = df.copy()
    df[up_col] = _as_bool(up)
    df[down_col] = _as_bool(down)
    return df
```

### 51. 三外部上涨 / 下跌（Three Outside Up / Down）

吞没 + 第三根同向确认。

```python
def three_outside(df, metric_col=("three_outside_up", "three_outside_down"),
                  in_place=False):
    up_col, down_col = metric_col
    o, c = df["open"], df["close"]

    bull_engulf = _as_bool(
        (c.shift(2) < o.shift(2)) & (c.shift(1) > o.shift(1)) &
        (o.shift(1) <= c.shift(2)) & (c.shift(1) >= o.shift(2))
    )
    bear_engulf = _as_bool(
        (c.shift(2) > o.shift(2)) & (c.shift(1) < o.shift(1)) &
        (o.shift(1) >= c.shift(2)) & (c.shift(1) <= o.shift(2))
    )

    up = bull_engulf & (c > o) & (c > c.shift(1))
    down = bear_engulf & (c < o) & (c < c.shift(1))

    if not in_place: df = df.copy()
    df[up_col] = _as_bool(up)
    df[down_col] = _as_bool(down)
    return df
```

### 52. 弃婴底 / 弃婴顶（Abandoned Baby, Bullish / Bearish）

十字星前后均有跳空，底部看涨、顶部看跌，属于强烈反转。

```python
def abandoned_baby(df, metric_col=("ab_bull", "ab_bear"), in_place=False,
                   long_min=0.5, doji_max=0.1):
    bull_col, bear_col = metric_col
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]
    body, _, _, rng = _candle_parts(df)

    mid_doji = _as_bool(body.shift(1) / rng.shift(1) <= doji_max)

    bull = _as_bool(
        (c.shift(2) < o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        mid_doji & (h.shift(1) < l.shift(2)) &
        (c > o) & (body/rng >= long_min) & (l > h.shift(1))
    )
    bear = _as_bool(
        (c.shift(2) > o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        mid_doji & (l.shift(1) > h.shift(2)) &
        (c < o) & (body/rng >= long_min) & (h < l.shift(1))
    )

    if not in_place: df = df.copy()
    df[bull_col] = bull
    df[bear_col] = bear
    return df
```

### 53. 三星底 / 三星顶（Tri-Star Bottom / Top）

连续三根十字星，底部出现为看涨，顶部出现为看跌。方向通过前置趋势 `pct_change` 判断。

```python
def tri_star(df, metric_col=("tri_star_bull", "tri_star_bear"), in_place=False,
             doji_max=0.1, lookback=5):
    bull_col, bear_col = metric_col
    body, _, _, rng = _candle_parts(df)

    three_doji = _as_bool(
        (body.shift(2)/rng.shift(2) <= doji_max) &
        (body.shift(1)/rng.shift(1) <= doji_max) &
        (body/rng <= doji_max)
    )
    trend = df["close"].pct_change(lookback)

    if not in_place: df = df.copy()
    df[bull_col] = _as_bool(three_doji & (trend < 0))
    df[bear_col] = _as_bool(three_doji & (trend > 0))
    return df
```

### 54. 十字星线（Doji Star, Bullish / Bearish）

大 K 线后接十字星，底部看涨、顶部看跌。

```python
def doji_star(df, metric_col=("doji_star_bull", "doji_star_bear"), in_place=False,
              long_min=0.5, doji_max=0.1):
    bull_col, bear_col = metric_col
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)

    prev_long_bear = _as_bool((c.shift(1) < o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min))
    prev_long_bull = _as_bool((c.shift(1) > o.shift(1)) & (body.shift(1)/rng.shift(1) >= long_min))
    curr_doji      = _as_bool(body / rng <= doji_max)

    if not in_place: df = df.copy()
    df[bull_col] = prev_long_bear & curr_doji
    df[bear_col] = prev_long_bull & curr_doji
    return df
```

### 55. 三线打击（Three Line Strike, Bullish / Bearish）

三根同向 K 线后，第四根反向长 K 线贯穿前三根；经典读作持续形态。

```python
def three_line_strike(df, metric_col=("tls_bull", "tls_bear"), in_place=False):
    bull_col, bear_col = metric_col
    o, c = df["open"], df["close"]

    bull = _as_bool(
        (c.shift(3) < o.shift(3)) & (c.shift(2) < o.shift(2)) & (c.shift(1) < o.shift(1)) &
        (c > o) & (c > o.shift(3)) & (o < c.shift(1))
    )
    bear = _as_bool(
        (c.shift(3) > o.shift(3)) & (c.shift(2) > o.shift(2)) & (c.shift(1) > o.shift(1)) &
        (c < o) & (c < o.shift(3)) & (o > c.shift(1))
    )

    if not in_place: df = df.copy()
    df[bull_col] = bull
    df[bear_col] = bear
    return df
```

### 56. 南方三星（Three Stars in the South）

三根逐渐缩短的阴线，下跌末端看涨反转。

```python
def three_stars_south(df, metric_col="three_stars_south", in_place=False):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)
    mask = _as_bool(
        (c.shift(2) < o.shift(2)) & (c.shift(1) < o.shift(1)) & (c < o) &
        (body.shift(1) < body.shift(2)) & (body < body.shift(1)) &
        (rng.shift(1) < rng.shift(2)) & (rng < rng.shift(1))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 57. 梯底（Ladder Bottom）

连续阴线后出现一根阳线，底部反转。

```python
def ladder_bottom(df, metric_col="ladder_bottom", in_place=False):
    o, c = df["open"], df["close"]
    bear_streak = (c < o) & (c.shift(1) < o.shift(1)) & (c.shift(2) < o.shift(2)) & (c.shift(3) < o.shift(3))
    mask = _as_bool(bear_streak.shift(1) & (c > o))
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 58. 藏婴吞没 / Concealing Baby Swallow

四根阴线：前两根长阴（第二根吞没第一根），后两根小阴被第二根包裹。

```python
def concealing_baby_swallow(df, metric_col="cbs", in_place=False, long_min=0.5):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)

    mask = _as_bool(
        (c.shift(3) < o.shift(3)) & (body.shift(3)/rng.shift(3) >= long_min) &
        (c.shift(2) < o.shift(2)) & (body.shift(2)/rng.shift(2) >= long_min) &
        (o.shift(2) >= o.shift(3)) & (c.shift(2) <= c.shift(3)) &
        (c.shift(1) < o.shift(1)) & (o.shift(1) >= c.shift(2)) & (c.shift(1) <= o.shift(2)) &
        (c < o) & (o >= c.shift(2)) & (c <= o.shift(2))
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 59. 挤压警报 / Mat Hold（Squeeze Alert）

长阳后 2~3 根小实体被包裹在其实体内，随后长阳突破，看涨持续。

```python
def mat_hold(df, metric_col="mat_hold", in_place=False, long_min=0.5, small_max=0.3):
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)

    first_bull = _as_bool((c.shift(3) > o.shift(3)) & (body.shift(3)/rng.shift(3) >= long_min))
    mid_small = _as_bool(
        (body.shift(2)/rng.shift(2) <= small_max) &
        (body.shift(1)/rng.shift(1) <= small_max) &
        (body/rng <= small_max) &
        (np.minimum(o.shift(2), c.shift(2)) >= o.shift(3)) &
        (np.maximum(o.shift(2), c.shift(2)) <= c.shift(3)) &
        (np.minimum(o.shift(1), c.shift(1)) >= o.shift(3)) &
        (np.maximum(o.shift(1), c.shift(1)) <= c.shift(3)) &
        (np.minimum(o, c) >= o.shift(3)) & (np.maximum(o, c) <= c.shift(3))
    )
    breakout = _as_bool((c > o) & (c > c.shift(3)))

    mask = first_bull & mid_small & breakout
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

---

## 四、多根 K 线及特殊组合形态

### 60. 上升三法 / 下降三法（Rising / Falling Three Methods）

长 K 线 + 3 根收敛小实体（落在第一根实体内） + 长 K 线突破。

```python
def three_methods(df, metric_col=("rising_3m", "falling_3m"), in_place=False,
                  long_min=0.5, small_max=0.3):
    rise_col, fall_col = metric_col
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)

    o1, c1, b1, r1 = o.shift(4), c.shift(4), body.shift(4), rng.shift(4)
    o2, c2, b2, r2 = o.shift(3), c.shift(3), body.shift(3), rng.shift(3)
    o3, c3, b3, r3 = o.shift(2), c.shift(2), body.shift(2), rng.shift(2)
    o4, c4, b4, r4 = o.shift(1), c.shift(1), body.shift(1), rng.shift(1)
    o5, c5, b5, r5 = o, c, body, rng

    rise = _as_bool(
        (c1 > o1) & (b1/r1 >= long_min) &
        (b2/r2 <= small_max) & (np.minimum(o2,c2) >= o1) & (np.maximum(o2,c2) <= c1) &
        (b3/r3 <= small_max) & (np.minimum(o3,c3) >= o1) & (np.maximum(o3,c3) <= c1) &
        (b4/r4 <= small_max) & (np.minimum(o4,c4) >= o1) & (np.maximum(o4,c4) <= c1) &
        (c5 > o5) & (b5/r5 >= long_min) & (c5 > c1)
    )
    fall = _as_bool(
        (c1 < o1) & (b1/r1 >= long_min) &
        (b2/r2 <= small_max) & (np.minimum(o2,c2) >= c1) & (np.maximum(o2,c2) <= o1) &
        (b3/r3 <= small_max) & (np.minimum(o3,c3) >= c1) & (np.maximum(o3,c3) <= o1) &
        (b4/r4 <= small_max) & (np.minimum(o4,c4) >= c1) & (np.maximum(o4,c4) <= o1) &
        (c5 < o5) & (b5/r5 >= long_min) & (c5 < c1)
    )

    if not in_place: df = df.copy()
    df[rise_col] = rise
    df[fall_col] = fall
    return df
```

### 61. 跳空缺口三法 / Tasuki Gap（Upside / Downside）

三根：跳空 K 线 + 反向 K 线收回缺口但未完全回补，属持续形态。

```python
def tasuki_gap(df, metric_col=("tasuki_up", "tasuki_down"), in_place=False):
    up_col, down_col = metric_col
    o, c, h, l = df["open"], df["close"], df["high"], df["low"]

    up = _as_bool(
        (c.shift(2) > o.shift(2)) & (l.shift(1) > h.shift(2)) &
        (c.shift(1) < o.shift(1)) & (c < o) & (c > o.shift(2))
    )
    down = _as_bool(
        (c.shift(2) < o.shift(2)) & (h.shift(1) < l.shift(2)) &
        (c.shift(1) > o.shift(1)) & (c > o) & (c < o.shift(2))
    )

    if not in_place: df = df.copy()
    df[up_col] = up
    df[down_col] = down
    return df
```

### 62. 夹心形态 / 三明治（Stick Sandwich）

两根同向 K 线（通常阴线）夹一根反向 K 线，两根同向 K 线收盘价接近。

```python
def stick_sandwich(df, metric_col="stick_sandwich", in_place=False, tol=0.005):
    o, c = df["open"], df["close"]
    mask = _as_bool(
        (c.shift(2) < o.shift(2)) & (c.shift(1) > o.shift(1)) & (c < o) &
        (np.abs(c - c.shift(2)) / c.shift(2) <= tol)
    )
    if not in_place: df = df.copy()
    df[metric_col] = mask
    return df
```

### 63. 塔底 / 塔顶（Tower Bottom / Top）

长 K 线 + 小实体盘整 + 反向长 K 线，属多根反转组合。此处以“长阴 → 至少 2 根小实体 → 长阳”为塔底，镜像为塔顶。

```python
def tower_bottom_top(df, metric_col=("tower_bottom", "tower_top"), in_place=False,
                     long_min=0.5, small_max=0.3, n_small=2):
    bot_col, top_col = metric_col
    o, c = df["open"], df["close"]
    body, _, _, rng = _candle_parts(df)

    first_long_bear = _as_bool((c.shift(3) < o.shift(3)) & (body.shift(3)/rng.shift(3) >= long_min))
    first_long_bull = _as_bool((c.shift(3) > o.shift(3)) & (body.shift(3)/rng.shift(3) >= long_min))

    mid_small = _as_bool(
        (body.shift(2)/rng.shift(2) <= small_max) &
        (body.shift(1)/rng.shift(1) <= small_max)
    )
    last_long_bull = _as_bool((c > o) & (body/rng >= long_min))
    last_long_bear = _as_bool((c < o) & (body/rng >= long_min))

    if not in_place: df = df.copy()
    df[bot_col] = first_long_bear & mid_small & last_long_bull
    df[top_col] = first_long_bull & mid_small & last_long_bear
    return df
```

---

## 五、使用提示

以上函数输出的是**布尔指标列**（`True` 表示形态出现），不直接包含交易方向。实际使用时可以按“看涨形态组合减去看跌形态组合”构造信号：

```python
bull_cols = ["hammer", "bull_engulf", "morning_star", "piercing", "three_white_soldiers"]
bear_cols = ["shooting_star", "bear_engulf", "evening_star", "dark_cloud", "three_black_crows"]

df["form_signal"] = (
    df[bull_cols].astype(int).sum(axis=1)
    - df[bear_cols].astype(int).sum(axis=1)
).clip(-1, 1)

res = compute_cumulative_return(df, signal_col="form_signal", result_col="cum_ret")
```

几点说明：

1. **多方向形态的列名**：`metric_col` 传二元组（如 `("ab_bull", "ab_bear")`），函数内部解包，两列分别写入。
2. **`tol` 参数**：涉及“价格几乎相同”（镊子、反击线、Tasuki 等）的判定，均使用相对容差 `tol`，默认 0.2%~0.5%，可按品种波动率调整。
3. **趋势过滤**：单根反转形态（锤子、上吊、捉腰带、Tri-Star 等）内置了 `lookback` 的 `pct_change` 趋势过滤，避免同一形状在错误位置被误判。
4. **稀有形态**：Breakaway、Concealing Baby Swallow 等在 Bulkowski 统计中出现频率极低（排名 97~103 位），布尔列可能长期为 `False`，属正常现象。
5. **方向语义**：Three Line Strike、Tasuki Gap、Advance Block 等形态的“经典方向”与 Bulkowski 统计结果存在不一致（例如 Three Line Strike 统计上更常表现为反转而非持续），代码只负责**识别形态**，方向解读由策略层决定。