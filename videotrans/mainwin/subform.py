import os
import re

from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import Qt
from videotrans.configure import config
from videotrans.util import tools


class Subform():
    def __init__(self, main=None):
        self.main = main
    # 设置每行角色
    def set_line_role_fun(self):
        def get_checked_boxes(widget):
            checked_boxes = []
            for child in widget.children():
                if isinstance(child, QtWidgets.QCheckBox) and child.isChecked():
                    checked_boxes.append(child.objectName())
                else:
                    checked_boxes.extend(get_checked_boxes(child))
            return checked_boxes

        def save(role):
            # 初始化一个列表，用于存放所有选中 checkbox 的名字
            checked_checkbox_names = get_checked_boxes(self.main.w)

            if len(checked_checkbox_names) < 1:
                return QtWidgets.QMessageBox.critical(self.main.w, config.transobj['anerror'],
                                            config.transobj['zhishaoxuanzeyihang'])

            for n in checked_checkbox_names:
                _, line = n.split('_')
                # 设置labe为角色名
                ck = self.main.w.findChild(QtWidgets.QCheckBox, n)
                ck.setText(config.transobj['default'] if role in ['No', 'no', '-'] else role)
                ck.setChecked(False)
                config.params['line_roles'][line] = config.params['voice_role'] if role in ['No', 'no', '-'] else role

        from videotrans.component import SetLineRole
        self.main.w = SetLineRole()
        box = QtWidgets.QWidget()  # 创建新的 QWidget，它将承载你的 QHBoxLayouts
        box.setLayout(QtWidgets.QVBoxLayout())  # 设置 QVBoxLayout 为新的 QWidget 的layout
        if config.params['voice_role'] in ['No', '-', 'no']:
            return QtWidgets.QMessageBox.critical(self.main.w, config.transobj['anerror'], config.transobj['xianxuanjuese'])
        if not self.main.subtitle_area.toPlainText().strip():
            return QtWidgets.QMessageBox.critical(self.main.w, config.transobj['anerror'], config.transobj['youzimuyouset'])

        #  获取字幕
        srt_json = tools.get_subtitle_from_srt(self.main.subtitle_area.toPlainText().strip(), is_file=False)
        for it in srt_json:
            # 创建新水平布局
            h_layout = QtWidgets.QHBoxLayout()
            check = QtWidgets.QCheckBox()
            check.setText(
                config.params['line_roles'][f'{it["line"]}'] if f'{it["line"]}' in config.params['line_roles'] else
                config.transobj['default'])
            check.setObjectName(f'check_{it["line"]}')
            # 创建并配置 QLineEdit
            line_edit = QtWidgets.QLineEdit()
            line_edit.setPlaceholderText(config.transobj['shezhijueseline'])

            line_edit.setText(f'[{it["line"]}] {it["text"]}')
            line_edit.setReadOnly(True)
            # 将标签和编辑线添加到水平布局
            h_layout.addWidget(check)
            h_layout.addWidget(line_edit)
            box.layout().addLayout(h_layout)
        box.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main.w.select_role.addItems(self.main.current_rolelist)
        self.main.w.set_role_label.setText(config.transobj['shezhijuese'])

        self.main.w.select_role.currentTextChanged.connect(save)
        # 创建 QScrollArea 并将 box QWidget 设置为小部件
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(box)
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 将 QScrollArea 添加到主窗口的 layout
        self.main.w.layout.addWidget(scroll_area)

        self.main.w.set_ok.clicked.connect(lambda: self.main.w.close())
        self.main.w.show()



    def open_youtube(self):
        def download():
            proxy = self.main.youw.proxy.text().strip()
            outdir = self.main.youw.outputdir.text()
            url = self.main.youw.url.text().strip()
            vid = self.main.youw.formatname.isChecked()
            if not url or not re.match(r'^https://(www.)?(youtube.com/(watch|shorts)|youtu.be/\w)', url, re.I):
                QtWidgets.QMessageBox.critical(self.main.youw, config.transobj['anerror'],
                                     config.transobj['You must fill in the YouTube video playback page address'])
                return
            self.main.settings.setValue("youtube_outdir", outdir)
            if proxy:
                config.proxy = proxy
                self.main.settings.setValue("proxy", proxy)
            from videotrans.task.download_youtube import Download
            down = Download(proxy=proxy, url=url, out=outdir, parent=self.main, vid=vid)
            down.start()
            self.main.youw.set.setText(config.transobj["downing..."])

        def selectdir():
            dirname = QtWidgets.QFileDialog.getExistingDirectory(self.main, "Select Dir", outdir).replace('\\', '/')
            self.main.youw.outputdir.setText(dirname)

        from videotrans.component import YoutubeForm
        self.main.youw = YoutubeForm()
        self.main.youw.set.setText(config.transobj['start download'])
        self.main.youw.selectdir.setText(config.transobj['Select Out Dir'])
        outdir = config.params['youtube_outdir'] if 'youtube_outdir' in config.params else os.path.join(config.homedir,
                                                                                                        'youtube').replace(
            '\\', '/')
        if not os.path.exists(outdir):
            os.makedirs(outdir, exist_ok=True)
        # 创建事件过滤器实例并将其安装到 lineEdit 上

        self.main.youw.outputdir.setText(outdir)
        if config.proxy:
            self.main.youw.proxy.setText(config.proxy)
        self.main.youw.selectdir.clicked.connect(selectdir)

        self.main.youw.set.clicked.connect(download)
        self.main.youw.show()

    # set deepl key
    def set_deepL_key(self):
        def save():
            key = self.main.w.deepl_authkey.text()
            api = self.main.w.deepl_api.text().strip()
            self.main.settings.setValue("deepl_authkey", key)
            config.params['deepl_authkey'] = key
            self.main.settings.setValue("deepl_api", api)
            config.params['deepl_api'] = api
            self.main.w.close()

        from videotrans.component import DeepLForm
        self.main.w = DeepLForm()
        if config.params['deepl_authkey']:
            self.main.w.deepl_authkey.setText(config.params['deepl_authkey'])
        if config.params['deepl_api']:
            self.main.w.deepl_api.setText(config.params['deepl_api'])
        self.main.w.set_deepl.clicked.connect(save)
        self.main.w.show()

    def set_auzuretts_key(self):
        def save():
            key = self.main.aztw.speech_key.text()
            region = self.main.aztw.speech_region.text().strip()
            self.main.settings.setValue("azure_speech_key", key)
            self.main.settings.setValue("azure_speech_region", region)

            config.params['azure_speech_key'] = key
            config.params['azure_speech_region'] = region
            self.main.aztw.close()

        from videotrans.component import AzurettsForm
        self.main.aztw = AzurettsForm()
        if config.params['azure_speech_region']:
            self.main.aztw.speech_region.setText(config.params['azure_speech_region'])
        if config.params['azure_speech_key']:
            self.main.aztw.speech_key.setText(config.params['azure_speech_key'])
        self.main.aztw.save.clicked.connect(save)
        self.main.aztw.show()

    def set_elevenlabs_key(self):
        def save():
            key = self.main.w.elevenlabstts_key.text()
            self.main.settings.setValue("elevenlabstts_key", key)
            config.params['elevenlabstts_key'] = key
            self.main.w.close()

        from videotrans.component import ElevenlabsForm
        self.main.w = ElevenlabsForm()
        if config.params['elevenlabstts_key']:
            self.main.w.elevenlabstts_key.setText(config.params['elevenlabstts_key'])
        self.main.w.set.clicked.connect(save)
        self.main.w.show()

    def set_deepLX_address(self):
        def save():
            key = self.main.w.deeplx_address.text()
            self.main.settings.setValue("deeplx_address", key)
            config.params["deeplx_address"] = key
            self.main.w.close()

        from videotrans.component import DeepLXForm
        self.main.w = DeepLXForm()
        if config.params["deeplx_address"]:
            self.main.w.deeplx_address.setText(config.params["deeplx_address"])
        self.main.w.set_deeplx.clicked.connect(save)
        self.main.w.show()

    def set_ott_address(self):
        def save():
            key = self.main.w.ott_address.text()
            self.main.settings.setValue("ott_address", key)
            config.params["ott_address"] = key
            self.main.w.close()

        from videotrans.component import OttForm
        self.main.w = OttForm()
        if config.params["ott_address"]:
            self.main.w.ott_address.setText(config.params["ott_address"])
        self.main.w.set_ott.clicked.connect(save)
        self.main.w.show()

    def set_clone_address(self):
        class TestTTS(QThread):
            uito = Signal(str)

            def __init__(self, *, parent=None, text=None, language=None, role=None):
                super().__init__(parent=parent)
                self.text = text
                self.language = language
                self.role = role

            def run(self):
                from videotrans.tts.clone import get_voice
                try:
                    tools.get_clone_role(True)
                    if len(config.clone_voicelist) < 2:
                        raise Exception('没有可供测试的声音')
                    get_voice(text=self.text, language=self.language, role=config.clone_voicelist[1], set_p=False,
                              filename=config.homedir + "/test.mp3")

                    self.uito.emit("ok")
                except Exception as e:
                    self.uito.emit(str(e))

        def feed(d):
            if d == "ok":
                tools.pygameaudio(config.homedir + "/test.mp3")
                QtWidgets.QMessageBox.information(self.main.clonw, "ok", "Test Ok")
            else:
                QtWidgets.QMessageBox.critical(self.main.clonw, config.transobj['anerror'], d)
            self.main.clonw.test.setText('测试' if config.defaulelang == 'zh' else 'Test')

        def test():
            if not self.main.clonw.clone_address.text().strip():
                QtWidgets.QMessageBox.critical(self.main.clonw, config.transobj['anerror'], '必须填写http地址')
                return
            config.params['clone_api'] = self.main.clonw.clone_address.text().strip()
            task = TestTTS(parent=self.main.clonw,
                           text="你好啊我的朋友" if config.defaulelang == 'zh' else 'hello,my friend'
                           , language="zh-cn" if config.defaulelang == 'zh' else 'en')
            self.main.clonw.test.setText('测试中请稍等...' if config.defaulelang == 'zh' else 'Testing...')
            task.uito.connect(feed)
            task.start()

        def save():
            key = self.main.clonw.clone_address.text().strip()
            key = key.rstrip('/')
            key = 'http://' + key.replace('http://', '')
            self.main.settings.setValue("clone_api", key)
            config.params["clone_api"] = key
            self.main.clonw.close()

        from videotrans.component import CloneForm
        self.main.clonw = CloneForm()
        if config.params["clone_api"]:
            self.main.clonw.clone_address.setText(config.params["clone_api"])
        self.main.clonw.set_clone.clicked.connect(save)
        self.main.clonw.test.clicked.connect(test)
        self.main.clonw.show()

    # set baidu
    def set_baidu_key(self):
        def save_baidu():
            appid = self.main.w.baidu_appid.text()
            miyue = self.main.w.baidu_miyue.text()
            self.main.settings.setValue("baidu_appid", appid)
            self.main.settings.setValue("baidu_miyue", miyue)
            config.params["baidu_appid"] = appid
            config.params["baidu_miyue"] = miyue
            self.main.w.close()

        from videotrans.component import BaiduForm
        self.main.w = BaiduForm()
        if config.params["baidu_appid"]:
            self.main.w.baidu_appid.setText(config.params["baidu_appid"])
        if config.params["baidu_miyue"]:
            self.main.w.baidu_miyue.setText(config.params["baidu_miyue"])
        self.main.w.set_badiu.clicked.connect(save_baidu)
        self.main.w.show()

    def set_tencent_key(self):
        def save():
            SecretId = self.main.w.tencent_SecretId.text()
            SecretKey = self.main.w.tencent_SecretKey.text()
            self.main.settings.setValue("tencent_SecretId", SecretId)
            self.main.settings.setValue("tencent_SecretKey", SecretKey)
            config.params["tencent_SecretId"] = SecretId
            config.params["tencent_SecretKey"] = SecretKey
            self.main.w.close()

        from videotrans.component import TencentForm
        self.main.w = TencentForm()
        if config.params["tencent_SecretId"]:
            self.main.w.tencent_SecretId.setText(config.params["tencent_SecretId"])
        if config.params["tencent_SecretKey"]:
            self.main.w.tencent_SecretKey.setText(config.params["tencent_SecretKey"])
        self.main.w.set_tencent.clicked.connect(save)
        self.main.w.show()

    # set chatgpt
    def set_chatgpt_key(self):
        class TestChatgpt(QThread):
            uito = Signal(str)

            def __init__(self, *, parent=None):
                super().__init__(parent=parent)

            def run(self):
                try:
                    from videotrans.translator.chatgpt import trans as trans_chatgpt
                    raw = "你好啊我的朋友" if config.defaulelang != 'zh' else "hello,my friend"
                    text = trans_chatgpt(raw, "English" if config.defaulelang != 'zh' else "Chinese", set_p=False,
                                         inst=None, is_test=True)
                    self.uito.emit(f"ok:{raw}\n{text}")
                except Exception as e:
                    self.uito.emit(str(e))

        def feed(d):
            if not d.startswith("ok:"):
                QtWidgets.QMessageBox.critical(self.main.w, config.transobj['anerror'], d)
            else:
                QtWidgets.QMessageBox.information(self.main.w, "OK", d[3:])
            self.main.w.test_chatgpt.setText('测试' if config.defaulelang == 'zh' else 'Test')

        def test():
            key = self.main.w.chatgpt_key.text()
            api = self.main.w.chatgpt_api.text().strip()
            api = api if api else 'https://api.openai.com/v1'
            model = self.main.w.chatgpt_model.currentText()
            template = self.main.w.chatgpt_template.toPlainText()
            self.main.settings.setValue("chatgpt_key", key)
            self.main.settings.setValue("chatgpt_api", api)

            self.main.settings.setValue("chatgpt_model", model)
            self.main.settings.setValue("chatgpt_template", template)

            os.environ['OPENAI_API_KEY'] = key
            config.params["chatgpt_key"] = key
            config.params["chatgpt_api"] = api
            config.params["chatgpt_model"] = model
            config.params["chatgpt_template"] = template

            task = TestChatgpt(parent=self.main.w)
            self.main.w.test_chatgpt.setText('测试中请稍等...' if config.defaulelang == 'zh' else 'Testing...')
            task.uito.connect(feed)
            task.start()
            self.main.w.test_chatgpt.setText('测试中请稍等...' if config.defaulelang == 'zh' else 'Testing...')

        def save_chatgpt():
            key = self.main.w.chatgpt_key.text()
            api = self.main.w.chatgpt_api.text().strip()
            api = api if api else 'https://api.openai.com/v1'
            model = self.main.w.chatgpt_model.currentText()
            template = self.main.w.chatgpt_template.toPlainText()
            self.main.settings.setValue("chatgpt_key", key)
            self.main.settings.setValue("chatgpt_api", api)

            self.main.settings.setValue("chatgpt_model", model)
            self.main.settings.setValue("chatgpt_template", template)

            os.environ['OPENAI_API_KEY'] = key
            config.params["chatgpt_key"] = key
            config.params["chatgpt_api"] = api
            config.params["chatgpt_model"] = model
            config.params["chatgpt_template"] = template

            self.main.w.close()

        from videotrans.component import ChatgptForm
        self.main.w = ChatgptForm()
        if config.params["chatgpt_key"]:
            self.main.w.chatgpt_key.setText(config.params["chatgpt_key"])
        if config.params["chatgpt_api"]:
            self.main.w.chatgpt_api.setText(config.params["chatgpt_api"])
        if config.params["chatgpt_model"]:
            self.main.w.chatgpt_model.setCurrentText(config.params["chatgpt_model"])
        if config.params["chatgpt_template"]:
            self.main.w.chatgpt_template.setPlainText(config.params["chatgpt_template"])
        self.main.w.set_chatgpt.clicked.connect(save_chatgpt)
        self.main.w.test_chatgpt.clicked.connect(test)
        self.main.w.show()

    def set_ttsapi(self):
        class TestTTS(QThread):
            uito = Signal(str)

            def __init__(self, *, parent=None, text=None, language=None, rate="+0%", role=None):
                super().__init__(parent=parent)
                self.text = text
                self.language = language
                self.rate = rate
                self.role = role

            def run(self):

                from videotrans.tts.ttsapi import get_voice
                try:

                    get_voice(text=self.text, language=self.language, rate=self.rate, role=self.role, set_p=False,
                              filename=config.homedir + "/test.mp3")

                    self.uito.emit("ok")
                except Exception as e:
                    self.uito.emit(str(e))

        def feed(d):
            if d == "ok":
                tools.pygameaudio(config.homedir + "/test.mp3")
                QtWidgets.QMessageBox.information(self.main.ttsapiw, "ok", "Test Ok")
            else:
                QtWidgets.QMessageBox.critical(self.main.ttsapiw, config.transobj['anerror'], d)
            self.main.ttsapiw.test.setText('测试api' if config.defaulelang == 'zh' else 'Test api')

        def test():
            url = self.main.ttsapiw.api_url.text()
            extra = self.main.ttsapiw.extra.text()
            role = self.main.ttsapiw.voice_role.text().strip()

            self.main.settings.setValue("ttsapi_url", url)
            self.main.settings.setValue("ttsapi_extra", extra if extra else "pyvideotrans")
            self.main.settings.setValue("ttsapi_voice_role", role)

            config.params["ttsapi_url"] = url
            config.params["ttsapi_extra"] = extra
            config.params["ttsapi_voice_role"] = role

            task = TestTTS(parent=self.main.ttsapiw,
                           text="你好啊我的朋友" if config.defaulelang == 'zh' else 'hello,my friend',
                           role=self.main.ttsapiw.voice_role.text().strip().split(',')[0],
                           language="zh-cn" if config.defaulelang == 'zh' else 'en')
            self.main.ttsapiw.test.setText('测试中请稍等...' if config.defaulelang == 'zh' else 'Testing...')
            task.uito.connect(feed)
            task.start()

        def save():
            url = self.main.ttsapiw.api_url.text()
            extra = self.main.ttsapiw.extra.text()
            role = self.main.ttsapiw.voice_role.text().strip()

            self.main.settings.setValue("ttsapi_url", url)
            self.main.settings.setValue("ttsapi_extra", extra if extra else "pyvideotrans")
            self.main.settings.setValue("ttsapi_voice_role", role)

            config.params["ttsapi_url"] = url
            config.params["ttsapi_extra"] = extra
            config.params["ttsapi_voice_role"] = role
            self.main.ttsapiw.close()

        from videotrans.component import TtsapiForm
        self.main.ttsapiw = TtsapiForm()
        if config.params["ttsapi_url"]:
            self.main.ttsapiw.api_url.setText(config.params["ttsapi_url"])
        if config.params["ttsapi_voice_role"]:
            self.main.ttsapiw.voice_role.setText(config.params["ttsapi_voice_role"])
        if config.params["ttsapi_extra"]:
            self.main.ttsapiw.extra.setText(config.params["ttsapi_extra"])

        self.main.ttsapiw.save.clicked.connect(save)
        self.main.ttsapiw.test.clicked.connect(test)
        self.main.ttsapiw.show()

    def set_transapi(self):
        class Test(QThread):
            uito = Signal(str)

            def __init__(self, *, parent=None, text=None):
                super().__init__(parent=parent)
                self.text = text

            def run(self):
                from videotrans.translator.transapi import trans
                try:
                    t = trans(self.text, target_language="en", set_p=False, source_code="zh", is_test=True)
                    self.uito.emit(f"ok:{self.text}\n{t}")
                except Exception as e:
                    self.uito.emit(str(e))

        def feed(d):
            if d.startswith("ok:"):
                QtWidgets.QMessageBox.information(self.main.transapiw, "ok", d[3:])
            else:
                QtWidgets.QMessageBox.critical(self.main.transapiw, config.transobj['anerror'], d)
            self.main.transapiw.test.setText('测试api' if config.defaulelang == 'zh' else 'Test api')

        def test():
            url = self.main.transapiw.api_url.text()
            config.params["ttsapi_url"] = url
            if not url:
                return QtWidgets.QMessageBox.critical(self.main.transapiw, config.transobj['anerror'],
                                            "必须填写自定义翻译的url" if config.defaulelang == 'zh' else "The url of the custom translation must be filled in")
            url = self.main.transapiw.api_url.text()
            miyue = self.main.transapiw.miyue.text()
            self.main.settings.setValue("trans_api_url", url)
            self.main.settings.setValue("trans_secret", miyue)
            config.params["trans_api_url"] = url
            config.params["trans_secret"] = miyue
            task = Test(parent=self.main.transapiw, text="你好啊我的朋友")
            self.main.transapiw.test.setText('测试中请稍等...' if config.defaulelang == 'zh' else 'Testing...')
            task.uito.connect(feed)
            task.start()

        def save():
            url = self.main.transapiw.api_url.text()
            miyue = self.main.transapiw.miyue.text()
            self.main.settings.setValue("trans_api_url", url)
            self.main.settings.setValue("trans_secret", miyue)
            config.params["trans_api_url"] = url
            config.params["trans_secret"] = miyue
            self.main.transapiw.close()

        from videotrans.component import TransapiForm
        self.main.transapiw = TransapiForm()
        if config.params["trans_api_url"]:
            self.main.transapiw.api_url.setText(config.params["trans_api_url"])
        if config.params["trans_secret"]:
            self.main.transapiw.miyue.setText(config.params["trans_secret"])

        self.main.transapiw.save.clicked.connect(save)
        self.main.transapiw.test.clicked.connect(test)
        self.main.transapiw.show()

    def set_gptsovits(self):
        class TestTTS(QThread):
            uito = Signal(str)

            def __init__(self, *, parent=None, text=None, language=None, role=None):
                super().__init__(parent=parent)
                self.text = text
                self.language = language
                self.role = role

            def run(self):
                from videotrans.tts.gptsovits import get_voice
                try:
                    get_voice(text=self.text, language=self.language, set_p=False, role=self.role,
                              filename=config.homedir + "/test.wav")
                    self.uito.emit("ok")
                except Exception as e:
                    self.uito.emit(str(e))

        def feed(d):
            if d == "ok":
                tools.pygameaudio(config.homedir + "/test.wav")
                QtWidgets.QMessageBox.information(self.main.gptsovitsw, "ok", "Test Ok")
            else:
                QtWidgets.QMessageBox.critical(self.main.gptsovitsw, config.transobj['anerror'], d)
            self.main.gptsovitsw.test.setText('测试api')

        def test():
            url = self.main.gptsovitsw.api_url.text()
            config.params["gptsovits_url"] = url
            task = TestTTS(parent=self.main.gptsovitsw,
                           text="你好啊我的朋友",
                           role=getrole(),
                           language="zh")
            self.main.gptsovitsw.test.setText('测试中请稍等...')
            task.uito.connect(feed)
            task.start()

        def getrole():
            tmp = self.main.gptsovitsw.role.toPlainText().strip()
            role = None
            if not tmp:
                return role

            for it in tmp.split("\n"):
                s = it.strip().split('#')
                if len(s) != 3:
                    QtWidgets.QMessageBox.critical(self.main.gptsovitsw, config.transobj['anerror'],
                                         "每行都必须以#分割为三部分，格式为   音频名称.wav#音频文字内容#音频语言代码")
                    return
                if not s[0].endswith(".wav"):
                    QtWidgets.QMessageBox.critical(self.main.gptsovitsw, config.transobj['anerror'],
                                         "每行都必须以#分割为三部分，格式为  音频名称.wav#音频文字内容#音频语言代码 ,并且第一部分为.wav结尾的音频名称")
                    return
                if s[2] not in ['zh', 'ja', 'en']:
                    QtWidgets.QMessageBox.critical(self.main.gptsovitsw, config.transobj['anerror'],
                                         "每行必须以#分割为三部分，格式为 音频名称.wav#音频文字内容#音频语言代码 ,并且第三部分语言代码只能是 zh或en或ja")
                    return
                role = s[0]
            config.params['gptsovits_role'] = tmp
            self.main.settings.setValue("gptsovits_rolel", tmp)
            return role

        def save():
            url = self.main.gptsovitsw.api_url.text()
            extra = self.main.gptsovitsw.extra.text()
            role = self.main.gptsovitsw.role.toPlainText().strip()

            self.main.settings.setValue("gptsovits_role", role)
            self.main.settings.setValue("gptsovits_url", url)
            self.main.settings.setValue("gptsovits_extra", extra if extra else "pyvideotrans")

            config.params["gptsovits_url"] = url
            config.params["gptsovits_extra"] = extra
            config.params["gptsovits_role"] = role

            self.main.gptsovitsw.close()

        from videotrans.component import GPTSoVITSForm
        self.main.gptsovitsw = GPTSoVITSForm()
        if config.params["gptsovits_url"]:
            self.main.gptsovitsw.api_url.setText(config.params["gptsovits_url"])
        if config.params["gptsovits_extra"]:
            self.main.gptsovitsw.extra.setText(config.params["gptsovits_extra"])
        if config.params["gptsovits_role"]:
            self.main.gptsovitsw.role.setPlainText(config.params["gptsovits_role"])

        self.main.gptsovitsw.save.clicked.connect(save)
        self.main.gptsovitsw.test.clicked.connect(test)
        self.main.gptsovitsw.show()

    def set_gemini_key(self):
        def save():
            key = self.main.w.gemini_key.text()
            template = self.main.w.gemini_template.toPlainText()
            self.main.settings.setValue("gemini_key", key)
            self.main.settings.setValue("gemini_template", template)

            os.environ['GOOGLE_API_KEY'] = key
            config.params["gemini_key"] = key
            config.params["gemini_template"] = template
            self.main.w.close()

        from videotrans.component import GeminiForm
        self.main.w = GeminiForm()
        if config.params["gemini_key"]:
            self.main.w.gemini_key.setText(config.params["gemini_key"])
        if config.params["gemini_template"]:
            self.main.w.gemini_template.setPlainText(config.params["gemini_template"])
        self.main.w.set_gemini.clicked.connect(save)
        self.main.w.show()

    def set_azure_key(self):
        def save():
            key = self.main.w.azure_key.text()
            api = self.main.w.azure_api.text()
            model = self.main.w.azure_model.currentText()
            template = self.main.w.azure_template.toPlainText()
            self.main.settings.setValue("azure_key", key)
            self.main.settings.setValue("azure_api", api)

            self.main.settings.setValue("azure_model", model)
            self.main.settings.setValue("azure_template", template)

            config.params["azure_key"] = key
            config.params["azure_api"] = api
            config.params["azure_model"] = model
            config.params["azure_template"] = template
            self.main.w.close()

        from videotrans.component import AzureForm
        self.main.w = AzureForm()
        if config.params["azure_key"]:
            self.main.w.azure_key.setText(config.params["azure_key"])
        if config.params["azure_api"]:
            self.main.w.azure_api.setText(config.params["azure_api"])
        if config.params["azure_model"]:
            self.main.w.azure_model.setCurrentText(config.params["azure_model"])
        if config.params["azure_template"]:
            self.main.w.azure_template.setPlainText(config.params["azure_template"])
        self.main.w.set_azure.clicked.connect(save)
        self.main.w.show()
