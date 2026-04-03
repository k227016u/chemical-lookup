from flask import Flask, request, jsonify, render_template
import bisect

app = Flask(__name__)

# 化合物データ: {値: 化合物名} の形式で追加・編集してください
# 例として UV 吸収波長 (nm) のデータを入れています
COMPOUNDS = {
    200: "ベンゼン",
    254: "ナフタレン",
    280: "フェニルアラニン",
    310: "アントラセン",
    365: "ピレン",
    410: "クロロフィルb",
    430: "クロロフィルa",
    500: "カロテン",
    550: "ヘモグロビン",
    660: "クロロフィルa（赤帯）",
}

# ソート済みキーリスト（高速検索用）
SORTED_KEYS = sorted(COMPOUNDS.keys())


def find_closest(value: float) -> dict:
    """入力値に最も近い化合物を返す"""
    if not SORTED_KEYS:
        return {"error": "データが登録されていません"}

    # 二分探索で挿入位置を取得
    pos = bisect.bisect_left(SORTED_KEYS, value)

    candidates = []
    if pos < len(SORTED_KEYS):
        candidates.append(SORTED_KEYS[pos])
    if pos > 0:
        candidates.append(SORTED_KEYS[pos - 1])

    closest_key = min(candidates, key=lambda k: abs(k - value))
    diff = abs(closest_key - value)

    return {
        "input": value,
        "matched_value": closest_key,
        "compound": COMPOUNDS[closest_key],
        "difference": diff,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    try:
        value = float(data.get("value", ""))
    except (TypeError, ValueError):
        return jsonify({"error": "有効な数値を入力してください"}), 400

    result = find_closest(value)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
