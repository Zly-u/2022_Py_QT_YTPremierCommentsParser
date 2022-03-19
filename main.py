import json
import sys, os
from random import uniform
from urllib import request
import re


from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont


avatar_placehokders = os.listdir("avyPlaceholders")
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)

        self.resize(460, 1000)
        self.setWindowTitle("YT Premierka Commentka 0_0")

        #App's Main Layout
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.comments: list = []

        self.prepare()
        self.setupUI()

    def parseJSON(self, file_name):
        temp_json = None
        with open(file_name, "r", encoding="utf-8") as comments:
            # for line in comments.readlines():
            temp_json = json.load(comments)

        new_json = []
        for i, comment in enumerate(temp_json["comments"]):
            user_action = comment["replayChatItemAction"]["actions"][0]
            user_item   = user_action.get("addChatItemAction", None)                    # if none - It's a deleted message

            if user_item:
                user_info   = user_item["item"].get("liveChatTextMessageRenderer", None)    # if none - it's a system message
                if not user_info: continue

                found_messag = user_info["message"]["runs"][0].get("text", None)
                if not found_messag and len(user_info["message"]["runs"]) > 1:
                    for element in user_info["message"]["runs"][1:]:
                        found_messag = element.get("text", None)
                        if found_messag: break

                if not found_messag: continue

                new_json.append(
                    {
                        "author_name": user_info["authorName"]["simpleText"],
                        "message": found_messag,
                        "avatar": user_info["authorPhoto"]["thumbnails"][1]["url"]
                    }
                )
            else:
                new_json.append(
                    {
                        "author_name": None,
                        "message": user_action["markChatItemAsDeletedAction"]["deletedStateMessage"]["runs"][0]["text"],
                        "avatar": None
                    }
                )

        return new_json

    def prepare(self):
        self.comments = self.parseJSON("test.json")
        # print(self.comments)

    def setupUI(self):
        if "scroll_area":
            scrollArea_MAIN_WidgetContents = QtWidgets.QWidget()

            # Setting up the Layout of the Scroll Area
            scroll_area = QtWidgets.QScrollArea(self.central_widget)
            scroll_area.setWidget(scrollArea_MAIN_WidgetContents)
            scroll_area_VB = QtWidgets.QVBoxLayout(scrollArea_MAIN_WidgetContents)
            scroll_area_VB.setAlignment(Qt.AlignTop)
            scroll_area.setWidgetResizable(True)

            # Setting up the style of the Scroll Area
            scroll_area.setFrameShape(QtWidgets.QFrame.Panel)
            scroll_area.setFrameShadow(QtWidgets.QFrame.Raised)
            scroll_area.setLineWidth(2)

            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

            #Create each comment
            for comment in self.comments:
                frame_commentItem = QtWidgets.QFrame(scrollArea_MAIN_WidgetContents)
                frame_layout = QtWidgets.QVBoxLayout(frame_commentItem)
                frame_commentItem.setLayout(frame_layout)

                frame_commentItem.setFrameShape(QtWidgets.QFrame.Panel)
                frame_commentItem.setFrameShadow(QtWidgets.QFrame.Sunken)
                frame_commentItem.setLineWidth(2)

                frame_commentItem.setFixedHeight(120)
                frame_commentItem.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

                # Name
                label_name = QtWidgets.QLabel(frame_commentItem)
                label_name.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                label_name_font = QFont("Roboto")
                label_name_font.setPixelSize(24)
                label_name.setFont(label_name_font)

                frame_ac_HB = QtWidgets.QHBoxLayout(frame_commentItem)
                frame_ac_HB.setSpacing(5)
                if "avy comment layout":
                    # Frame for avy
                    frame_commentItem_avatar = QtWidgets.QFrame(frame_commentItem)
                    frame_commentItem_avatar.setFrameShape(QtWidgets.QFrame.Panel)
                    frame_commentItem_avatar.setFrameShadow(QtWidgets.QFrame.Plain)
                    frame_commentItem_avatar.setLineWidth(3)
                    frame_commentItem_avatar.setFixedSize(64, 64)

                    frame_commentItem_avatar_VB = QtWidgets.QVBoxLayout(frame_commentItem_avatar)
                    frame_commentItem_avatar.setLayout(frame_commentItem_avatar_VB)
                    frame_commentItem_avatar_VB.setContentsMargins(0,0,0,0)

                    # Avatar Frame
                    avy_url = comment.get("avatar", None)
                    avy_label_image = QtWidgets.QLabel(frame_commentItem_avatar)
                    avy_label_image.setText("Avy")
                    avy_label_image.setScaledContents(True)
                    author_name = None
                    if avy_url:
                        avy_req     = request.Request(avy_url)
                        avy_img_raw = request.urlopen(avy_req).read()
                        avy_img = QPixmap()
                        avy_img.loadFromData(avy_img_raw)

                        avy_label_image.setPixmap(avy_img)
                        avy_label_image.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                        avy_label_image.setFixedSize(64-6, 64-6)

                        author_name = comment["author_name"]
                    else:
                        place_holder_avy = avatar_placehokders[int(uniform(0, len(avatar_placehokders)-1))]
                        avy_img = QPixmap("avyPlaceholders/"+place_holder_avy)

                        avy_label_image.setPixmap(avy_img)
                        avy_label_image.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
                        avy_label_image.setFixedSize(64 - 6, 64 - 6)

                        author_name = re.match("(\w+).\w+$", place_holder_avy).group(1)

                    frame_commentItem_avatar_VB.addWidget(avy_label_image)

                    frame_ac_HB.addWidget(frame_commentItem_avatar)

                    label_name.setText(author_name)

                    # Comment Label
                    label_comment_font = QFont("Roboto")
                    label_comment_font.setPixelSize(16)
                    label_comment = QtWidgets.QLabel(frame_commentItem)
                    label_comment.setFont(label_comment_font)
                    label_comment.setText(comment["message"])
                    label_comment.setWordWrap(True)

                    frame_ac_HB.addWidget(label_comment)

                frame_layout.addWidget(label_name)
                frame_layout.addItem(frame_ac_HB)
                scroll_area_VB.addWidget(frame_commentItem)

        self.main_layout.addWidget(scroll_area)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()

    status = app.exec_()
    sys.exit(status)

main()








































