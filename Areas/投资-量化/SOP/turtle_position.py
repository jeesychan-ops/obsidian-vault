#!/usr/bin/env python3
"""
海龟交易法则 - ATR 头寸计算器
================================
作者：稳盈君
用途：下单前计算海龟头寸单位（Unit）、止损位、加仓点、离场信号
公式来源：海龟交易法则（Richard Dennis, 1983）

用法：
  python3 turtle_position.py 688110           # 单只股票
  python3 turtle_position.py 688110 84400     # 单只 + 自定义账户金额
  python3 turtle_position.py --holdings       # 诊断当前持仓

公式：
  Unit = 账户 × 风险系数% ÷ (ATR × 每点价值)
  2N 止损位 = 现价 - 2 × ATR
  加仓点 = 现价 + 0.5N × N（第N次加仓）
  离场 = 跌破 10/20 日最低
"""

import requests
import argparse
import sys
from typing import Optional, List, Dict

# ============ 配置 ============
DEFAULT_ACCOUNT = 84394       # 老板当前账户
DEFAULT_RISK_PCT = 1.0        # 单笔风险 1%
MAX_UNITS = 4                # 单一市场上限
ATR_PERIOD = 20              # ATR 周期


# ============ 工具函数 ============
def get_kline(code: str, market: str = 'sh', days: int = 60) -> Optional[List]:
    """腾讯 K 线接口（防限流）"""
    secid = f"{market}{code}"
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={secid},day,,,{days},qfq"
    headers = {"User-Agent": "Mozilla/5.0"}
    for attempt in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=15)
            data = r.json()
            if data.get('code') == 0:
                inner = data.get('data', {}).get(secid, {})
                if 'qfqday' in inner:
                    return inner['qfqday']
        except Exception:
            pass
    return None


def calc_atr(klines: List, period: int = 20) -> Optional[float]:
    """ATR(N) = 过去 N 根 K 线 (最高-最低) 均值"""
    if not klines or len(klines) < period:
        return None
    trs = []
    for k in klines[-period:]:
        h, l = float(k[3]), float(k[4])
        trs.append(h - l)
    return sum(trs) / period


def get_market(code: str) -> str:
    """根据代码判断市场"""
    if code.startswith(('6', '5', '9')):
        return 'sh'
    elif code.startswith(('0', '3', '1', '2')):
        return 'sz'
    return 'sh'


def get_quote(code: str) -> Optional[Dict]:
    """腾讯实时行情"""
    market = get_market(code)
    secid = f"{market}{code}"
    url = f"https://qt.gtimg.cn/q={secid}"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        text = r.text.strip()
        if '"' in text:
            parts = text.split('"')[1].split('~')
            if len(parts) > 40:
                return {
                    'name': parts[1],
                    'code': parts[2],
                    'price': float(parts[3]),
                    'prev_close': float(parts[4]),
                    'open': float(parts[5]),
                    'high': float(parts[33]) if parts[33] else None,
                    'low': float(parts[34]) if parts[34] else None,
                }
    except Exception:
        pass
    return None


# ============ 核心计算 ============
def calc_turtle(code: str, account: float = DEFAULT_ACCOUNT, risk_pct: float = DEFAULT_RISK_PCT,
                shares_held: int = 0, cost: float = 0.0) -> Optional[Dict]:
    """海龟法则全套计算"""
    market = get_market(code)
    quote = get_quote(code)
    klines = get_kline(code, market)
    
    if not quote or not klines:
        print(f"❌ 无法获取 {code} 的数据")
        return None
    
    atr = calc_atr(klines, ATR_PERIOD)
    if not atr:
        print(f"❌ ATR 计算失败")
        return None
    
    price = quote['price']
    risk_amount = account * (risk_pct / 100)
    
    # 头寸 Unit = 账户 × 风险% ÷ (ATR × 1)
    # 股票每点价值 = 1 元（人民币）
    unit = int(risk_amount / atr)
    
    # 4 Unit 满仓
    max_shares = unit * MAX_UNITS
    
    # 2N 止损
    stop_loss = price - 2 * atr
    
    # 加仓点（每 0.5N）
    add_points = [price + 0.5 * atr * i for i in range(1, 4)]
    
    # 离场信号
    lows_20 = [float(k[4]) for k in klines[-20:]]
    lows_10 = lows_20[-10:]
    exit_10d = min(lows_10)
    exit_20d = min(lows_20)
    
    # 当前头寸评估
    units_held = shares_held / unit if unit > 0 else 0
    is_over = units_held > MAX_UNITS
    
    result = {
        'code': code,
        'name': quote['name'],
        'price': price,
        'prev_close': quote['prev_close'],
        'change_pct': (price / quote['prev_close'] - 1) * 100,
        'atr': atr,
        'atr_pct': atr / price * 100,
        'account': account,
        'risk_amount': risk_amount,
        'unit': unit,
        'max_shares': max_shares,
        'shares_held': shares_held,
        'cost': cost,
        'pnl_pct': (price / cost - 1) * 100 if cost else None,
        'units_held': units_held,
        'is_over': is_over,
        'stop_loss': stop_loss,
        'add_points': add_points,
        'exit_10d': exit_10d,
        'exit_20d': exit_20d,
        'over_units': max(0, units_held - MAX_UNITS),
    }
    return result


