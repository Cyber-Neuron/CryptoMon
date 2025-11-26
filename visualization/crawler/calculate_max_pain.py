import json


def calculate_max_pain_and_profit(data):
    # 1) 读取行权价和 OI
    strikes = [float(k) for k in data["data"]["keyList"]]
    call_oi = data["data"]["callOiList"]
    put_oi = data["data"]["putOiList"]

    # 2) 计算每个 S 下的总痛苦值 pain(S)
    pains = []
    for S in strikes:
        pain_S = sum(
            C * max(S - K, 0)  # call 部分做市商要赔的钱
            + P * max(K - S, 0)  # put  部分做市商要赔的钱
            for K, C, P in zip(strikes, call_oi, put_oi)
        )
        pains.append(pain_S)

    # 3) 把 pain 取负作为 PnL
    profits = [-p for p in pains]

    # 4) 找到最大 PnL 对应的行权价
    idx_profit = profits.index(max(profits))
    max_profit = profits[idx_profit]
    max_profit_S = strikes[idx_profit]

    return max_profit_S, max_profit


def calculate_max_pain(data):
    # 1) 读取行权价和 OI
    strikes = [float(k) for k in data["data"]["keyList"]]
    call_oi = data["data"]["callOiList"]
    put_oi = data["data"]["putOiList"]

    # 2) 对每个候选到期价 S，计算总痛苦 pain(S)
    pains = []
    for S in strikes:
        pain_S = 0.0
        for K, C, P in zip(strikes, call_oi, put_oi):
            pain_S += C * max(S - K, 0)  # call 部分
            pain_S += P * max(K - S, 0)  # put 部分
        pains.append(pain_S)

    # 3) 找到使得痛苦最小的行权价
    idx = pains.index(min(pains))
    S_mp = strikes[idx]
    print(f"→ Max Pain Strike: {S_mp}")
    print(f"→ Min Total Pain: {pains[idx]:.2f}")


def pain(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    calculate_max_pain(data)
    S_mp, profit_mp = calculate_max_pain_and_profit(data)
    print(f"→ Max Pain Strike: {S_mp}")
    print(f"→ Market Maker PnL at Max Pain: {profit_mp:.2f}")


if __name__ == "__main__":
    import fire

    fire.Fire(pain)
