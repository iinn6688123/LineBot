from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message, send_carousel_message
from linebot.models import URITemplateAction, MessageTemplateAction, ImageCarouselColumn, TextSendMessage

from bs4 import BeautifulSoup
import requests
fest = ""
pre = -1
cur = -1
pretmp = -1
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_start(self, event):
        global pre
        text = event.message.text
        if text.lower() == "start":
            return True
        if pre == 0 and text == "返回":
            return True
        return False

    def on_enter_start(self, event):
        global pre,cur
        pre = -1
        cur = 0
        title = "傳統節日"
        text = "了解台灣傳統節日，認識在地文化。\n輸入「總覽」可看到台灣主要傳統節日名稱與日期\n輸入「查詢」可查詢特定節日"
        btn = [
            MessageTemplateAction(
                label = "總覽",
                text = "總覽"
            ),
            MessageTemplateAction(
                label = "查詢",
                text = "查詢"
            ),
        ]
        url = "https://img.juzimo.com/20200806/8653660560325246976.jpg"
        reply_token = event.reply_token
        send_button_message(reply_token, title, text, btn, url)

    def is_going_to_overview(self, event):
        global cur,pre
        text = event.message.text
        if text == "總覽":
            return True
        if pre == 1 and text == "返回":
            cur = 0
            return True
        return False #text.lower() == "overview"

    def is_going_to_search(self, event):
        global cur,pre
        text = event.message.text
        if text == "查詢":
            return True
        if pre == 2 and text == "返回":
            cur = 0
            return True
        return False # text.lower() == "search"

    def on_enter_overview(self, event):
        global pre,cur
        pre = cur
        cur = 1
        print("I'm entering overview")
        emoji = [
            {
                "index": 0,
                "productId": "5ac2213e040ab15980c9b447",
                "emojiId": "037"
            },
            {
                "index": 8,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "141"
            },
            {
                "index": 10,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053"
            },
            {
                "index": 23,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054"
            },
            {
                "index": 38,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055"
            },
            {
                "index": 55,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056"
            },
            {
                "index": 69,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "057"
            },
            {
                "index": 82,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "058"
            },
            {
                "index": 97,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "059"
            },
            {
                "index": 112,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "060"
            },
            {
                "index": 126,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "061"
            },
            {
                "index": 146,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "142"
            },
            {
                "index": 174,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "142"
            },
        ]
        msg = "$ 傳統節日總覽$\n$ 春節(農曆1月1日)\n$ 元宵節(農曆1月15日)\n$ 清明節(國曆4月4日或5日)\n$ 端午節(農曆5月5日)\n$ 七夕(農曆7月7日)\n$ 中元節(農曆7月15日)\n$ 中秋節(農曆8月15日)\n$ 重陽節(農曆9月9日)\n$ 冬至(國曆12月21日或22日)\n\n$輸入節日名稱或日期以了解更多，如「春節」或「1/1」\n$輸入「返回」回到主選單"
        #send_message = [msg1, msg2]
        reply_token = event.reply_token
        send_text_message(reply_token, msg, emoji)
        #self.go_back()

    def on_enter_search(self, event):
        global pre,cur
        pre = cur
        cur = 2
        print("I'm entering search")
        emoji = [
            {
                "index": 12,
                "productId": "5ac21a18040ab15980c9b43e",
                "emojiId": "111" # before example
            },
            {
                "index": 14,
                "productId": "5ac21a18040ab15980c9b43e",
                "emojiId": "048" 
            },
            {
                "index": 28,
                "productId": "5ac21b4f031a6752fb806d59",
                "emojiId": "107" # before example
            },
            {
                "index": 35,
                "productId": "5ac21b4f031a6752fb806d59",
                "emojiId": "107" 
            },
            {
                "index": 43,
                "productId": "5ac21b4f031a6752fb806d59",
                "emojiId": "142" # before example
            },
        ]
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入要查詢的節日或日期$\n$注意確認輸入格式是否正確\n$如「春節」\n$如「1/1」\n$輸入「返回」回到主選單", emoji)
        #self.go_back()

    def is_going_to_Festival(self, event):  #********改成所有festival
        global fest,pretmp,cur,pre
        text = event.message.text
        if text == "春節" or text == "元宵節"or text == "清明節"or text == "端午節"or text == "七夕"or text == "中元節"or text == "中秋節"or text == "重陽節"or text == "冬至":
            fest = text
            return True
        if text == "1/1": #or text == "1/15"
            fest = "春節"
            return True
        elif text == "1/15":
            fest = "元宵節"
            return True
        elif text == "4/4" or text == "4/5":
            fest = "清明節"
            return True
        elif text == "5/5":
            fest = "端午節"
            return True
        elif text == "7/7":
            fest = "七夕"
            return True
        elif text == "7/15":
            fest = "中元節"
            return True
        elif text == "8/15":
            fest = "中秋節"
            return True
        elif text == "9/9":
            fest = "重陽節"
            return True
        elif text == "12/21" or text == "12/22":
            fest = "冬至"
            return True
        if pre == 3 and text == "返回": ###
            cur = pretmp
            return True
        return False

    def on_enter_Festival(self, event):
        global pre,cur,pretmp
        pre = cur
        cur = 3
        pretmp = pre
        global fest
        print("I'm entering Festival")
        if fest == "春節":
            title = "春節 (農曆1月1日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://pic.pimg.tw/john547/1579741219-3918908498_wn.jpg"
        elif fest == "元宵節":
            title = "元宵節 (農曆1月15日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://cdn2.ettoday.net/images/4687/4687999.jpg"
        elif fest == "清明節":
            title = "清明節 (國曆4月4日或5日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://image.cache.storm.mg/styles/smg-800x533-fp/s3/media/image/2018/04/03/20180403-102217_U10931_M398442_879b.jpg"
        elif fest == "端午節":
            title = "端午節 (農曆5月5日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://attach.setn.com/newsimages/2018/06/14/1402129-PH.jpg"
        elif fest == "七夕":
            title = "七夕 (農曆7月7日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://images.lnka.tw/images/16x9/20200825084506407.jpg"
        elif fest == "中元節":
            title = "中元節 (農曆7月15日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://cdn.mamaclub.com/wp-content/uploads/2020/08/0826renee0359-1024x724.jpg"
        elif fest == "中秋節":
            title = "中秋節 (農曆8月15日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://media.istockphoto.com/vectors/happy-midautumn-festival-vector-id1170415124?k=20&m=1170415124&s=612x612&w=0&h=yZg33rVEzlo91WoEKYDfEsAC1ZCJS7kyi_OGHI5eXuE="
        elif fest == "重陽節":
            title = "重陽節 (農曆9月9日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://i3.lhysg.com/3cf0a0/31f9f00914dea8df1a10172d93.jpg"
        elif fest == "冬至":
            title = "冬至 (國曆12月21日或22日)"
            text = "輸入或選擇想要的操作"
            btn = [
                MessageTemplateAction(
                    label = "介紹",
                    text = "介紹"
                ),
                MessageTemplateAction(
                    label = "習俗",
                    text = "習俗"
                ),
                MessageTemplateAction(
                    label = "更多相關影片",
                    text = "更多相關影片"
                ),
                MessageTemplateAction(
                    label = "返回",
                    text = "返回"
                ),
            ]
            url = "https://www.travelliker.com.hk/img/upload/img/1-294.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, title, text, btn, url)

    def is_going_to_intro(self, event): #**********
        text = event.message.text
        if text == "介紹":
            return True
        return False

    def on_enter_intro(self, event):
        global pre,cur
        pre = cur
        global fest
        print("I'm entering intro")
        if fest == "春節":
            f = open("src/intro/intro1.txt", "r")
            message = f.read()
            f.close()
        elif fest == "元宵節":
            f = open("src/intro/intro2.txt", "r")
            message = f.read()
            f.close()
        elif fest == "清明節":
            f = open("src/intro/intro3.txt", "r")
            message = f.read()
            f.close()
        elif fest == "端午節":
            f = open("src/intro/intro4.txt", "r")
            message = f.read()
            f.close()
        elif fest == "七夕":
            f = open("src/intro/intro5.txt", "r")
            message = f.read()
            f.close()
        elif fest == "中元節":
            f = open("src/intro/intro6.txt", "r")
            message = f.read()
            f.close()
        elif fest == "中秋節":
            f = open("src/intro/intro7.txt", "r")
            message = f.read()
            f.close()
        elif fest == "重陽節":
            f = open("src/intro/intro8.txt", "r")
            message = f.read()
            f.close()
        elif fest == "冬至":
            f = open("src/intro/intro9.txt", "r")
            message = f.read()
            f.close()
        reply_token = event.reply_token
        send_text_message(reply_token, message, None)
        #self.go_back(event)

    def is_going_to_custom(self, event): #**********
        text = event.message.text
        if text == "習俗":
            return True
        return False

    def on_enter_custom(self, event):
        global pre,cur
        pre = cur
        global fest
        print("I'm entering custom")
        emoji1 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 5,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 10,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 15,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
            {
                "index": 20,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "057" # before example
            },
            {
                "index": 24,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "058" # before example
            },
            {
                "index": 29,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "059" # before example
            },
        ]
        emoji2 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 5,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 10,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 15,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
            {
                "index": 19,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "057" # before example
            },
            {
                "index": 24,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "058" # before example
            },
        ]
        emoji3 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 4,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 8,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 12,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
        ]
        emoji4 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 4,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 9,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 14,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
            {
                "index": 19,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "057" # before example
            },
        ]
        emoji5 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 4,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 8,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 13,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
            {
                "index": 18,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "057" # before example
            },
        ]
        emoji6 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 6,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 10,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 15,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
        ]
        emoji7 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 4,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 9,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 14,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
        ]
        emoji8 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
            {
                "index": 6,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "054" # before example
            },
            {
                "index": 15,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "055" # before example
            },
            {
                "index": 21,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "056" # before example
            },
            {
                "index": 27,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "057" # before example
            },
            {
                "index": 32,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "058" # before example
            },
        ]
        emoji9 = [
            {
                "index": 0,
                "productId": "5ac21ae3040ab15980c9b440",
                "emojiId": "053" # before example
            },
        ]
        if fest == "春節":
            message = "$大掃除\n$貼春聯\n$掛燈籠\n$放鞭炮\n$拜年\n$發紅包\n$舞龍舞獅"
            emoji = emoji1
        elif fest == "元宵節":
            message = "$點天燈\n$燃蜂炮\n$炸邯鄲\n$乞龜\n$猜燈謎\n$鬧花燈"
            emoji = emoji2
        elif fest == "清明節":
            # 5ac2216f040ab15980c9b448 133 / 
            message = "$掃墓\n$踏青\n$寒食\n$插柳戴柳"
            emoji = emoji3
        elif fest == "端午節":
            message = "$立蛋\n$吃粽子\n$划龍舟\n$掛艾草\n$戴香包"
            emoji = emoji4
        elif fest == "七夕":
            message = "$乞巧\n$祈願\n$拜織女\n$吃巧果\n$染指甲"
            emoji = emoji5
        elif fest == "中元節":
            message = "$中元普渡\n$搶孤\n$放水燈\n$跳鍾馗"
            emoji = emoji6
        elif fest == "中秋節":
            message = "$賞月\n$吃月餅\n$吃柚子\n$烤肉"
            emoji = emoji7
        elif fest == "重陽節":
            message = "$佩帶茱萸\n$賞菊、飲菊花酒\n$吃重陽糕\n$登高郊遊\n$放風箏\n$敬老活動"
            emoji = emoji8
        elif fest == "冬至":
            message = "$吃湯圓"
            emoji = emoji9
        reply_token = event.reply_token
        send_text_message(reply_token, message,emoji)

    def is_going_to_video(self, event): #**********
        text = event.message.text
        if text == "更多相關影片":
            return True
        return False

    def on_enter_video(self, event): ###
        global pre,cur
        pre = cur
        global fest
        print("I'm entering video")
        url_list = []
        img_list = []
        label_list = []
        if(fest == "春節"):
            url_list.append("https://www.youtube.com/watch?v=DwNV7dlamIk")
            url_list.append("https://www.youtube.com/watch?v=zvYw_QkeQRI")
            url_list.append("https://www.youtube.com/watch?v=iD5mdjR_tNU")
            img_list.append("https://i.ytimg.com/vi/DwNV7dlamIk/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBIri6adDZJvUPB8CN7X-1hXhyt_w")
            img_list.append("https://i.ytimg.com/vi/zvYw_QkeQRI/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAeAgra1EZvpswMHtJkkgUNdB_QrQ")
            img_list.append("https://i.ytimg.com/an_webp/iD5mdjR_tNU/mqdefault_6s.webp?du=3000&sqp=CISpp44G&rs=AOn4CLBOyqwaWIuQUovvrX4ig51f1_62Uw")
            label_list.append("過年習俗的有趣之處？")
            label_list.append("春節習俗")
            label_list.append("臺灣節日習俗的冷知識!")
        elif(fest == "元宵節"):
            url_list.append("https://www.youtube.com/watch?v=2pRhuoJ6k_U")
            url_list.append("https://www.youtube.com/watch?v=Ij6nxAk25jc&ab_channel=HD.Club.tw")
            url_list.append("https://www.youtube.com/watch?v=osoMn7UtlQg")
            img_list.append("https://i.ytimg.com/vi/2pRhuoJ6k_U/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLAq7L1gnMoLmVwOa2-h_5iPLq5Tgg")
            img_list.append("https://i.ytimg.com/vi/Ij6nxAk25jc/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBfPVDshiM8nwopzk5Ba3h18ArmSA")
            img_list.append("https://i.ytimg.com/an_webp/osoMn7UtlQg/mqdefault_6s.webp?du=3000&sqp=CNiArI4G&rs=AOn4CLDrx8frvu3fYHOGepEylGlgC3y6TA")
            label_list.append("為什麼會有元宵節呢？")
            label_list.append("台灣元宵禮讚(2009)")
            label_list.append("元宵節由來")
        elif(fest == "清明節"):
            url_list.append("https://www.youtube.com/watch?app=desktop&v=IeioyzDCBEk")
            url_list.append("https://m.youtube.com/watch?v=3GfjjyZI79I")
            url_list.append("https://m.youtube.com/watch?v=6ZUZvIVCIvs")
            img_list.append("https://i.ytimg.com/vi_webp/IeioyzDCBEk/mqdefault.webp")
            img_list.append("https://i.ytimg.com/vi_webp/3GfjjyZI79I/mqdefault.webp")
            img_list.append("https://i.ytimg.com/vi_webp/6ZUZvIVCIvs/mqdefault.webp")
            label_list.append("台灣掃墓習俗")
            label_list.append("清明節一起掃墓、吃潤餅")
            label_list.append("清明節的由來")
        elif(fest == "端午節"):
            url_list.append("https://www.youtube.com/watch?v=ZOz8GFV2ByU")
            url_list.append("https://www.youtube.com/watch?v=aIOd7jUIsns")
            url_list.append("https://www.youtube.com/watch?v=C9EnbUKLJn4")
            img_list.append("https://i.ytimg.com/an_webp/ZOz8GFV2ByU/mqdefault_6s.webp?du=3000&sqp=CKD4q44G&rs=AOn4CLBKfz2bfBHx36KBbSfIley2a3ZsUg")
            img_list.append("https://i.ytimg.com/an_webp/aIOd7jUIsns/mqdefault_6s.webp?du=3000&sqp=COTIq44G&rs=AOn4CLBDlCrcIEZUxWI5zxDKrjIDDDapaQ")
            img_list.append("https://i.ytimg.com/an_webp/C9EnbUKLJn4/mqdefault_6s.webp?du=3000&sqp=CJzpq44G&rs=AOn4CLDLQLrklGjMt_VmJTobfOFNsrL-2A")
            label_list.append("端午節的故事")
            label_list.append("為什麼要吃粽子、划龍舟？")
            label_list.append("白素貞跟許仙的故事")
        elif(fest == "七夕"):
            url_list.append("https://m.youtube.com/watch?v=HHcyNSr8nPU")
            url_list.append("https://m.youtube.com/watch?v=pU-7zPAaDfc")
            url_list.append("https://m.youtube.com/watch?v=wO4CDiCvYjU")
            img_list.append("https://i.ytimg.com/vi_webp/HHcyNSr8nPU/mqdefault.webp")
            img_list.append("https://i.ytimg.com/vi/pU-7zPAaDfc/mqdefault.jpg")
            img_list.append("https://i.ytimg.com/vi_webp/wO4CDiCvYjU/mqdefault.webp")
            label_list.append("牛郎與織女")
            label_list.append("七夕情人節的由來與習俗")
            label_list.append("牛郎與織女一年一會的故事")
        elif(fest == "中元節"):
            url_list.append("https://m.youtube.com/watch?v=THaqTjCH_t0")
            url_list.append("https://m.youtube.com/watch?v=8aJgDwsV3y8")
            url_list.append("https://m.youtube.com/watch?v=_HB8UE-6HI0")
            img_list.append("https://i.ytimg.com/vi_webp/THaqTjCH_t0/mqdefault.webp")
            img_list.append("https://i.ytimg.com/vi/8aJgDwsV3y8/mqdefault.jpg")
            img_list.append("https://i.ytimg.com/vi_webp/_HB8UE-6HI0/mqdefault.webp")
            label_list.append("中元節普渡拜拜有典故")
            label_list.append("雞籠中元祭重點全紀錄")
            label_list.append("地官大帝─「舜」的故事")
        elif(fest == "中秋節"):
            url_list.append("https://www.youtube.com/watch?v=z1nPSp5Jm0I")
            url_list.append("https://www.youtube.com/watch?v=l2RKMqrEKSU")
            url_list.append("https://www.youtube.com/watch?v=58BmnalsQ9I")
            img_list.append("https://i.ytimg.com/an_webp/z1nPSp5Jm0I/mqdefault_6s.webp?du=3000&sqp=CKjiq44G&rs=AOn4CLAZ4bjMWNMDd63-EsOC6ckn9rSOdg")
            img_list.append("https://i.ytimg.com/an_webp/l2RKMqrEKSU/mqdefault_6s.webp?du=3000&sqp=CJbtq44G&rs=AOn4CLBHxpHiPdxsYqBc_aN_cSDz8rAggA")
            img_list.append("https://i.ytimg.com/vi/58BmnalsQ9I/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCMvG-b0pUO0PzWFD-JLc6uTIPACQ")
            label_list.append("中秋吃月餅有典故")
            label_list.append("嫦娥奔月、吳剛伐桂的故事")
            label_list.append("用英文介紹中秋節")
        elif(fest == "重陽節"):
            url_list.append("https://www.youtube.com/watch?v=gVnVo4IGZNE")
            url_list.append("https://www.youtube.com/watch?v=nEuT6kWtbBY")
            url_list.append("https://www.youtube.com/watch?v=CSKaVVo48p4")
            img_list.append("https://i.ytimg.com/an_webp/gVnVo4IGZNE/mqdefault_6s.webp?du=3000&sqp=CKvpq44G&rs=AOn4CLAYVsXAOrrIT82gdHS15DewJ92Uaw")
            img_list.append("https://i.ytimg.com/an_webp/nEuT6kWtbBY/mqdefault_6s.webp?du=3000&sqp=CJbmq44G&rs=AOn4CLCtBqduywIiTdXYCUDMSurzHpfPjg")
            img_list.append("https://i.ytimg.com/an_webp/CSKaVVo48p4/mqdefault_6s.webp?du=3000&sqp=CPzLq44G&rs=AOn4CLB3af9R4wwmYWtk7tJ2S5y7UU0ShQ")
            label_list.append("為什麼會有「重陽節」？")
            label_list.append("重陽節為什麼要登高山")
            label_list.append("傳統節慶(重陽節)")
        elif(fest == "冬至"):
            url_list.append("https://www.youtube.com/watch?v=tVE_xXHkvHE")
            url_list.append("https://www.youtube.com/watch?v=MSqnaQ1pePA")
            url_list.append("https://www.youtube.com/watch?v=ZbDlsIwatkQ")
            img_list.append("https://i.ytimg.com/vi/tVE_xXHkvHE/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBaK8zXA45IvcyeMwzdbCjf6EQACQ")
            img_list.append("https://i.ytimg.com/an_webp/MSqnaQ1pePA/mqdefault_6s.webp?du=3000&sqp=CPD9q44G&rs=AOn4CLBgcTHYsQ-QXFM5VNyhC6fK-VLETg")
            img_list.append("https://i.ytimg.com/an_webp/ZbDlsIwatkQ/mqdefault_6s.webp?du=3000&sqp=CKzpq44G&rs=AOn4CLDdUNoPD0sgGPu4ZhaCIaHIT6mCCg")
            label_list.append("冬至由來與活動")
            label_list.append("冬至吃湯圓製作湯圓不容易")
            label_list.append("冬至為什麼要吃湯圓？")
        column = []
        for i in range(len(url_list)):
            c = ImageCarouselColumn(
                image_url = img_list[i],
                action = URITemplateAction(
                    label = label_list[i],
                    uri = url_list[i]
                ),
            )
            column.append(c)

        reply_token = event.reply_token
        send_carousel_message(reply_token, column)
