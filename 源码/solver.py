# -*- coding: utf-8 -*-
"""
敲击步骤计算器：在固定最后三步的前提下，用最少点击使总结果为 0。
"""

# 图1：8 个操作（第一行左→右，第二行左→右）
OPERATIONS = [
    ("轻击", -3),
    ("击打", -6),
    ("冲压", +2),
    ("弯曲", +7),
    ("重击", -9),
    ("牵拉", -15),
    ("镦锻", +13),
    ("收缩", +16),
]

NAME_TO_VALUE = {name: val for name, val in OPERATIONS}

# 某些“最后步骤”在游戏里其实可以是多个不同力度。
# 例如：你在图2里只能看到“击打”图标，但实际可以是轻击 / 击打 / 重击。
AMBIGUOUS_FINAL_CHOICES = {
    # 当下拉框里选的是“击打”，内部会依次尝试下面三种具体情况，
    # 选出总点击次数（前面平衡步骤 + 最后三步）最少的那个。
    "击打": ["轻击", "击打", "重击"],
}


def min_steps_to_target(target: int) -> tuple[int, list[str]]:
    """
    用 BFS 求从 0 到 target 的最少步数，以及其中一种操作序列。
    每种操作可重复使用。
    返回 (步数, 操作名称列表)，若无法达到则返回 (None, [])。
    """
    if target == 0:
        return 0, []

    # (当前值, 已选操作列表)
    from collections import deque
    q = deque([(0, [])])
    seen = {0}

    while q:
        cur, path = q.popleft()
        for name, val in OPERATIONS:
            nxt = cur + val
            if nxt == target:
                return len(path) + 1, path + [name]
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, path + [name]))

    return -1, []


def _solve_concrete(final_three: list[str]) -> dict:
    """
    处理一组“已经具体确定”的最后三步（不含模糊选择），返回一次完整计算结果。
    """
    if len(final_three) != 3:
        return {"error": "必须选择恰好 3 个最后步骤"}

    values = []
    for name in final_three:
        if name not in NAME_TO_VALUE:
            return {"error": f"未知操作: {name}"}
        values.append(NAME_TO_VALUE[name])

    final_sum = sum(values)
    target = -final_sum  # 前面要点的操作之和需为 target，这样 total = target + final_sum = 0

    steps, balance_path = min_steps_to_target(target)

    # 完整顺序：先平衡步骤，再最后三步反序（与图2对上）
    reverse_final = list(reversed(final_three))
    full_sequence = balance_path + reverse_final

    return {
        "final_three": final_three,
        "final_values": values,
        "final_sum": final_sum,
        "target": target,
        "min_steps": steps,
        "balance_sequence": balance_path,
        "reverse_final": reverse_final,
        "full_sequence": full_sequence,
        "success": steps >= 0,
    }


def solve(final_three: list[str]) -> dict:
    """
    给定最后三步的名称（图2第一行从左到右），计算：
    - 若某一步是“模糊”的（例如：击打 ⇒ 轻击 / 击打 / 重击 都可以），
      会枚举所有组合，选出总点击次数（平衡步骤 + 最后三步）最少的方案。
    - 返回其中一个最优方案的详细结果。
    """
    if len(final_three) != 3:
        return {"error": "必须选择恰好 3 个最后步骤"}

    # 为每个位置准备候选列表，例如：
    #   [\"击打\", \"冲压\", \"牵拉\"]  ⇒  [[轻,中,重], [冲压], [牵拉]]
    from itertools import product

    candidates_per_pos: list[list[str]] = []
    for name in final_three:
        if name in AMBIGUOUS_FINAL_CHOICES:
            candidates_per_pos.append(AMBIGUOUS_FINAL_CHOICES[name])
        else:
            candidates_per_pos.append([name])

    # 如果没有任何模糊选择，直接按原逻辑算一次即可。
    if all(len(cands) == 1 for cands in candidates_per_pos):
        return _solve_concrete(final_three)

    best_result: dict | None = None
    best_total_steps: int | None = None

    for combo in product(*candidates_per_pos):
        concrete_three = list(combo)
        cur = _solve_concrete(concrete_three)
        if not cur.get("success", False):
            continue
        # 总点击次数 = 平衡步骤数量 + 最后三步数量（固定为 3）
        total_steps = len(cur["balance_sequence"]) + len(concrete_three)
        if best_result is None or total_steps < best_total_steps:  # type: ignore[arg-type]
            best_result = cur
            best_total_steps = total_steps

    if best_result is None:
        # 所有组合都无法凑出目标值，至少返回第一个组合的结果（用于提示 target 等信息）。
        first_combo = [cands[0] for cands in candidates_per_pos]
        res = _solve_concrete(first_combo)
        res["original_final_three"] = final_three
        return res

    # 记录原始选择（可能包含“击打”这种模糊写法），方便将来需要区分时查看。
    best_result["original_final_three"] = final_three
    best_result["total_steps"] = best_total_steps
    return best_result


if __name__ == "__main__":
    # 示例：图2 最后三步为 冲压、弯曲、牵拉
    r = solve(["冲压", "弯曲", "牵拉"])
    if "error" in r:
        print(r["error"])
    else:
        print("最后三步:", r["final_three"], "→ 数值", r["final_values"], "→ 和", r["final_sum"])
        print("需要抵消的值（前面点的和）:", r["target"])
        print("最少步数:", r["min_steps"])
        print("平衡步骤序列:", r["balance_sequence"])
        print("最后三步反序（与图对上）:", r["reverse_final"])
        print("完整点击顺序:", r["full_sequence"])
