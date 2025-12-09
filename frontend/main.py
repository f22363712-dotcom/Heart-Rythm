from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API配置
API_BASE_URL = "http://localhost:8000"

# 首页
@app.route("/")
def index():
    return render_template("index.html")

# 情侣管理页面
@app.route("/couples")
def couples():
    return render_template("couples.html")

# 奖励管理页面
@app.route("/rewards")
def rewards():
    return render_template("rewards.html")

# 积分变动页面
@app.route("/points")
def points():
    return render_template("points.html")

# 系统统计页面
@app.route("/stats")
def stats():
    try:
        response = requests.get(f"{API_BASE_URL}/stats/")
        if response.status_code == 200:
            stats_data = response.json()
            return render_template("stats.html", stats=stats_data)
        else:
            return render_template("stats.html", stats=None, error="无法获取统计数据")
    except Exception as e:
        return render_template("stats.html", stats=None, error=str(e))

# API代理路由，用于前端调用后端API
@app.route("/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def api_proxy(path):
    url = f"{API_BASE_URL}/{path}"
    try:
        if request.method == "GET":
            response = requests.get(url, params=request.args)
        elif request.method == "POST":
            response = requests.post(url, json=request.json)
        elif request.method == "PUT":
            response = requests.put(url, json=request.json)
        elif request.method == "DELETE":
            response = requests.delete(url, params=request.args)
        else:
            return jsonify({"error": "不支持的请求方法"}), 405
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