def print_result(r: Dict):
    """打印分析结果"""
    print("=" * 70)
    print(f"🐢 海龟头寸分析  ·  {r['name']} ({r['code']})")
    print("=" * 70)
    print(f"现价: {r['price']:.2f}  |  昨收: {r['prev_close']:.2f}  |  "
          f"今日: {r['change_pct']:+.2f}%")
    print(f"账户: {r['account']:,.0f} 元  |  单笔风险 {r['risk_amount']:.0f} 元 (1%)")
    print()
    
    # ATR
    print(f"📊 ATR(20) = {r['atr']:.2f} 元 (日波动 {r['atr_pct']:.1f}%)")
    print()
    
    # 头寸
    print(f"📐 海龟 1 Unit = {r['unit']} 股")
    print(f"   满仓 4 Unit = {r['max_shares']} 股 (约 {r['max_shares']*r['price']/r['account']*100:.0f}% 仓位)")
    
    if r['shares_held'] > 0:
        print()
        print(f"💼 当前持仓: {r['shares_held']} 股 = {r['units_held']:.2f} Unit")
        if r['cost']:
            pnl_str = f"  |  浮亏 {r['pnl_pct']:+.2f}%" if r['pnl_pct'] < 0 else f"  |  浮盈 {r['pnl_pct']:+.2f}%"
            print(f"   成本: {r['cost']:.2f}{pnl_str}")
        if r['is_over']:
            reduce_to = r['max_shares']
            reduce_shares = r['shares_held'] - reduce_to
            print(f"   ❌ **超规 {r['units_held']/MAX_UNITS:.1f} 倍**")
            print(f"   🚨 建议减仓 {reduce_shares} 股 → 降至 {reduce_to} 股（4 Unit）")
        elif r['units_held'] > 3:
            print(f"   ⚠️ 接近上限 ({r['units_held']:.2f}/4 Unit)")
        else:
            print(f"   ✅ 头寸合规")
    
    print()
    print("🛡️  风险控制位")
    print(f"   2N 止损位: {r['stop_loss']:.2f} 元")
    print(f"   跌破 10 日最低 ({r['exit_10d']:.2f}) → 全平（系统一）")
    print(f"   跌破 20 日最低 ({r['exit_20d']:.2f}) → 全平（系统二）")
    
    if r['shares_held'] == 0 or r['units_held'] < 4:
        print()
        print("📈 盈利加仓点（每 0.5N 加 1 Unit）")
        for i, p in enumerate(r['add_points'], 1):
            print(f"   第 {i} 次加仓: {p:.2f} 元 (+{i*0.5:.1f}N)")
        print(f"   满仓价: {r['price'] + 1.5 * r['atr']:.2f} 元 (4 Unit)")
    
    print()
    print("💡 速查表")
    print(f"   单笔最大亏损: {r['unit'] * 2 * r['atr']:.0f} 元 (1 Unit × 2N)")
    print(f"   满仓最大亏损: {r['max_shares'] * 2 * r['atr']:.0f} 元 (4 Unit × 2N)")
    print("=" * 70)


# ============ 老板默认持仓 ============
DEFAULT_HOLDINGS = [
    {'code': '688691', 'shares': 400, 'cost': 125.38, 'name': '灿芯股份'},
    {'code': '688726', 'shares': 400, 'cost': 71.77, 'name': '拉普拉斯'},
    {'code': '300323', 'shares': 500, 'cost': 16.53, 'name': '华灿光电'},
]


def main():
    parser = argparse.ArgumentParser(
        description='🐢 海龟头寸计算器 - 下单前先算清楚',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s 688110              # 算灿芯股份（无持仓）
  %(prog)s 688110 --shares 400 --cost 125.38  # 算灿芯（带持仓）
  %(prog)s 688726 84400        # 自定义账户金额
  %(prog)s --holdings          # 老板当前持仓诊断
        """)
    parser.add_argument('code', nargs='?', help='股票代码')
    parser.add_argument('account', nargs='?', type=float, default=DEFAULT_ACCOUNT,
                        help=f'账户金额（默认 {DEFAULT_ACCOUNT}）')
    parser.add_argument('--shares', type=int, default=0, help='当前持仓股数')
    parser.add_argument('--cost', type=float, default=0.0, help='成本价')
    parser.add_argument('--holdings', action='store_true', help='诊断老板默认持仓')
    parser.add_argument('--risk', type=float, default=1.0, help='单笔风险%%（默认 1）')
    
    args = parser.parse_args()
    
    if args.holdings:
        print(f"\n🐢 老板持仓海龟诊断（账户 {DEFAULT_ACCOUNT:,.0f}）\n")
        for h in DEFAULT_HOLDINGS:
            r = calc_turtle(h['code'], DEFAULT_ACCOUNT, args.risk, h['shares'], h['cost'])
            if r:
                print_result(r)
                print()
        return
    
    if not args.code:
        parser.print_help()
        return
    
    r = calc_turtle(args.code, args.account, args.risk, args.shares, args.cost)
    if r:
        print_result(r)


if __name__ == '__main__':
    main()
