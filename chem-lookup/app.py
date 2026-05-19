from flask import Flask, request, jsonify, render_template

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


def find_in_range(value: float, tolerance: float, tolerance_type: str) -> dict:
    """許容範囲内の化合物をすべて返す"""
    if not COMPOUNDS:
        return {"error": "データが登録されていません"}

    results = []
    for key, name in COMPOUNDS.items():
        diff = abs(key - value)

        if tolerance_type == "absolute":
            # 絶対値：差がtolerance以内
            in_range = diff <= tolerance
        else:
            # 相対値：差が入力値のtolerance%以内
            in_range = diff <= value * (tolerance / 100)

        if in_range:
            results.append({
                "matched_value": key,
                "compound": name,
                "difference": diff,
            })

    # 差が小さい順に並べる
    results.sort(key=lambda x: x["difference"])

    return {
        "input": value,
        "tolerance": tolerance,
        "tolerance_type": tolerance_type,
        "results": results,
        "count": len(results),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    try:
        value = float(data.get("value", ""))
        tolerance = float(data.get("tolerance", 0))
        tolerance_type = data.get("tolerance_type", "absolute")
    except (TypeError, ValueError):
        return jsonify({"error": "有効な数値を入力してください"}), 400

    if tolerance < 0:
        return jsonify({"error": "許容範囲は0以上で入力してください"}), 400

    result = find_in_range(value, tolerance, tolerance_type)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)