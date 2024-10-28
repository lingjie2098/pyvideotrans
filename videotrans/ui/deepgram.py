# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPlainTextEdit

from videotrans.configure import config
from videotrans.util import tools


class Ui_deepgramform(object):
    def setupUi(self, deepgramform):
        self.has_done = False
        deepgramform.setObjectName("deepgramform")
        deepgramform.setWindowModality(QtCore.Qt.NonModal)
        deepgramform.resize(500, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(deepgramform.sizePolicy().hasHeightForWidth())
        deepgramform.setSizePolicy(sizePolicy)

        self.verticalLayout = QtWidgets.QVBoxLayout(deepgramform)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.formLayout_2.setObjectName("formLayout_2")

        # api key
        self.label_apikey = QtWidgets.QLabel(deepgramform)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_apikey.sizePolicy().hasHeightForWidth())
        self.label_apikey.setSizePolicy(sizePolicy)
        self.label_apikey.setMinimumSize(QtCore.QSize(100, 35))
        self.label_apikey.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_apikey.setObjectName("label_apikey")
        self.label_apikey.setText('API KEY ')

        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_apikey)
        self.apikey = QtWidgets.QLineEdit(deepgramform)
        self.apikey.setMinimumSize(QtCore.QSize(0, 35))
        self.apikey.setObjectName("apikey")

        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.apikey)
        self.verticalLayout.addLayout(self.formLayout_2)

        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.formLayout_3.setFormAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_utt = QtWidgets.QLabel(deepgramform)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_utt.sizePolicy().hasHeightForWidth())
        self.label_utt.setSizePolicy(sizePolicy)
        self.label_utt.setMinimumSize(QtCore.QSize(100, 35))
        self.label_utt.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_utt.setObjectName("label")
        self.label_utt.setText('静默时间长度/毫秒')

        self.utt = QtWidgets.QLineEdit(deepgramform)
        self.utt.setMinimumSize(QtCore.QSize(0, 35))
        self.utt.setObjectName("utt")

        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_utt)
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.utt)

        self.verticalLayout.addLayout(self.formLayout_3)

        self.label_model = QtWidgets.QLabel(deepgramform)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_model.sizePolicy().hasHeightForWidth())
        self.label_model.setSizePolicy(sizePolicy)
        self.label_model.setMinimumSize(QtCore.QSize(100, 35))
        self.label_model.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_model.setObjectName("label")
        self.label_model.setText('识别模型')

        self.model = QtWidgets.QComboBox(deepgramform)
        self.model.addItems([
            "whisper-large",
            "whisper-medium",
            "whisper-small",
            "whisper-base",
            "whisper-tiny",
            "nova-2-general",
            "enhanced-2-general",
            "base-2-general",

        ])
        self.model.setObjectName("model")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.formLayout_4.setFormAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.formLayout_4.setObjectName("formLayout_4")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_model)
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.model)

        self.verticalLayout.addLayout(self.formLayout_4)



        self.set = QtWidgets.QPushButton(deepgramform)
        self.set.setMinimumSize(QtCore.QSize(0, 35))
        self.set.setObjectName("set")

        self.test = QtWidgets.QPushButton(deepgramform)
        self.test.setMinimumSize(QtCore.QSize(0, 30))
        self.test.setObjectName("test")

        help_btn = QtWidgets.QPushButton()
        help_btn.setMinimumSize(QtCore.QSize(0, 35))
        help_btn.setStyleSheet("background-color: rgba(255, 255, 255,0)")
        help_btn.setObjectName("help_btn")
        help_btn.setCursor(Qt.PointingHandCursor)
        help_btn.setText("查看填写教程" if config.defaulelang == 'zh' else "Fill out the tutorial")
        help_btn.clicked.connect(lambda: tools.open_url(url='https://pyvideotrans.com/deepgram'))


        self.layout_btn = QtWidgets.QHBoxLayout()
        self.layout_btn.setObjectName("layout_btn")


        self.layout_btn.addWidget(self.set)
        self.layout_btn.addWidget(self.test)
        self.layout_btn.addWidget(help_btn)

        self.verticalLayout.addLayout(self.layout_btn)

        self.retranslateUi(deepgramform)
        QtCore.QMetaObject.connectSlotsByName(deepgramform)

    def retranslateUi(self, deepgramform):
        deepgramform.setWindowTitle("Deepgram语音识别" if config.defaulelang == 'zh' else 'Deepgram Speech Recognition')

        self.label_apikey.setText('API Key')
        self.label_utt.setText('静默时长/毫秒' if config.defaulelang == 'zh' else 'silence between words/ms')

        self.label_model.setText('识别模型' if config.defaulelang == 'zh' else 'Select Model')
        self.set.setText('保存' if config.defaulelang == 'zh' else 'Save')
        self.test.setText('测试' if config.defaulelang == 'zh' else 'Test')
