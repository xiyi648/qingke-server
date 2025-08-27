from flask import Flask, render_template, send_from_directory, url_for, request
from flask_socketio import SocketIO, emit
import os
import base64
import time  
from datetime import datetime

# 移除 Werkzeug/Flask 环境变量干扰
os.environ.pop('WERKZEUG_SERVER_FD', None)
os.environ.pop('FLASK_ENV', None)

# 初始化 Flask 应用（动态指定模板和静态目录）
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
)
app.config['SECRET_KEY'] = 'qingke_console_secret'  # 保持秘钥不变

# 初始化 SocketIO（改用 eventlet 异步模式，适配 Gunicorn worker）
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False,
    async_mode='eventlet'  # 关键修改：从 'threading' 切换为 'eventlet'
)

# ---------------------- 工具函数 ---------------------- #
def fuzzy_find_file(directory, keyword, extensions=('png', 'jpg', 'jpeg')):
    for root, _, files in os.walk(directory):
        for file in files:
            if keyword.lower() in file.lower() and file.split('.')[-1].lower() in extensions:
                return os.path.join(root, file)
    return None

def image_to_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

def is_mobile_device():
    user_agent = request.user_agent.string.lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ios', 'windows phone', 'opera mini', 'ucweb']
    return any(keyword in user_agent for keyword in mobile_keywords)

# ---------------------- 路由定义 ---------------------- #
@app.route('/download/<filename>')
def download_file(filename):
    download_dir = os.path.join(app.static_folder, 'download')
    if not os.path.exists(download_dir) or not os.path.isfile(os.path.join(download_dir, filename)):
        return "文件未找到", 404
    return send_from_directory(download_dir, filename, as_attachment=True)

@app.route('/philosophy')
def philosophy_page():
    return render_template(
        'philosophy.html',
        letter=philosophy_letter,
        poster=image_to_base64(fuzzy_find_file(app.static_folder, "哲学社海报")),
        qr_code=image_to_base64(fuzzy_find_file(app.static_folder, "哲学社二维码")),
        logo=image_to_base64(fuzzy_find_file(app.static_folder, "哲学社图标"))
    )

@app.route('/')
def index():
    template_name = 'mobile_index.html' if is_mobile_device() else 'pc_index.html'
    return render_template(template_name, **get_page_data())

# ---------------------- 数据初始化 ---------------------- #
# 图片 Base64 预处理
logo_b64 = image_to_base64(fuzzy_find_file(app.static_folder, "青客联盟图标"))
qrcode_b64 = image_to_base64(fuzzy_find_file(app.static_folder, "青客联盟二维码"))
poster_b64 = image_to_base64(fuzzy_find_file(app.static_folder, "文娱部宣传海报"))

# 哲学社信件内容（保持不变）
philosophy_letter = """福清一中“凌空”哲学社给新生们的一封信...（原文省略，保持不变）"""

# 资源、成员、时间线等数据（保持不变）
download_dir = os.path.join(app.static_folder, 'download')
resources = []
if os.path.exists(download_dir):
    with app.test_request_context():
        for file in os.listdir(download_dir):
            if os.path.isfile(os.path.join(download_dir, file)):
                resources.append({
                    "name": file,
                    "url": url_for('download_file', filename=file)
                })

people = [
    {"name": "知天易", "title": "盟主", "intro": "曾获物理竞赛省一"},
    {"name": "潦草杂草汤", "title": "文科部主任", "intro": "曾获福清市新时代好少年"},
    {"name": "风吹不动", "title": "副盟主", "intro": "创始人，啥也不是"},
    {"name": "被猫吃了", "title": "联盟驻信息社外交官", "intro": "尊贵的菁英班大佬"},
    {"name": "蓝莓酸", "title": "测试部主任", "intro": "文娱部民乐组组长"}
]

timeline = [
    {"date": "2025/02/03", "event": "风吹不动和潦草杂草汤 用钱帮助了一位在寒风中辛苦卖菜的削瘦老人，青客联盟的精神由此萌发 "},
    {"date": "2025/07/13", "event": "风吹不动发布了一款针对信息社网站的一键猜分程序，并且创立了青客联盟"},
    {"date": "2025/07/15", "event": "一致通过知天易建议，风吹不动开放「一元代做综评」源代码"},
    {"date": "2025/07/16", "event": "风吹不动任命知天易为代理盟主"},
    {"date": "2025/08/08", "event": "知天易接任盟主，册封蓝莓酸，被猫吃了头衔"},
    {"date": "2025/08/16", "event": "为了纪念日本宣布无条件投降80周年风吹不动和潦草杂草汤用Python开发了一款文字游戏《青春记忆1931-1945》，并上传抖音。隔日风吹不动调整联盟职责归属：知天易仍为盟主，风吹不动为副盟主，蓝莓酸为测试部主任，被猫吃了为联盟驻信息社外交官，潦草杂草汤为文科部主任"}
]

friend_link = {"name": "福清一中信息社", "url": "https://guess.gsqclub.cn/account/registerStep1.php"}
open_source_license = "MIT License"
qq_group = "874636477"

def get_page_data():
    return {
        "logo_b64": logo_b64,
        "qrcode_b64": qrcode_b64,
        "poster_b64": poster_b64,
        "people": people,
        "timeline": timeline,
        "resources": resources,
        "qq_group": qq_group,
        "friend_link": friend_link,
        "open_source_license": open_source_license,
        "philosophy_icon": image_to_base64(fuzzy_find_file(app.static_folder, "哲学社图标")),
        "philosophy_button": "「凌空」哲学社，来看看吗？",
        "philosophy_link": url_for('philosophy_page')
    }

# ---------------------- SocketIO 事件 ---------------------- #
@socketio.on('connect')
def handle_connect():
    emit('heartbeat', {'status': 'alive'})

# ---------------------- 启动入口（动态适配端口） ---------------------- #
if __name__ == '__main__':
    # 优先读取环境变量 PORT（Render 自动注入），本地默认 1126
    port = int(os.environ.get("PORT", 1126))  
    socketio.run(
        app,
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False
    )