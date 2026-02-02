"""
心动积分项目 - 前端应用 (v2.0)
使用Flask构建Web界面，支持用户认证
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "heartbeat_secret_key_2024"  # 用于session加密

# API配置
API_BASE_URL = "http://localhost:8000"

@app.route("/")
def index():
    """首页"""
    return render_template("index_new.html")

@app.route("/login")
def login():
    """登录页面"""
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    """用户仪表板"""
    return render_template("dashboard.html")

@app.route("/rewards")
def rewards():
    """奖励管理页面"""
    return render_template("rewards_new.html")

@app.route("/admin")
def admin():
    """管理员后台"""
    return render_template("admin.html")

# API代理路由
@app.route("/api/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def api_proxy(path):
    """API代理，转发请求到后端"""
    url = f"{API_BASE_URL}/{path}"
    try:
        # 根据请求方法转发请求
        if request.method == "GET":
            response = requests.get(url, params=request.args, timeout=10, headers=request.headers)
        elif request.method == "POST":
            response = requests.post(url, json=request.json, headers=request.headers, timeout=10)
        elif request.method == "PUT":
            response = requests.put(url, json=request.json, headers=request.headers, timeout=10)
        elif request.method == "DELETE":
            response = requests.delete(url, params=request.args, headers=request.headers, timeout=10)
        else:
            return jsonify({"error": "不支持的请求方法"}), 405
        
        # 处理响应，保留原始状态码和头部
        try:
            # 尝试解析JSON响应
            data = response.json()
            return jsonify(data), response.status_code
        except ValueError:
            # 如果不是JSON响应，直接返回原始响应内容
            return response.content, response.status_code, response.headers.items()
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "无法连接到后端服务，请确保后端已启动"}), 503
    except Exception as e:
        return jsonify({"error": f"代理请求失败: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
