#青春记忆:1931-1945
#庆祝日本宣布无条件投降80周年
import time
import random
import sys


class YouthMemory:
    def __init__(self):
        # 终端适配：手机/电脑宽度调整
        self.screen_width = 40 if sys.platform.startswith('android') else 60
        # 7个核心记忆碎片（覆盖1931-1945关键节点）
        self.fragments = [
            {
                "year": 1931,
                "role": "东北中学生（高一）",
                "scene": (
                    "深秋的晨雾还没散，你正低头临摹《兰亭集序》，鼻尖几乎碰到冻得发硬的宣纸。"
                    "后排突然传来桌椅碰撞声——值日生小王正用墨汁疯狂涂抹墙上的地图，"
                    "黑褐色的墨水流下来，像从沈阳城淌出的血。历史老师攥着卷边的《盛京时报》，"
                    "指节泛白得像窗台上的冰棱：「1500个鬼子就占了沈阳，咱北大营7旅就有6000多人啊…」"
                    "窗外的北风卷着冰碴打在玻璃上，同学的棉鞋踩过走廊的薄冰，咯吱声混着远处"
                    "隐约的炮响，让人分不清是冻裂的冰面还是正在裂开的国土。"
                ),
                "choice": "你会抄《抗敌歌》歌词传看，还是组织同学去火车站拦请愿火车？",
                "options": {
                    "抄歌词": "你拆了作业本最后五页，用父亲药房的复写纸抄了50份。第三节课间，"
                             "低沉的哼唱从各个角落冒出来，像春草穿透冻土。后来在流亡关内的火车上，"
                             "你听见车厢连接处两个陌生士兵也在哼，他们说这曲子让他们在寒夜里握紧了枪。"
                             "多年后才知道，这旋律成了四万万同胞共同的呼吸。",
                    "拦火车": "你们用红墨水在白布上写「宁为玉碎」，跑到奉天站时，蒸汽火车正喷着白气准备发车。"
                             "三十七个学生齐刷刷跪在铁轨上，你能看见司机慌乱拉动汽笛的手。三个小时后，"
                             "一位戴棉帽的东北军士兵偷偷塞给你颗黄铜子弹：「这是我们欠你们的」，他转身时"
                             "你发现他军装上的纽扣都掉光了，想必是一路奔逃来的。"
                },
                "textbook_link": "（链接课本：1931年九一八事变后，东北各族人民与未撤走的东北军爱国官兵组织抗日义勇军，全国掀起抗日救亡运动。《抗敌歌》是中国最早的以抗日救亡为题材的歌曲）",
                "short_tip": "东北觉醒",
                "subject": "历史/语文"
            },
            {
                "year": 1935,
                "role": "北平中学生（高二，化学课代表）",
                "scene": (
                    "化学实验室的玻璃窗蒙着层灰，你握着滴管往玻璃片上滴浓硫酸，「还我河山」四个字"
                    "正慢慢显形——这是你摸索了三晚的技法，四个字下逐渐毛糙的玻璃是你设计的无声抗议。"
                    "班长突然撞了下你的胳膊肘，他袖口还沾着上周游行被警棍打破的血迹：「今晚改道王府井，"
                    "那儿有日军粮库，听说囤了不少粮食」。校医刘先生背着手站在门口，白大褂口袋露出"
                    "急救包的红十字：「碘仿粉给你多加了两包，这玩意儿能防伤口化脓，你省着点用。」，他镜片后的眼睛"
                    "亮得像实验室的酒精灯。"
                ),
                "choice": "你会带浓硫酸去泼日军粮袋（化学知识应用），还是用急救包跟着医疗队？",
                "options": {
                    "泼粮袋": "你往搪瓷缸里倒了半瓶浓硫酸，又灌了些自来水——上周刚学的「浓硫酸遇水放热」原理，"
                             "此刻成了最趁手的武器。粮库外的哨兵刚转身，你就把混合液泼向麻袋垛，白雾腾起时"
                             "能闻到粮食烧焦的糊味。后来化学老师在课堂上说：「知识用对地方，就是武器」，他"
                             "讲这话时，特意看了你沾着酸蚀痕迹的指甲。",
                    "当医护": "你把急救包藏在棉袄夹层里，跟着刘先生守在巷口。第一个被送过来的是初三的小邓，"
                             "额头淌着血还喊「冲啊」，你给他包扎时发现他口袋里揣着没写完的几何作业。那晚你共"
                             "给17个同学止了血，其中有个戴圆眼镜的女生说：「我以后要学法律告倒这些侵略者」。"
                             "多年后，你在报纸上看到她带着细菌战受害者跨国诉讼的照片。"
                },
                "textbook_link": "（链接课本：1935年一二·九运动中，北平学生举行抗日救国示威游行，反对华北自治，反抗日本帝国主义，掀起全国抗日救国新高潮）",
                "short_tip": "北平抗争",
                "subject": "化学/生物"
            },
            {
                "year": 1938,
                "role": "武汉兵工厂学徒（辍学高中生）",
                "scene": (
                    "车床的轰鸣声震得你耳膜发麻，铁屑溅在蓝布工装裤上烫出小窟窿。你在铁块上刻着刚算出的弹道数据："
                    "日军92式步兵炮射程2800米，咱厂里的迫击炮总差500米，这意味着前线弟兄得多扛500米的枪林弹雨。"
                    "厂长老张把本卷边的《物理学》拍在你油污的工作台上，书里夹着张泛黄的照片——穿西装的年轻人站在"
                    "国外实验室里。「留洋博士寄来的，说抛物线公式能改炮弹弧度」，他烟袋锅里的火星落在你算草纸上，"
                    "烧出个小洞，倒像炮弹炸出的弹坑。窗外，江风卷着抗日标语的碎纸，贴在生锈的铁皮屋顶上。"
                ),
                "choice": "你会按公式改炮弹弧度（数学应用），还是在炮弹里塞辣椒面（民间智慧）？",
                "options": {
                    "改弧度": "你把抛物线公式写在车间的黑板上，老工匠们围着看时，烟斗都忘了抽。三天后试射，炮弹"
                             "拖着白烟飞过江面，落在3400米外的沙洲上——比原来多飞了600米！接着这批炮弹被送往前线，"
                             "取得战果后，通讯员说正是这批炮弹压制了日军炮兵。后来你收到母校寄来的报纸，数学老师把你的公式"
                             "用红笔圈着，贴在教室最显眼的地方。",
                    "塞辣椒": "你想起老家赶马人用辣椒面防狼，便带着徒工们往空炮弹壳里塞朝天椒粉末。第一次实战后，"
                             "伤兵说鬼子被呛得涕泪横流，像群没头苍蝇。后来厂里收到八路军的感谢信，说这招被学去"
                             "打地道战，效果比手榴弹还妙。老张厂长总拿你打趣：「这脑子，不去考大学可惜了」，但你"
                             "看见他偷偷把辣椒炮弹的图纸锁进了铁皮柜。"
                },
                "textbook_link": "（链接课本：抗战时期，大后方兵工厂工人与科学家合作，克服物资匮乏困难，改进武器装备支援前线）",
                "short_tip": "军工智慧",
                "subject": "数学/物理"
            },
            {
                "year": 1940,
                "role": "西南联大先修班学生（原高三流亡生）",
                "scene": (
                    "防空洞的土腥味混着煤油灯味，你打着手电核对《应用力学》作业本——"
                    "上面有茅以升教授来联大讲座时写的公式。工程系的周教授指着怒江地图："
                    "「惠通桥的钢索总被炸断，用你算的『竹篾缆替代方案』试试？」"
                    "洞顶震落的土块砸在草图上，像日军炸弹在江面炸起的水花。"
                    "远处传来刻蜡板的沙沙声，那是同学在编《护桥三字经》："
                    "「篾缆牢，敌机恼；钢索缺，巧劲接」..."
                ),
                "choice": "你会算竹篾缆承重（理工救国），还是编《护桥三字经》（文教动员）？",
                "options": {
                    "算公式": "你找到龙竹抗拉数据，三天后算出："
                             "8股油浸竹篾缆可承重15吨！新缆索在惠通桥试用当天，"
                             "恰遇敌机轰炸——炸断的竹缆飘在江面，但主桥墩安然无恙。"
                             "前线传来消息：这周36辆军车平安过江，运去了昆明厂新造的机枪。"
                             "1956年，你站在武汉长江大桥的工地上，总想起那个在防空洞刻公式的夜晚——原来当年埋下的种子，"
                             "真能长成支撑国家的桥梁。后来你成了国家重要工程的桥梁专家，办公室里总摆着那本"
                             "缺了页的《应用力学》。",
                    "编三字经": "你把护桥要点编成朗朗上口的「篾缆牢，敌机恼；钢索缺，巧劲接」，"
                             "同学连夜刻印成《护桥手册》。筑路队王队长说："
                             "「识字的老乡看完就懂，文盲的听三遍也能背！」"
                             "三个月后，惠通桥守军靠手册提示，用竹缆及时抢修了被炸桥面。"
                             "后来在昆明街头，你听见赶马人都在哼这调子——他们说是『保命经』。"
                },
                "textbook_link": "（链接课本：全面抗战爆发后，北大、清华、南开等校迁往昆明组成西南联大，师生在艰苦环境中坚持教学科研，同时积极投身抗日宣传）",
                "short_tip": "联大坚守",
                "subject": "物理/语文"
            },
            {
                "year": 1942,
                "role": "延安《解放日报》通讯员（高二辍学生）",
                "scene": (
                    "窑洞里的油灯芯爆出火星，你捏着回民支队寄来的信，字迹被雨水泡得发皱：「吾队战士多不识字，"
                    "望将《论持久战》讲成故事」。社长老李蹲在土炕边卷烟，烟丝里混着晒干的艾叶。「陕北老乡认"
                    "『打比方』」，他吐着烟圈说，「把『持久战』说成『磨豆腐』——得慢慢磨，才能出浆」。窗外传来"
                    "纺车的嗡嗡声，月光从窗棂漏进来，在信纸上投下格子状的影子，像块没织完的布。"
                ),
                "choice": "你会把理论写成「磨豆腐」故事（通俗化），还是画成连环画（视觉化）？",
                "options": {
                    "写故事": "你把「战略防御」写成「磨子刚转，豆腐脑还没成形」，「战略相持」写成「磨得正紧，浆汁"
                             "慢慢多起来」。这篇《磨好抗战这块豆腐》被印成巴掌大的小册子，回民支队的战士们揣在"
                             "怀里，打仗间隙就互相读。后来彭德怀将军路过报社，笑着说：「这比我们讲三次课还管用」，"
                             "他临走时特意要走了你的原稿，说要带给前线的指挥员看看。",
                    "画连环": "你在马兰纸上天马行空：鬼子被画成歪嘴的豆腐块，八路军是磨豆腐的汉子，磨盘上刻着"
                             "「持久战」三个字。这套连环画在根据地流传时，连没牙的老太太都能指着画说：「这豆腐"
                             "得慢慢磨」。后来从日军俘虏那里缴获一份文件，竟是这套连环画的翻译稿——原来鬼子也在"
                             "研究，为什么老乡们看了画就更敢跟他们拼命。多年后这套画被收进博物馆，旁边摆着当年"
                             "的磨盘。"
                },
                "textbook_link": "（链接课本：敌后抗日根据地通过通俗文艺作品宣传党的政策，动员群众参与抗战，形成全民抗战的局面）",
                "short_tip": "文化抗战",
                "subject": "语文/美术"
            },
            {
                "year": 1944,
                "role":"远征军译员（高三英语尖子）",
                "scene": (
                    "缅甸丛林的雨下得像要把天空砸漏，你抹了把脸上的泥水，美军顾问正指着军用地图大喊："
                    "\"The artillery position is 5 miles north\"。炮弹呼啸着从头顶飞过，你突然想起"
                    "地理课王老师的话：1英里=1.609公里。团长正举着望远镜等坐标，你手心的汗把译稿浸得发皱——"
                    "算错一个数字，前线的弟兄就要多挨一轮轰炸。远处传来骡马的嘶鸣，那是运输队的骡马被炮声惊了，"
                    "它们的哀嚎混着枪炮声，像首怪异的交响曲。"
                ),
                "choice": "你会精准换算坐标（英语+地理），还是加句「相当于从学校跑到县城的距离」（生活化解释）？",
                "options": {
                    "精准换算": "你在膝盖上飞快计算：5×1.609=8.045公里。这个数字报出去后，美军的炮弹像长了眼睛"
                             "般落在日军阵地。战斗结束后，美军少校拍着你湿透的肩膀说：「中国高中生的换算比雷达还准」。"
                             "你摸着口袋里那张被雨水泡软的高中毕业证，突然明白王老师为什么总说「地理课能救命」。后来"
                             "你成了测绘工程师，地图上的每一条等高线，都刻着那个雨林里的下午。",
                    "生活化": "你脱口而出：「往北8公里，相当于从咱们县中跑到李家集的距离！」团长眼睛一亮——他去年"
                             "去县城开会，刚跑过这段路。炮火覆盖的瞬间，他拍着你后背大笑：「这土办法比洋坐标管用！」"
                             "后来在战术总结会上，他特意让你给参谋们讲「如何把英里说成家乡路」。多年后你当英语老师，"
                             "总给学生讲这个故事：「语言的力量，不在精准，而在让人听懂」。"
                },
                "textbook_link": "（链接课本：1942年中国远征军入缅作战，配合美英盟军打击日军，打通中印公路，为抗战胜利作出重要贡献）",
                "short_tip": "远征翻译",
                "subject": "英语/地理"
            },
            {
                "year": 1945,
                "role":"重庆中学生（备考大学）",
                "scene": (
                    "8月15日午时的蝉鸣撕扯着暑气，你正在临摹《满江红》，"
                    "毛笔尖在“待从头收拾旧山河”的“收”字上颤抖——"
                    "校工突然撞开竹篾门，"
                    "疯狂摇动手摇铃：「收音机！快听收音机！鬼子投降了！」"
                    "隔壁班传来《中国不会亡》的歌声，很快变成整条街的大合唱。"
                    "女生们撕碎日语练习册抛向空中，泛黄的纸页像群挣脱牢笼的鸟。"
                ),
                "choice": "你会带课本去街头，让老兵在扉页签名，还是把这一刻写成作文《胜利日的课堂》？",
                "options": {
                    "求签名": "你攥着课本冲到民族路，那里聚满欢呼的人群。"
                             "一位穿残破军装的老兵用刺刀尖在扉页刻下「国魂不灭」，他颤抖的手指缺了两节。"
                             "2015年抗战展上，这本课本陈列在玻璃柜中，"
                             "解说词写着：「刻在纸上的民族记忆」",
                    "写作文": "你在欢呼声中摊开作文本，茅草棚漏下的光斑跳动在"
                             "《胜利日的课堂》标题上。你写机群掠过时的恐惧，"
                             "写听到消息时毛笔掉落的瞬间，写空中飞舞的碎纸片——"
                             "那些被迫学的日语单词，此刻成了庆祝的彩屑。"
                             "这篇作文被《中央日报》刊登，结尾那句"
                             "「我们的笔，终将写回自己的山河」"
                             "成为了几个月后毕业典礼的誓词"
                },
                "textbook_link": "（链接课本：1945年8月15日，日本宣布无条件投降，中国人民取得了抗日战争的伟大胜利，这是近代以来中国人民反抗外敌入侵第一次取得完全胜利的民族解放战争）",
                "short_tip": "胜利时刻",
                "subject": "语文/历史"
            }
        ]
        self.collected = []  # 已收集碎片索引
        self.shuffled = random.sample(range(len(self.fragments)), len(self.fragments))  # 随机排序
        self.player_name = ""  # 玩家昵称（由用户输入）
        self.choices = []  # 记录关键选择
        self.subject_contrib = {"理科": 0, "文科": 0}  # 学科贡献统计
        self.unselected_options = []  # 记录未选择的选项及结果
        # 学科分类标准（用于修正统计bug）
        self.science_subjects = {'化学', '物理', '数学', '生物'}
        self.arts_subjects = {'语文', '历史', '英语', '地理', '美术'}

    def print_decor(self, char="-", length=None):
        """统一ASCII装饰，避免乱码"""
        length = length or self.screen_width
        print(char * length)

    def type_writer(self, text, delay=None):
        """动态打字效果：短文本慢读，长文本快读"""
        delay = delay or (0.05 if len(text) < 60 else 0.02)
        for c in text:
            print(c, end="", flush=True)
            time.sleep(delay)
        print()

    def welcome(self):
        """欢迎界面"""
        self.print_decor("=")
        self.type_writer("  青春记忆：1931-1945  ", 0.1)
        self.type_writer("—— 当课本知识遇上真实抗战 ——", 0.07)
        self.print_decor("=")
        self.type_writer("\n80多年前，那些和你一样的十七八岁少年：", 0.05)
        self.type_writer("- 在化学实验室里，用浓硫酸在玻璃上蚀刻出「还我河山」", 0.04)
        self.type_writer("- 在防空洞里，用抛物线公式计算炮弹轨迹，只为多打500米", 0.04)
        self.type_writer("- 在油灯下，把《论持久战》写成「磨豆腐」的故事，让老乡们都能看懂", 0.04)
        self.type_writer("- 在缅北丛林，把英里换算成「从学校到县城的距离」，帮团长精准定位", 0.04)
        self.type_writer("\n今天，你将穿过时光长廊，用他们的眼睛看那段历史——", 0.05)
        self.type_writer("不是为了记住仇恨，而是为了明白：你现在解的每道题，背的每个单词，", 0.04)
        self.type_writer("都曾是前人守护家国的武器。", 0.04)

    def set_name(self):
        """让用户输入自定义昵称"""
        while not self.player_name:  # 确保输入非空
            self.player_name = input("请输入你的名字（将记录在「青春抗战档案」中）：").strip()
        self.print_decor("-")
        self.type_writer(f"你好，{self.player_name}！很高兴与你一起解锁这段青春记忆。", 0.05)
        self.type_writer("接下来，你将遇到7个历史瞬间，每个都藏着知识的力量。", 0.04)
        self.type_writer("输入1-7选择想探索的记忆碎片，遇到选择时输入1/2做出你的决定～", 0.04)
        self.print_decor("-")

    def progress_display(self):
        """展示探索进度和待探索碎片"""
        total = len(self.fragments)
        collected_idx = set(self.collected)
        progress = []
        uncollected = []
        for i in range(total):
            if i in collected_idx:
                progress.append("■")
            else:
                progress.append("□")
                frag = self.fragments[self.shuffled[i]]
                uncollected.append(f"{i+1}（{frag['short_tip']}·{frag['subject']}）")
        
        progress_bar = "".join(progress)
        status = f"\n【探索进度】{progress_bar}  {len(collected_idx)}/{total}"
        if uncollected:
            status += f"\n  待探索：{', '.join(uncollected)}"
        else:
            status += "\n  ✨ 所有记忆已解锁！即将为你生成专属档案..."
        print(status)

    def format_text(self, text):
        """自动换行适配屏幕宽度"""
        if len(text) <= self.screen_width:
            return text
        words = text.split()
        lines, current = [], ""
        for word in words:
            if len(current + word) > self.screen_width:
                lines.append(current)
                current = word + " "
            else:
                current += word + " "
        lines.append(current)
        return "\n".join(lines)

    def trigger_egg1(self):
        """彩蛋1：集齐3个理科碎片触发"""
        self.print_decor("◇")
        self.type_writer("\n【隐藏档案：理科生的抗战】", 0.05)
        self.type_writer("1941年冬，浙江大学师生西迁途中，在贵州遵义的山洞里建起实验室：", 0.04)
        self.type_writer("- 物理系师生用铁皮罐头和X光管，造出简易X光机，救活了200多名前线伤员", 0.04)
        self.type_writer("- 化学系在破庙里提炼桐油，制成的炸药威力竟超过进口产品", 0.04)
        self.type_writer("- 数学系算出日军轰炸规律，让防空警报提前15分钟响起，挽救了上千人", 0.04)
        self.type_writer("系主任王淦昌说：「实验室就是我们的战场，烧杯就是我们的枪」。", 0.04)
        self.type_writer("这些在战乱中坚持演算的青年，后来都为祖国做出了卓著的贡献。", 0.04)
        self.print_decor("◇")
        input("\n按回车继续探索...")

    def trigger_egg2(self):
        """彩蛋2：输入1945触发（胜利年份）"""
        self.print_decor("◇")
        self.type_writer("\n【胜利日的秘密】", 0.05)
        self.type_writer("1945年8月15日，重庆中央大学的考场里发生了这样的故事：", 0.04)
        self.type_writer("英语考试进行到一半，广播里突然传出日本投降的消息。", 0.04)
        self.type_writer("有学生把试卷翻过来，在背面写下『胜利宣言』，", 0.04)
        self.type_writer("当晚，70%的学生又回到了教室——他们说：「抗战胜利了，建设中国更需要知识」。", 0.04)
        self.type_writer("那天的月亮特别亮，照亮了他们年轻的脸庞，也照亮了一个民族的希望。", 0.04)
        self.print_decor("◇")
        input("\n按回车继续...")

    def trigger_egg3(self):
        """彩蛋3：结局输入0触发（当代连接）"""
        self.print_decor("◇")
        self.type_writer("\n【你的青春与历史对话】", 0.05)
        self.type_writer(f"{self.player_name}，当你解出一道复杂的数学题时，你知道吗？", 0.04)
        self.type_writer("1938年武汉兵工厂的学徒，就是这样算出炮弹轨迹，让射程多了600米；", 0.04)
        self.type_writer("当你流利地背出英语课文时，1944年的远征军译员正用同样的专注，", 0.04)
        self.type_writer("把英里换算成「家乡的路」，帮战友躲过轰炸；", 0.04)
        self.type_writer("当你写下一篇真情实感的作文时，1942年延安的通讯员正用同样的热忱，", 0.04)
        self.type_writer("把深刻的理论写成「磨豆腐」的故事，号召群众积极抗日。", 0.04)
        self.type_writer("\n原来，你们从未分离。", 0.05)
        self.type_writer("请在下方写下你的「青春誓言」（会存入虚拟档案）：", 0.05)
        oath = input("> ")
        self.type_writer(f"\n2045年，抗战胜利100周年时，这段誓言会变成历史的一部分：{oath}", 0.04)
        self.type_writer("因为青春从不是挥霍的资本，而是用来照亮未来的火炬——", 0.04)
        self.type_writer("就像80多年前，那些和你一样年轻的人做的那样。", 0.04)
        self.print_decor("◇")

    def collect(self, idx):
        """收集碎片核心逻辑：展示场景、处理选择、记录数据"""
        total = len(self.fragments)
        if idx < 0 or idx >= total:
            self.type_writer(f"请输入1-{total}之间的数字哦～", 0.04)
            return False
        if idx in self.collected:
            frag = self.fragments[self.shuffled[idx]]
            self.type_writer(f"这段{frag['year']}年的记忆已刻入你心中，试试其他碎片吧～", 0.04)
            return False
        
        self.collected.append(idx)
        frag_idx = self.shuffled[idx]
        frag = self.fragments[frag_idx]
        self.print_decor("*", 20)
        self.type_writer(f"\n【{frag['year']}年·{frag['role']}】", 0.05)
        self.type_writer(f"学科关联：{frag['subject']}", 0.04)
        self.type_writer("场景：" + self.format_text(frag['scene']), 0.04)
        self.type_writer("\n" + frag['choice'], 0.04)
        
        # 选项交互
        options = list(frag['options'].items())
        print(f"  1. {options[0][0]}")
        print(f"  2. {options[1][0]}")
        # 场景化提示
        role_tips = {
            "东北中学生（高一）": "传歌词能唤醒人心，拦火车能直面抗争——选1或2→",
            "北平中学生（高二，化学课代表）": "化学知识能反击，急救包能救同学——选1或2→",
            "武汉兵工厂学徒（辍学高中生）": "数学改炮弹，土法显智慧——选1或2→",
            "西南联大先修班学生（原高三流亡生）": "理工造桥梁，文教聚协力——选1或2→",
            "延安《解放日报》通讯员（高二辍学生）": "故事传思想，连环画接地气——选1或2→",
            "远征军译员（高三英语尖子）": "精准换算保胜利，通俗解释更高效——选1或2→",
            "重庆中学生（备考大学）": "签名连历史，作文记当下——选1或2→"
        }
        while True:
            try:
                choice = int(input(role_tips[frag['role']])) - 1
                if 0 <= choice < 2:
                    # 记录选择的选项
                    opt_key, opt_desc = options[choice]
                    self.choices.append((frag['year'], opt_key))
                    # 记录未选择的选项及结果
                    unselected_key, unselected_desc = options[1 - choice]
                    self.unselected_options.append({
                        "year": frag['year'],
                        "role": frag['role'],
                        "unselected_option": unselected_key,
                        "unselected_desc": unselected_desc
                    })
                    # 修正学科贡献统计（根据具体学科判断）
                    subject_parts = frag['subject'].split('/')
                    is_science = any(part in self.science_subjects for part in subject_parts)
                    if is_science:
                        self.subject_contrib["理科"] += 1
                    else:
                        self.subject_contrib["文科"] += 1
                    break
                else:
                    self.type_writer("请输入1或2呀～", 0.04)
            except ValueError:
                self.type_writer("请输入数字1或2～", 0.04)
        
        self.type_writer("\n【你的行动】" + self.format_text(opt_desc), 0.04)
        self.type_writer("\n" + frag['textbook_link'], 0.03)
        self.print_decor("*", 20)
        
        # 触发彩蛋1
        if self.subject_contrib["理科"] >= 3 and self.subject_contrib["理科"] % 3 == 0:
            self.trigger_egg1()
        
        input("\n按回车继续探索...")
        return True

    def final_scene(self):
        """结局展示：贡献统计+未选择的可能性+历史回响"""
        self.print_decor("=")
        self.type_writer(f"\n🏆 抗战青春档案：{self.player_name}", 0.05)
        self.type_writer("【你的历史贡献】", 0.04)
        self.type_writer(f"- 理科贡献：{self.subject_contrib['理科']}次（武器改良/桥梁计算/精准翻译）", 0.04)
        self.type_writer(f"  你用数理化知识解决了战场上的实际问题，就像当年西南联大的师生们那样，", 0.04)
        self.type_writer(f"  在最艰苦的环境里，让公式和定理变成守护家国的盾牌。", 0.04)
        self.type_writer(f"- 文科贡献：{self.subject_contrib['文科']}次（宣传动员/历史记录/文化传播）", 0.04)
        self.type_writer(f"  你用文字和故事唤醒人心，正如那些在敌后编顺口溜、画连环画的战士，", 0.04)
        self.type_writer(f"  让精神的火炬在最黑暗的时刻也不曾熄灭。", 0.04)
        
        # 展示未选择的选项及结果
        if self.unselected_options:
            self.type_writer("\n【未选择的可能性】", 0.04)
            self.type_writer("每个选择都通向不同的历史细节，这些未走的路同样珍贵：", 0.04)
            for item in self.unselected_options:
                self.type_writer(f"- {item['year']}年·{item['role']}：若选择「{item['unselected_option']}」", 0.04)
                self.type_writer(f"  → {self.format_text(item['unselected_desc'])}", 0.04)
        
        self.type_writer("\n【历史的回响】", 0.04)
        self.type_writer("80年前的高中生们，用他们的方式回答了「知识为何而学」：", 0.04)
        self.type_writer("不是为了应付考试，而是为了在国家需要时，能拿出真本事；", 0.04)
        self.type_writer("不是为了个人前程，而是为了让脚下的土地，能少受些苦难。", 0.04)
        self.type_writer("今天的你，解数学题时会想起武汉兵工厂的弹道计算吗？", 0.04)
        self.type_writer("背英语单词时会想起缅北丛林里的翻译官吗？", 0.04)
        self.type_writer("写作文时会想起防空洞里刻蜡纸的宣传员吗？", 0.04)
        self.type_writer("\n原来，你们一直在同一条赛道上奔跑——", 0.05)
        self.type_writer("用青春和知识，守护脚下的土地，照亮民族的未来。", 0.05)
        self.print_decor("=")
        
        # 触发彩蛋3
        after_input = input("\n想写下你的青春誓言吗？输入0查看；其他键结束→")
        if after_input == "0":
            self.trigger_egg3()
            print("\n你的誓言，就是新的历史。")
        
        # 结尾标识
        print("\n程序制作/设计:风吹不动(青客联盟副盟主)\n写作/内容校对:潦草杂草汤(青客联盟文科部主任)\n欢迎加入青客联盟QQ群:874636477")

    def start(self):
        """主流程：引导→探索→结局"""
        self.welcome()
        self.set_name()
        while len(self.collected) < len(self.fragments):
            self.progress_display()
            try:
                num = input("请选择碎片编号（或输入1945触发胜利彩蛋）→")
                if num == "1945":
                    self.trigger_egg2()
                    continue
                idx = int(num) - 1
                self.collect(idx)
            except ValueError:
                self.type_writer("请输入数字哦～", 0.04)
        self.final_scene()


if __name__ == "__main__":
    game = YouthMemory()
    game.start()
