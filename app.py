from flask import Flask, render_template, send_from_directory, url_for, request
from flask_socketio import SocketIO, emit
import os
import base64
import time  
from datetime import datetime
os.environ.pop('WERKZEUG_SERVER_FD', None)
os.environ.pop('FLASK_ENV', None)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
)
app.config['SERVER_NAME'] = '0.0.0.0:1126'  # 保留原始配置
app.config['SECRET_KEY'] = 'qingke_console_secret'  
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    logger=False,
    engineio_logger=False,
    async_mode='threading'  # 恢复原始异步模式（需配合下方启动命令）
)

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

@app.route('/download/<filename>')
def download_file(filename):
    download_dir = os.path.join(app.static_folder, 'download')
    if not os.path.exists(download_dir) or not os.path.isfile(os.path.join(download_dir, filename)):
        return "文件未找到", 404
    return send_from_directory(download_dir, filename, as_attachment=True)

logo_b64 = image_to_base64(fuzzy_find_file(app.static_folder, "青客联盟图标"))
qrcode_b64 = image_to_base64(fuzzy_find_file(app.static_folder, "青客联盟二维码"))
poster_b64 = image_to_base64(fuzzy_find_file(app.static_folder, "文娱部宣传海报"))

philosophy_letter = """福清一中“凌空”哲学社给新生们的一封信

To 即将进入一中的学弟学妹们：

见字如面！

“我有不释卷，与君共赏之”。在这个身闲时好的夏天，福清一中“凌空”哲学社诚挚地邀请您加入本社，共话古今哲思之理，同寻真理价值所在。若问缘由，且看以下四点是否足以让你心动：

1.本社既名曰“哲学社”，自然是以品析哲学为宗旨。而“哲学”作为“爱智之学”，品析之下且不论那些“证明宇宙中自然律的存在”等宏大命题带给人类的价值，单单对于高中生而言，品析哲学可以帮助你接近“中式教育下学习的意义所在”“所谓‘真爱’到底是不是一个谎言”“自由意志是否存在”等与精神生活息息相关的问题的答案，最不济从功利主义的角度看也可以提升你的数学逻辑推理和语文议论文思辨等能力。

2.哲学社目前暂定主要开展两项活动，分别为“百家讲坛”和辩论赛。其中“百家讲坛”暂定由两位副社长主讲（即为“百家”，当然不排除新人，也就是在看这封信的你们中的潜在讲师），内容涵盖了 西方哲学史，各类哲学命题和各哲学流派（即各种“主义”）的介绍，旨在帮助社员们入门哲学并一定程度地系统地了解哲学知识。此外，在“百家讲坛”开展到一定程度之后，本社暂定在用一次社团活动时间来介绍辩论的规则&技巧&要求的基础上，穿插进行辩论赛，旨在让社员们于意识形态无比澎湃的现场中运用哲学知识以获得思辨的快乐。

3.哲学社极其尊重社员们的言论自由，everyone的任何看法和意见经由我们珍重地审视后都可能影响最终内容的呈现。换言之，“凌空”哲学社到底会成为怎样的一个社团，其决定权在每个社员手中。

4.其余请参见哲学社招新视频（约八月发布）

最后，我们想说：其实选择没有绝对的对错，未来尚远，过去已去，时间会证明一切。如果说就读于福清一中是你人生旅途中的必经之路，那么我们希望“凌空”哲学社能成为你们沿途中“浮生暂寄梦中梦，一晌贪欢”的片刻乌托邦，真的，时间会证明你们选择的价值。

P.S. 最后的最后，若有意愿加入哲学社者，请扫码入群了解更多讯息
群号：981094818

若仍有疑问，欢迎添加学长学姐 QQ
社长：3657165489
副社 L：229912402
副社 F：3579577741
副社 Y：3083019832

祝，
每个加入哲学社的同学都能在这里知道自己想知道的一切！

某副社长
2025年七月于凤凰山"""

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

@app.route('/philosophy')
def philosophy_page():
    return render_template(
        'philosophy.html',
        letter=philosophy_letter,
        poster=image_to_base64(fuzzy_find_file(app.static_folder, "哲学社海报")),
        qr_code=image_to_base64(fuzzy_find_file(app.static_folder, "哲学社二维码")),
        logo=image_to_base64(fuzzy_find_file(app.static_folder, "哲学社图标"))  # 恢复原始变量名（需配合前端修正）
    )

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
        "philosophy_icon": image_to_base64(fuzzy_find_file(app.static_folder, "哲学社图标")),  # 保留原始变量（供前端使用）
        "philosophy_button": "「凌空」哲学社，来看看吗？",
        "philosophy_link": url_for('philosophy_page')
    }

@app.route('/')
def index():
    template_name = 'mobile_index.html' if is_mobile_device() else 'pc_index.html'
    return render_template(template_name, **get_page_data())

@socketio.on('connect')
def handle_connect():
    emit('heartbeat', {'status': 'alive'})

if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=1126,
        debug=False,
        use_reloader=False
    )