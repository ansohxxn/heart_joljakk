
from flask import Flask, request
from pymessenger import Bot
import requests
import json
import dbIdtoImage
import poemprint
import work

app = Flask(__name__)
ACCESS_TOKEN = 'EAALdHcJDoVUBAMcpkwc346VPdN31V0ZCYa7XSFUlkE78NqSEtkpf6WkTGoD94ZCM3OhSMhYqo473Rj4rnJMfB0e90FE5I8nQhwAEniCRZBK8turfv2qr9LRtJDrWZBjxbBHH1TcbxXvz7ZBvk0ZCRFPTZBjhqsMyvsm0gruvK6hkf7UCsZADkipZB'
VERIFY_TOKEN = 'Joljakk'
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET'])
def webhook():
    token = request.args.get("hub.verify_token")
    mode = request.args.get('hub.mode')
    print(token)
    if token == VERIFY_TOKEN and mode == 'subscribe':
        return request.args.get('hub.challenge')
    return 'Invalid verification token'


@app.route("/", methods=['POST'])
def message():
    get_started()
    output = request.get_json()
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:

            recipient_id = message['sender']['id']
            name = "소현"

            if message.get('message'):

                message_text = message['message'].get('text')

                if message_text:  # 유저직접타핑 대화

                    if message_text[0] == '마':
                        bot.send_text_message(recipient_id, "왜불러? :)")
                    elif message_text[:2] == '안녕':
                        bot.send_text_message(recipient_id, "반가워 난 마음이라고해!")
                    else:
                        bot.send_text_message(recipient_id, "마음이가 모르는 말이야 :(")

            elif message.get('postback'):

                payload = message['postback']['payload']

                if payload == 'start':

                    image_url = "https://drive.google.com/uc?id=1vfbH997YHluS1D2jJhZjjn5nCA3nMB1g"
                    bot.send_image_url(recipient_id, image_url)

                    init_text_1 = "{}! 안녕! 마음이 여기 있어.\n{}(이)가 잊지 않고 마음이한테 말 걸어줘서 마음이는 기쁘다.".format(name, name)
                    init_text_2 = "{}의 오늘 하루가 궁금하네.\n{}의 마음은 어때?".format(name, name)
                    init_text_3 = "%s의 마음을 얼굴 표정으로 보여줘." % (name)
                    bot.send_text_message(recipient_id, init_text_1)
                    bot.send_text_message(recipient_id, init_text_2)
                    bot.send_text_message(recipient_id, init_text_3)

                    button = [{
                        'type': 'postback',
                        'title': '준비 됐어 마음아!',
                        'payload': 'ready'
                    }]

                    bot.send_button_message(recipient_id, '준비 되면 나를 불러줘!', button)


                elif payload == "ready":

                    button = [{
                        'type': 'postback',
                        'title': '사진 찍기',
                        'payload': 'photo'
                    }]
                    bot.send_button_message(recipient_id, '우리 사진찍자!', button)


                elif payload == "photo":

                    result = work.takephoto()

                    if result == 'sorrow':
                        text = '아하, 오늘 %s의 마음은 이렇군. 나에게 솔직하게 알려줘서 고마워. 오늘 슬픈 일이 있었나봐. 시무룩해보이네.' % (name)
                        buttons = [

                            {
                                'type': 'postback',
                                'title': '응, 맞아. 그런일이 있었어.',
                                'payload': 'sorrow'
                            },
                            {
                                'type': 'postback',
                                'title': '아니, 별로 슬프지 않아',
                                'payload': 'wrong'
                            }
                        ]
                        bot.send_button_message(recipient_id, text, buttons)


                    elif result == 'joy':

                        text = '아하, 오늘 %s의 마음은 이렇군. 나에게 솔직하게 알려줘서 고마워. 오늘 기쁜 일이 있었나봐. 행복해보인다. :)' % (name)
                        buttons = [
                            {
                                'type': 'postback',
                                'title': '응, 맞아. 그런일이 있었어.',
                                'payload': 'joy'
                            },
                            {
                                'type': 'postback',
                                'title': '아니, 별로 기쁘지 않아',
                                'payload': 'wrong'
                            }
                        ]

                        bot.send_button_message(recipient_id, text, buttons)


                    elif result == 'anger':
                        text = '아하, 오늘 %s의 마음은 이렇군. 나에게 솔직하게 알려줘서 고마워. 오늘 화나는 일이 있었나봐. 화난 것 같아 보이네.' % (name)
                        buttons = [
                            {
                                'type': 'postback',
                                'title': '응, 맞아. 그런일이 있었어.',
                                'payload': 'anger'
                            },
                            {
                                'type': 'postback',
                                'title': '아니, 별로 화나지 않아',
                                'payload': 'wrong'
                            }
                        ]
                        bot.send_button_message(recipient_id, text, buttons)

                    elif result == 'neutral':
                        text = ' 음.. 헷갈린다.ㅠㅠ 한번만 다시 찍어줄 수 있을까? '
                        button = [{
                            'type': 'postback',
                            'title': '다시찍기',
                            'payload': 'ready'
                        }]
                        bot.send_button_message(recipient_id, text, button)

                ### 슬픔 ###

                elif payload == 'sorrow':
                    text = '그랬구나. 어떤 일이 있었어? 혹시 다른 누군가 떄문에 슬픈거야?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '응',
                            'payload': 'sorrow_y'
                        },
                        {
                            'type': 'postback',
                            'title': '아니',
                            'payload': 'sorrow_n'
                        }
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_y':
                    text = '누군가와 갈등이 있었어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '응',
                            'payload': 'sorrow_yy'
                        },
                        {
                            'type': 'postback',
                            'title': '아니',
                            'payload': 'sorrow_yn'
                        }
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_yy':

                    text = '어떤 사람이였어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '가족',
                            'payload': 'sorrow_yya'
                        },
                        {
                            'type': 'postback',
                            'title': '직장, 학교사람',
                            'payload': 'sorrow_yyb'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'sorrow_yym'
                        },

                    ]

                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_yym':

                    text = '어떤 사람이였어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '친구',
                            'payload': 'sorrow_yyb'
                        },
                        {
                            'type': 'postback',
                            'title': '연인',
                            'payload': 'sorrow_yyc'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_yya':  ##### 시출력 #####

                    keyword = "가족"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_yyb':  ##### 시출력 #####

                    keyword = "인간관계"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_yyc':
                    text = "{}의 마음은 어때?\n그게 가장 중요하지.\n{}은 어떻게 하고싶어?".format(name, name)
                    button = [
                        {
                            'type': 'postback',
                            'title': '힘들어서 \n이 관계를 그만두고 싶어.',
                            'payload': 'sorrow_yyca'
                        },
                        {
                            'type': 'postback',
                            'title': '잘해보고 싶어',
                            'payload': 'sorrow_yycb'
                        },
                        {
                            'type': 'postback',
                            'title': '사실 나도 잘 모르겠어.',
                            'payload': 'sorrow_yycc'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_yyca':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그렇구나. 이 관계를 그만두고 싶을만큼 힘들었구나.")

                    keyword = "이별"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_yycb':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그래. 잘생각했어! \n출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name))

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_yycc':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그래. 혼란스러운 감정은 당연한거야. 천천히 생각해도 돼.")

                    keyword = "인간관계"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_yn':

                    text = '누군가를 떠나보내게 되었어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '응',
                            'payload': 'sorrow_yny'
                        },
                        {
                            'type': 'postback',
                            'title': '아니',
                            'payload': 'sorrow_n'
                        }
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_yny':

                    text = '누군가를 떠나보낸다는 것은 항상 어려운 것 같아. 그사람은 %s에게 어떤 사람이었어?' % (name)
                    button = [
                        {
                            'type': 'postback',
                            'title': '나의 가족이야.',
                            'payload': 'sorrow_ynya'
                        },
                        {
                            'type': 'postback',
                            'title': '내가 한 때 좋아했던 사람이었어.',
                            'payload': 'sorrow_ynyb'
                        },
                        {
                            'type': 'postback',
                            'title': '나의 친구야.',
                            'payload': 'sorrow_ynyb'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)

                elif payload == 'sorrow_ynya':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "정말 힘들었겠다. 혼자서 얼마나 외롭고 힘들었니. 너를 꼭 안아주고 싶어.")
                    keyword = "가족"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_ynyb':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "정말 마음이 쉽지 않았겠다. 이 시가 %s에게 위로가 되었으면 좋겠다." % (name))
                    keyword = "이별"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_n':

                    text = '그렇구나. %s는 지금 어떤 마음이야?' % (name)
                    button = [
                        {
                            'type': 'postback',
                            'title': '불안하고 답답해',
                            'payload': 'sorrow_na'
                        },
                        {
                            'type': 'postback',
                            'title': '몸이 힘드니 마음도 지쳐가.',
                            'payload': 'sorrow_nb'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'sorrow_nm'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)

                elif payload == 'sorrow_nm':

                    text = '그렇구나. %s는 지금 어떤 마음이야?' % (name)
                    button = [
                        {
                            'type': 'postback',
                            'title': '어디론가 떠나고 싶어.',
                            'payload': 'sorrow_nc'
                        },
                        {
                            'type': 'postback',
                            'title': '배고파서 기운이 없어.',
                            'payload': 'sorrow_nd'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_na':

                    text = '어떤 것 때문에 불안하고 답답해?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '내 자신이 실망스러워',
                            'payload': 'sorrow_naa'
                        },
                        {
                            'type': 'postback',
                            'title': '나의 미래가 불안해',
                            'payload': 'sorrow_nab'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'sorrow_nam'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_nam':

                    text = '어떤 것 때문에 불안하고 답답해?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '이 사회가 싫어',
                            'payload': 'sorrow_nac'
                        },
                        {
                            'type': 'postback',
                            'title': '경제적으로 힘들어',
                            'payload': 'sorrow_nad'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)

                elif payload == 'sorrow_naa':

                    bot.send_text_message(recipient_id, '내 안의 비난과 비판의 목소리를 마주하느라 힘들었겠다.\n많이 두렵고 답답했지.')
                    bot.send_text_message(recipient_id, '너와 비슷한 감정을 느꼈던 시민들을 알아')

                    text = '그들의 이야기를 들어볼래?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '응, 듣고싶어!',
                            'payload': 'sorrow_naay'
                        },
                        {
                            'type': 'postback',
                            'title': '아니, 나에게 힘을줘!',
                            'payload': 'sorrow_naan'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'sorrow_naay':  ##### 시출력 #####

                    bot.send_text_message(recipient_id,
                                          "{}. 너는 혼자가 아니야.\n출력된 이 시가 {}에게 도움이 되었으면 좋겠어.".format(name, name))
                    keyword = "자아성찰"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_naan':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "우와, 멋지다. 우리 {}. \n나는 항상 {}편이야.".format(name, name))
                    bot.send_text_message(recipient_id, "이 시를 통해서 %s에게 힘을 줄게!" % (name))
                    bot.send_text_message(recipient_id, "자~ 받아랏~!! 얍!")

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_nab':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "앞이 보이지 않아서 정말 답답하고 힘들었겠다.")
                    bot.send_text_message(recipient_id, "난 널 믿어.")

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_nac':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "아직 %s 같은 사람들이 있기에 시 세상은 더 살기 좋은 세상이 될 수 있는 것 같아." % (name))
                    bot.send_text_message(recipient_id, "이 시를 한번 읽어볼래?")

                    keyword = "사회비판"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_nad':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "현실적인 어려움에 정말 막막하겠다.")
                    bot.send_text_message(recipient_id, "이 시를 통해서 %s에게 힘을 주고 싶어." % (name))

                    keyword = "경제적어려움"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_nb':

                    bot.send_text_message(recipient_id, '정말 힘들겠다..')
                    text = '오늘도 많이 피곤해? :('
                    button = [
                        {
                            'type': 'postback',
                            'title': '응. 지금도 너무 피곤해',
                            'payload': 'sorrow_nby'
                        },
                        {
                            'type': 'postback',
                            'title': '오늘은 좀 괜찮아.',
                            'payload': 'sorrow_nbn'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)

                elif payload == 'sorrow_nby':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "오늘 밤에는 푹 잤으면 좋겠다.")

                    keyword = "자연"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_nbn':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "다행이다. 오늘도 내일과 같을거야.")
                    bot.send_text_message(recipient_id, "%s! 존버 화이팅이야!." % (name))

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_nc':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그래. 그동안 너무 힘들었지.")

                    keyword = "자연"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'sorrow_nd':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "아이고! 이따가 뭐 먹을지 잘 생각해둬!")
                    keyword = "음식"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                ##### 기 쁨 ########

                elif payload == 'joy':

                    bot.send_text_message(recipient_id, '나까지 기분이 좋아지네 :)')
                    text = '어떤일이 너를 행복하게 만들었어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '그냥! 그냥 행복해:)',
                            'payload': 'joy_a'
                        },
                        {
                            'type': 'postback',
                            'title': '마음 속에 떠오르는 사람이 있어.',
                            'payload': 'joy_b'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'joy__'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'joy__':

                    text = '어떤일이 너를 행복하게 만들었어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '오늘 날씨 최고잖아!',
                            'payload': 'joy_c'
                        },
                        {
                            'type': 'postback',
                            'title': '나한테 좋은 일이 있거든!',
                            'payload': 'joy_d'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'joy_a':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그렇다면.. 더 행복해져랏! 얍! >0< ")

                    keyword = "행복"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'joy_b':

                    bot.send_text_message(recipient_id, '우와! 그런 사람이 있어서 좋겠다~')
                    text = '어떤 사람이야?'

                    button = [
                        {
                            'type': 'postback',
                            'title': '나의 연인 ♥',
                            'payload': 'joy_ba'
                        },
                        {
                            'type': 'postback',
                            'title': '정말 사랑하는 나의 가족',
                            'payload': 'joy_bb'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'joy_b_'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'joy_b_':

                    bot.send_text_message(recipient_id, '우와! 그런 사람이 있어서 좋겠다~')
                    text = '어떤 사람이야?'

                    button = [
                        {
                            'type': 'postback',
                            'title': '나를 아껴주는 친구',
                            'payload': 'joy_bc'
                        },
                        {
                            'type': 'postback',
                            'title': '나의 ex! 헤어지니까 후련해!',
                            'payload': 'joy_bd'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'joy_ba':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "사랑하는 사람과 함께 읽으면 더 좋은 시를 선물할게! ♥")

                    keyword = "사랑"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'joy_bb':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "이 시를 읽고 가족 단톡에 공유해보는건 어때?")

                    keyword = "행복"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'joy_bc':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그런 친구가 있다니 벌써 성공했다!")

                    keyword = "친구"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'joy_bd':

                    keyword = "쿨이별"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'web_url',
                        'url': 'https://youtu.be/EEhZAHZQyf4',
                        'title': 'Thank u, next!♬'
                    }]

                    bot.send_button_message(recipient_id, '아리아나 그란데가 부릅니다♪♬', button)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'joy_c':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, '오늘은 태어나기를 잘한 날이다~ ㅎㅎ')

                    keyword = "자연"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'joy_d':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, '우와 정말? 나도 이렇게 기쁜데 너는 얼마나 더 기쁠까~!')

                    keyword = "행복"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                ##### 화 남 #########

                elif payload == 'anger':
                    text = '그랬구나. 어떤 일이 있었어? 혹시 다른 누군가 떄문에 화가 난 거야?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '응',
                            'payload': 'anger_y'
                        },
                        {
                            'type': 'postback',
                            'title': '아니',
                            'payload': 'anger_n'
                        }
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_y':
                    text = '누군가와 갈등이 있었어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '응',
                            'payload': 'anger_yy'
                        },
                        {
                            'type': 'postback',
                            'title': '아니',
                            'payload': 'anger_n'
                        }
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_yy':

                    text = '어떤 사람이였어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '가족',
                            'payload': 'anger_yya'
                        },
                        {
                            'type': 'postback',
                            'title': '직장, 학교사람',
                            'payload': 'anger_yyb'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'anger_yym'
                        },

                    ]

                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_yym':

                    text = '어떤 사람이였어?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '친구',
                            'payload': 'anger_yyb'
                        },
                        {
                            'type': 'postback',
                            'title': '연인',
                            'payload': 'anger_yyc'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_yya':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, '가족 때문에 화가 났구나...')

                    keyword = "가족"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()


                elif payload == 'anger_yyb':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, '인간관계가 어렵구나...')

                    keyword = "인간관계"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_yyc':
                    text = "{}의 마음은 어때?\n그게 가장 중요하지.\n{}는 어떻게 하고싶어?".format(name, name)
                    button = [
                        {
                            'type': 'postback',
                            'title': '힘들어서 \n이 관계를 그만두고 싶어.',
                            'payload': 'anger_yyca'
                        },
                        {
                            'type': 'postback',
                            'title': '잘해보고 싶어',
                            'payload': 'anger_yycb'
                        },
                        {
                            'type': 'postback',
                            'title': '사실 나도 잘 모르겠어.',
                            'payload': 'anger_yycc'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_yyca':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그렇구나. 이 관계를 그만두고 싶을만큼 화가 나고 힘들었구나.")

                    keyword = "이별"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_yycb':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그래. 잘생각했어! \n출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name))

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_yycc':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그래. 혼란스러운 감정은 당연한거야. 천천히 생각해도 돼.")

                    keyword = "인간관계"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_n':

                    text = '그렇구나. %s는 지금 어떤 마음이야?' % (name)
                    button = [
                        {
                            'type': 'postback',
                            'title': '답답하고 화가 나',
                            'payload': 'anger_na'
                        },
                        {
                            'type': 'postback',
                            'title': '몸도 힘들고 스트레스 받아.',
                            'payload': 'anger_nb'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'anger_nm'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)

                elif payload == 'anger_nm':

                    text = '그렇구나. %s는 지금 어떤 마음이야?' % (name)
                    button = [
                        {
                            'type': 'postback',
                            'title': '힘들어서 어디론가 떠나고 싶어.',
                            'payload': 'anger_nc'
                        },
                        {
                            'type': 'postback',
                            'title': '배고파서 화가 나.',
                            'payload': 'anger_nd'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_na':

                    text = '어떤 것 때문에 불안하고 답답해?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '내 자신이 실망스러워',
                            'payload': 'anger_naa'
                        },
                        {
                            'type': 'postback',
                            'title': '나의 미래가 불안해',
                            'payload': 'anger_nab'
                        },
                        {
                            'type': 'postback',
                            'title': '더보기',
                            'payload': 'anger_nam'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_nam':

                    text = '어떤 것 때문에 불안하고 답답해?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '이 사회가 싫어',
                            'payload': 'anger_nac'
                        },
                        {
                            'type': 'postback',
                            'title': '경제적으로 힘들어',
                            'payload': 'anger_nad'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)

                elif payload == 'anger_naa':

                    bot.send_text_message(recipient_id, '내 안의 비난과 비판의 목소리를 마주하느라 힘들었겠다.\n많이 두렵고 답답했지.')
                    bot.send_text_message(recipient_id, '너와 비슷한 감정을 느꼈던 시민들을 알아')

                    text = '그들의 이야기를 들어볼래?'
                    button = [
                        {
                            'type': 'postback',
                            'title': '응, 듣고싶어!',
                            'payload': 'anger_naay'
                        },
                        {
                            'type': 'postback',
                            'title': '아니, 나에게 힘을줘!',
                            'payload': 'anger_naan'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)


                elif payload == 'anger_naay':  ##### 시출력 #####

                    bot.send_text_message(recipient_id,
                                          "{}. 너는 혼자가 아니야.\n출력된 이 시가 {}에게 도움이 되었으면 좋겠어.".format(name, name))
                    keyword = "자아성찰"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_naan':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "우와, 멋지다. 우리 {}. \n나는 항상 {}편이야.".format(name, name))
                    bot.send_text_message(recipient_id, "이 시를 통해서 %s에게 힘을 줄게!" % (name))
                    bot.send_text_message(recipient_id, "자~ 받아랏~!! 얍!")

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_nab':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "앞이 보이지 않아서 정말 답답하고 힘들었겠다.")
                    bot.send_text_message(recipient_id, "난 널 믿어.")

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_nac':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "아직 %s 같은 사람들이 있기에 시 세상은 더 살기 좋은 세상이 될 수 있는 것 같아." % (name))
                    bot.send_text_message(recipient_id, "이 시를 한번 읽어볼래?")

                    keyword = "사회비판"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_nad':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "현실적인 어려움에 정말 막막하겠다.")
                    bot.send_text_message(recipient_id, "이 시를 통해서 %s에게 힘을 주고 싶어." % (name))

                    keyword = "경제적어려움"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_nb':

                    bot.send_text_message(recipient_id, '정말 힘들겠다..')
                    text = '오늘도 많이 피곤해? :('
                    button = [
                        {
                            'type': 'postback',
                            'title': '응. 지금도 너무 피곤해',
                            'payload': 'anger_nby'
                        },
                        {
                            'type': 'postback',
                            'title': '오늘은 좀 괜찮아.',
                            'payload': 'angeer_nbn'
                        },
                    ]
                    bot.send_button_message(recipient_id, text, button)

                elif payload == 'anger_nby':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "오늘 밤에는 푹 잤으면 좋겠다.")

                    keyword = "자연"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_nbn':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "다행이다. 오늘도 내일과 같을거야.")
                    bot.send_text_message(recipient_id, "%s! 존버 화이팅이야!." % (name))

                    keyword = "의지"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_nc':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "그래. 그동안 너무 힘들었지.")

                    keyword = "자연"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()

                elif payload == 'anger_nd':  ##### 시출력 #####

                    bot.send_text_message(recipient_id, "아이고! 이따가 뭐 먹을지 잘 생각해둬!")
                    keyword = "음식"

                    id = dbIdtoImage.tag_to_id(keyword)
                    title = dbIdtoImage.getTitle(id)
                    poet = dbIdtoImage.getPoet(id)

                    text = "{} 시인의 \n<{}>".format(poet, title)
                    bot.send_text_message(recipient_id, text)

                    text = "%s에 관한 시야!" % (keyword)
                    bot.send_text_message(recipient_id, text)

                    text = "출력된 이 시가 %s에게 도움이 되었으면 좋겠다." % (name)
                    bot.send_text_message(recipient_id, text)

                    button = [{
                        'type': 'postback',
                        'title': '응, 다시해볼래!',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, '처음부터 다시 해볼래?', button)

                    poemprint.print_poem()


                ##### 잘못결과 #######

                elif payload == 'wrong':

                    text = '그래? 앗.. 미안! :( 내가 잘못 봤나봐. 그래서 말인데... 한번만 더 표정으로 알려줘 ㅎㅎ 이번엔 눈 크게뜨고 잘 볼게! '
                    button = [{
                        'type': 'postback',
                        'title': '다시찍기',
                        'payload': 'ready'
                    }]
                    bot.send_button_message(recipient_id, text, button)

    return "Message Processed"


#
############# 대화 끝 ####################


def get_started():
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'setting_type': 'call_to_actions',
        'thread_state': 'new_thread',
        'call_to_actions': [{
            'type': 'postback',
            'payload': 'start'
        }]
    }
    ENDPOINT = "https://graph.facebook.com/v2.8/me/thread_settings?access_token=%s" % (ACCESS_TOKEN)
    requests.post(ENDPOINT, headers=headers, data=json.dumps(data))


if __name__ == '__main__':
    app.run()






