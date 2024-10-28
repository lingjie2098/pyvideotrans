# run again.  Do not edit this file unless you know what you are doing.

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import (QMetaObject, Qt)

from videotrans.configure import config
from videotrans.configure.config import box_lang


class Ui_fanyisrt(object):
    def setupUi(self, fanyisrt):
        self.has_done = False
        if not fanyisrt.objectName():
            fanyisrt.setObjectName(u"fanyisrt")
        fanyisrt.resize(1150, 535)
        fanyisrt.setWindowModality(QtCore.Qt.NonModal)

        self.files = []
        self.error_msg = ""

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(fanyisrt.sizePolicy().hasHeightForWidth())
        fanyisrt.setSizePolicy(sizePolicy)

        # start
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(fanyisrt)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")

        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")

        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")

        self.label_13 = QtWidgets.QLabel()
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_18.addWidget(self.label_13)

        self.fanyi_translate_type = QtWidgets.QComboBox()
        self.fanyi_translate_type.setMinimumSize(QtCore.QSize(100, 30))
        self.fanyi_translate_type.setObjectName("fanyi_translate_type")

        self.aisendsrt=QtWidgets.QCheckBox()
        self.aisendsrt.setText('发送完整字幕' if config.defaulelang=='zh' else 'Send full subtitles')
        self.aisendsrt.setToolTip('当使用AI或Google翻译渠道时，可选以完整srt字幕格式发送请求，但可能出现较多空行' if config.defaulelang=='zh' else 'When using AI or Google translation channel, you can translate in srt format, but there may be more empty lines')
        self.aisendsrt.setChecked(config.settings.get('aisendsrt'))

        self.fanyi_model_list = QtWidgets.QComboBox()
        self.fanyi_model_list.setMinimumSize(QtCore.QSize(100, 30))
        self.fanyi_model_list.setObjectName("fanyi_model_list")
        self.fanyi_model_list.setVisible(False)



        self.horizontalLayout_18.addWidget(self.fanyi_translate_type)
        self.horizontalLayout_18.addWidget(self.aisendsrt)
        self.horizontalLayout_18.addWidget(self.fanyi_model_list)

        self.label_source = QtWidgets.QLabel()
        self.label_source.setMinimumSize(QtCore.QSize(0, 30))
        self.fanyi_source = QtWidgets.QComboBox()
        self.fanyi_source.setMinimumSize(QtCore.QSize(120, 30))

        self.horizontalLayout_18.addWidget(self.label_source)
        self.horizontalLayout_18.addWidget(self.fanyi_source)

        self.label_613 = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_613.sizePolicy().hasHeightForWidth())
        self.label_613.setSizePolicy(sizePolicy)
        self.label_613.setMinimumSize(QtCore.QSize(0, 30))
        self.label_613.setObjectName("label_613")
        self.horizontalLayout_18.addWidget(self.label_613)

        self.fanyi_target = QtWidgets.QComboBox()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fanyi_target.sizePolicy().hasHeightForWidth())
        self.fanyi_target.setSizePolicy(sizePolicy)
        self.fanyi_target.setMinimumSize(QtCore.QSize(120, 30))
        self.fanyi_target.setObjectName("fanyi_target")
        self.horizontalLayout_18.addWidget(self.fanyi_target)

        self.out_format = QtWidgets.QComboBox()

        self.out_format.addItems([
            "单语字幕" if config.defaulelang == 'zh' else 'Monolingual subtitles',
            "目标语言在上(双语)" if config.defaulelang == 'zh' else 'Target language up(Bilingual)',
            "目标语言在下(双语)" if config.defaulelang == 'zh' else 'Target language under(Bilingual)'
        ])



        label_out = QtWidgets.QLabel()
        label_out.setText('输出' if config.defaulelang == 'zh' else 'Output')
        # label_out.setFixedWidth(60)
        self.horizontalLayout_18.addWidget(label_out)
        self.horizontalLayout_18.addWidget(self.out_format)

        self.label_614 = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_614.sizePolicy().hasHeightForWidth())
        self.label_614.setSizePolicy(sizePolicy)
        self.label_614.setMinimumSize(QtCore.QSize(0, 30))
        self.label_614.setObjectName("label_614")
        self.horizontalLayout_18.addWidget(self.label_614)

        self.fanyi_proxy = QtWidgets.QLineEdit()
        self.fanyi_proxy.setMinimumSize(QtCore.QSize(0, 30))
        self.fanyi_proxy.setObjectName("fanyi_proxy")
        self.horizontalLayout_18.addWidget(self.fanyi_proxy)

        self.verticalLayout_13.addLayout(self.horizontalLayout_18)

        self.loglabel = QtWidgets.QPushButton()
        self.loglabel.setStyleSheet('''color:#148cd2;background-color:transparent''')
        self.verticalLayout_13.addWidget(self.loglabel)

        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setContentsMargins(-1, 20, -1, -1)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.fanyi_import = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        sizePolicy.setHeightForWidth(self.fanyi_import.sizePolicy().hasHeightForWidth())
        self.fanyi_import.setSizePolicy(sizePolicy)
        self.fanyi_import.setMinimumSize(QtCore.QSize(200, 30))
        self.fanyi_import.setObjectName("fanyi_import")
        self.fanyi_import.setCursor(Qt.PointingHandCursor)

        self.horizontalLayout_19.addWidget(self.fanyi_import)
        self.daochu = QtWidgets.QToolButton()
        self.daochu.setMinimumSize(QtCore.QSize(0, 28))
        self.daochu.setObjectName("daochu")
        self.daochu.setCursor(Qt.PointingHandCursor)
        self.horizontalLayout_19.addStretch()
        self.horizontalLayout_19.addWidget(self.daochu)
        self.verticalLayout_13.addLayout(self.horizontalLayout_19)

        self.fanyi_layout = QtWidgets.QHBoxLayout()
        self.fanyi_layout.setObjectName("fanyi_layout")


        self.fanyi_start = QtWidgets.QPushButton()
        self.fanyi_start.setMinimumSize(QtCore.QSize(120, 30))
        self.fanyi_start.setObjectName("fanyi_start")
        self.fanyi_start.setCursor(Qt.PointingHandCursor)

        self.fanyi_stop = QtWidgets.QPushButton()
        self.fanyi_stop.setMinimumSize(QtCore.QSize(120, 25))
        self.fanyi_stop.setObjectName("fanyi_stop")
        self.fanyi_stop.setDisabled(True)
        self.fanyi_stop.setCursor(Qt.PointingHandCursor)
        self.fanyi_stop.setText("停止" if config.defaulelang=='zh' else 'Stop')

        v1=QtWidgets.QVBoxLayout()
        v1.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)
        v1.addWidget(self.fanyi_start)
        v1.addWidget(self.fanyi_stop)


        self.fanyi_layout.addLayout(v1)
        self.fanyi_targettext = QtWidgets.QPlainTextEdit()
        self.fanyi_targettext.setObjectName("fanyi_targettext")
        self.fanyi_targettext.setReadOnly(True)
        self.fanyi_layout.addWidget(self.fanyi_targettext)
        self.verticalLayout_13.addLayout(self.fanyi_layout)
        self.reslabel = QtWidgets.QLabel()

        self.verticalLayout_13.addWidget(self.reslabel)

        self.horizontalLayout_23.addLayout(self.verticalLayout_13)

        # end

        self.retranslateUi(fanyisrt)

        QMetaObject.connectSlotsByName(fanyisrt)

    # setupUi

    def retranslateUi(self, fanyisrt):
        fanyisrt.setWindowTitle(config.uilanglist.get("Text  Or Srt  Translation"))
        self.label_13.setText('翻译渠道' if config.defaulelang=='zh' else "Translation channels")
        self.label_613.setText(box_lang.get("Target lang"))
        self.label_source.setText('原语言' if config.defaulelang == 'zh' else 'Source language')
        self.label_614.setText('网络代理' if config.defaulelang=='zh' else 'Proxy')
        self.fanyi_proxy.setPlaceholderText(
            box_lang.get("Failed to access Google services. Please set up the proxy correctly"))
        self.fanyi_import.setText(box_lang.get("Import text to be translated from a file.."))
        self.daochu.setText(config.transobj['dakaizimubaocunmulu'])
        self.fanyi_start.setText(box_lang.get("Start>"))
        self.fanyi_targettext.setPlaceholderText(box_lang.get("The translation result is displayed here"))
