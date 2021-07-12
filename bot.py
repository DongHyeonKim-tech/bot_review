import logging
import telegram
import requests
import pymysql
from bs4 import BeautifulSoup
import pandas as pd
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler


# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

## 봇 TOKEN
# official bot
# BOT_TOKEN = "1612750464:AAHzrMCUR24yJYLnTto5laTwSqBUdxiJU6E"

# test bot
BOT_TOKEN = "1379155122:AAFBosDJqBRSoz7oE3ru8KsE1NyiedpqSlA"

bot = telegram.Bot(token=BOT_TOKEN)

updater = Updater(token=BOT_TOKEN, use_context=True)

## handler 등록
dp = updater.dispatcher

## 이모지
rhands = "\U0001F449"


## handler
def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="홍익대학교 세종캠퍼스 정보알리미 챗봇입니다!\n원하시는 서비스를 클릭해주세요.\n\n\U0001F393/site: *각 학과 정보*\n\U0001F35A/menu: *학식 메뉴*\n\U0001F4C5/schedule: *학사 일정*\n\U0001F4D6/sugang: *정규학기 수강신청 일정*\n\U0001F3EB/other: *기타 학교 정보*\n\U0001F3E0/room: 학교 인근 *자취방* 알아보기\n\U0001F64F/feedback: *피드백* 주기\n\n\U0001F449[클래스넷 바로가기](http://www.hongik.ac.kr/login.do?Refer=https://cn.hongik.ac.kr/)\t\t\t\U0001F449[수강신청 바로가기](https://sugang.hongik.ac.kr/cn1000.jsp)",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

def intro(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="안녕하세요. 홍익대학교 졸업생입니다.\n이 챗봇은 2020년 학교에서 주최한 빅데이터 비즈니스 개발자 양성 과정 교육 중 여러 재직자 멘토님들의 도움을 받아 제작한 챗봇으로써 학교와 학생들에게 조금이나마 도움이 되고자 *비영리*적으로 졸업 이후에도 수정과 배포 등 작업을 진행중입니다.\n피드백, 개선사항 등 언제나 환영입니다.\n\n\U0001F449/start: 첫 화면으로 돌아가기",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Currently I am in Alpha stage, help me also!')

def networking(update, context):
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text='네트워킹 데이에 참석하신 여러분! 반갑습니다\U0001F606\U0001F606\U0001F606',
        parse_mode="Markdown",
    )
    context.bot.sendVideo(
        chat_id = update.message.chat_id, 
        video='https://i.gifer.com/BvDU.gif'
    )

def echo(update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def feedback(update):
    update.message.reply_text(
        "@HongikInfoManager\n위 계정에 피드백, 추가 혹은 개선됐으면 하는 사항을 보내주세요!\n\n\U0001F449/start: 첫 화면으로 돌아가기")


## button

# 학과정보
def information_task_buttons(update, context):
    task_buttons = [
        [
            InlineKeyboardButton("상경대학", callback_data="상경대학"),
            InlineKeyboardButton("과학기술대학", callback_data="과학기술대학"),
        ],
        [
            InlineKeyboardButton("조형대학", callback_data="조형대학"),
            InlineKeyboardButton("융합전공", callback_data="융합전공"),
        ],
        [InlineKeyboardButton(
            "게임학부,광고홍보학부,캠퍼스자율,산업스포츠", callback_data="기타")],
    ]
    reply_markup = InlineKeyboardMarkup(task_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="대학/학과를 선택해주세요.\n\n"+rhands+"/start: 첫 화면으로 돌아가기",
        reply_markup=reply_markup,
    )

# 식단
def menu_task_buttons(update, context):
    menu_buttons = [
        [
            InlineKeyboardButton("월요일", callback_data="월요일"),
            InlineKeyboardButton("화요일", callback_data="화요일"),
        ],
        [
            InlineKeyboardButton("수요일", callback_data="수요일"),
            InlineKeyboardButton("목요일", callback_data="목요일"),
        ],
        [
            InlineKeyboardButton("금요일", callback_data="금요일"),
            InlineKeyboardButton("이번주", callback_data="이번주"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(menu_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="교직원식당 A동\n운영시간: 11:30~14:00\n가격: 5,500\n\n\U0001F449[학교식단 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/cafe_2.html)\n\U0001F449/start: 첫 화면으로 돌아가기",
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# 학사일정
def schedule_task_buttons(update, context):
    schedule_buttons = [
        [
            InlineKeyboardButton("수강과목 사전선택 기간", callback_data="사전선택"),
            InlineKeyboardButton("등록기간", callback_data="등록"),
        ],
        [
            InlineKeyboardButton("휴학신청기간", callback_data="휴학"),
            InlineKeyboardButton("수강신청기간", callback_data="수강신청"),
        ],
        [
            InlineKeyboardButton("개강", callback_data="개강"),
            InlineKeyboardButton("수강신청 정정", callback_data="수강신청 정정"),
        ],
        [
            InlineKeyboardButton("2학기 교내장학금 신청", callback_data="교내장학금"),
            InlineKeyboardButton("종강", callback_data="종강"),
        ],
        [InlineKeyboardButton("전체일정(21-1학기)", callback_data="전체일정")],
    ]
    reply_markup = InlineKeyboardMarkup(schedule_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="2021-1학기 일정입니다. 일정을 선택해주세요.\n\n\U0001F449[학사일정 사이트 바로가기](http://sejong.hongik.ac.kr/contents/www/cor/calendar_1.html)\n\U0001F449/start: 첫 화면으로 돌아가기",
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=True

    )

# 수강신청
def sugang_task_buttons(update, context):
    sugang_buttons = [
        [
            InlineKeyboardButton("수강신청 전체 일정", callback_data="수강신청 전체 일정"),
            # InlineKeyboardButton("담아두기 전체 일정", callback_data="담아두기 전체 일정"),
        ],
        [
            InlineKeyboardButton("1,2학년", callback_data="1,2"),
            InlineKeyboardButton("3학년", callback_data="3"),
        ],
        [
            InlineKeyboardButton("4,5학년", callback_data="4,5"),
            InlineKeyboardButton("하계 계절학기", callback_data="하계"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(sugang_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="일정 혹은 학년을 선택해주세요.\n\n\U0001F449[수강신청 바로가기](https://sugang.hongik.ac.kr/cn1000.jsp)\n\U0001F449/start: 첫 화면으로 돌아가기",
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# 방
def room_task_buttons(update, context):
    room_buttons = [
        [
            InlineKeyboardButton("연세", callback_data="연세"),
            InlineKeyboardButton("월세", callback_data="월세"),
        ],
        [
            InlineKeyboardButton("전세", callback_data="전세"),
            InlineKeyboardButton("신기숙사", callback_data="신기"),
        ],
        [
            InlineKeyboardButton("구기숙사", callback_data="구기"),
            InlineKeyboardButton("기타 위치", callback_data="기타위치"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(room_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="계약 형태 혹은 위치를 선택해주세요.\n\n\U0001F449[데이터 원본 링크](https://docs.google.com/spreadsheets/d/1VdexNRBDtmgYYPW5yPR7BuT_MuZi0i32bT4GPHhEmHI/edit?usp=sharing)\n\U0001F449/start: 첫 화면으로 돌아가기",
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

"""
# 계절학기
def seasonal_task_buttons(update, context):
    seasonal_buttons = [
        [
            InlineKeyboardButton(
                "수강신청 사이트 바로가기", callback_data="계절학기 수강신청 바로가기"),
            InlineKeyboardButton("수강신청 전체 일정", callback_data="계절학기일정"),
        ],
        [
            InlineKeyboardButton("1차 수강신청 일정", callback_data="계절1차수강"),
            InlineKeyboardButton("2차 수강신청 일정", callback_data="계절2차수강"),
        ],
        [
            InlineKeyboardButton("수강철회", callback_data="계절철회정정"),
            InlineKeyboardButton("폐강 과목 수강생 수강정정기간",
                                 callback_data="계절폐강정정"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(seasonal_buttons)
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="20-2 동계 계절학기 기간: 12. 28(월) ~ 2021. 1. 20(수).\n\n/start: 첫 화면으로 돌아가기",
        reply_markup=reply_markup,
    )
"""

def other_task_buttons(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="*각 서비스 상세 안내*\n"+rhands+"1.[학사행정](http://sejong.hongik.ac.kr/contents/www/cor/scholarship.html): 계절학기, 휴/복학, 장학금 등의 규정 및 종류\n"+rhands+"2.[행정기관](http://sejong.hongik.ac.kr/contents/www/cor/stration.html): 교무입시팀, 학생복지팀, 기숙사, 산학협력단 등\n"+rhands +
        "3.[부속기관](http://sejong.hongik.ac.kr/contents/www/cor/attachedd.html): 도서관, 전산실, 취업진로지원/학생상담/교수학습지원 등\n"+rhands+"4.[증명발급](http://hongik.certpia.com/default.asp): 재학/수료/졸업예정/성적증명서 등 발급 및 발급안내\n" +
        rhands+" 5.[공용프린터](http://sejong.hongik.ac.kr/contents/www/cor/printer.html): 공용프린터 위치 및 사용시간 안내\n\n" +
        rhands+"/start: 첫 화면으로 돌아가기",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

## 크롤링
def get_text_list(tag_list):
    return [tag.text for tag in tag_list]

# 식단 크롤링
req = requests.get("http://sj.hongik.ac.kr/site/food/food_menu.html")
html = req.content
soup = BeautifulSoup(html, "html.parser")

menu_list = get_text_list(soup.select("div.foodmenu"))
date_list = get_text_list(soup.find_all("th", {"strong": ""})[2:8])

sikdan_list = []
for date, menu in zip(date_list, menu_list):
    sikdan = {"date": date, "menu": menu}
    sikdan_list.append(sikdan)

sikdan_DF = pd.DataFrame(sikdan_list)
code_html = ""
if sikdan_DF.empty == False:
    for i in range(0, len(sikdan_DF)):
        code_html = code_html + "\n\n" + \
            sikdan_DF.date.iloc[i] + sikdan_DF.menu.iloc[i]
        if i == 4:
            break

# 학사일정 크롤링
req_sche = requests.get(
    "http://sejong.hongik.ac.kr/contents/www/cor/calendar.html")
html_sche = req_sche.content
soup_sche = BeautifulSoup(html_sche, "html5lib")

list_day = soup_sche.find_all(name="td", attrs={"valign": "middle"})
half_number = len(list_day) / 2
type(int(half_number))

calendar_list = []
for index in range(20, int(half_number) + 1):
    date = list_day[index * 2 - 2].find().text
    schedule = list_day[index * 2 - 1].find().text
    schedule_obj = {
        "date": date,
        "schedule": schedule,
    }
    calendar_list.append(schedule_obj)
    if index == 41:
        break

calendar_DF = pd.DataFrame(calendar_list)

code_html_schedule = ""
if calendar_DF.empty == False:
    for i in range(0, len(calendar_DF)):
        code_html_schedule = (
            code_html_schedule
            + "\n"
            + calendar_DF.schedule.iloc[i]
            + " : "
            + calendar_DF.date.iloc[i]
        )

# room 데이터 DB에서 가져오기
con_room = pymysql.connect(
    host="us-cdbr-east-03.cleardb.com",
    user="bdfae8dc9b66b5",
    password="3dbf2eea",
    db="heroku_6140de8324f49bc",
    charset="utf8mb4",
    autocommit=True,
)

cur_room = con_room.cursor(pymysql.cursors.DictCursor)

cur_room.execute("select * from room")

rows_room = cur_room.fetchall()

room_list = []


for row in rows_room:
    room = {
        "roomId": row["roomId"],
        "location": row["location"].strip(),
        "name": row["name"].strip(),
        "floors": row["floors"].strip(),
        "contactForm": row["contactForm"].strip(),
        "pay": row["pay"],
        "deposit": row["deposit"],
        "note": row["note"].strip(),
        "etc": row["etc"].strip(),
    }
    room_list.append(room)


room_DF = pd.DataFrame(room_list)

room_oDorm = ""
room_nDorm = ""
room_loca_else = ""

room_year = ""
room_month = ""
room_charter = ""

for i in range(0, len(room_DF)):

    if room_DF.location[i] == "구기숙사":
        room_oDorm = room_oDorm,"*건물명*: "+room_DF.name.iloc[i]+" *계약형식*: "+room_DF.contactForm.iloc[i]," *방세*: "+str(
            room_DF.pay.iloc[i])+" *보증금*: "+str(room_DF.deposit.iloc[i])+"\n"
    elif room_DF.location[i] == "신기숙사":
        room_nDorm = room_nDorm,("*건물명*: "+room_DF.name.iloc[i]+" *계약형식*: "+room_DF.contactForm.iloc[i]," *방세*: "+str(
            room_DF.pay.iloc[i])+" *보증금*: "+str(room_DF.deposit.iloc[i])+"\n")
    else:
        room_loca_else = room_loca_else,("*건물명*: "+room_DF.name.iloc[i]+" *계약형식*: "+room_DF.contactForm.iloc[i]+" *방세*: "+str(
            room_DF.pay[i])+" *보증금*: "+str(room_DF.deposit.iloc[i])+"\n")

    if room_DF.contactForm[i] == "연세":
        room_year = room_year,"*위치*: "+(room_DF.location.iloc[i]+" *건물명*: "+room_DF.name.iloc[i]+" *연세*: "+str(
            room_DF.pay.iloc[i])," *보증금*: "+str(room_DF.deposit.iloc[i]),"\n")
    elif room_DF.contactForm[i] == "전세":
        room_charter = room_charter,"*위치*: ",\
            (room_DF.location.iloc[i]+" *건물명*: "+room_DF.name.iloc[i] +
             " *보증금* "+str(room_DF.pay.iloc[i]),"\n")
    else:
        room_month = room_month,"*위치*: ",(room_DF.location.iloc[i]," *건물명*: ",room_DF.name.iloc[i]," *월세*: ",str(
            room_DF.pay.iloc[i])," *보증금*: ",str(room_DF.deposit.iloc[i]),"\n")

# 데이터 가져오기-각 학부 정보
dept = ["상경대학", "과학기술대학", "조형대학", "융합전공", "기타"]
dept_num = ["1", "2", "3", "4", "5"]


connect = pymysql.connect(
    host="us-cdbr-east-03.cleardb.com",
    user="bdfae8dc9b66b5",
    password="3dbf2eea",
    db="heroku_6140de8324f49bc",
    charset="utf8mb4",
)

dept_info_list = []

for i in range(0, len(dept)):
    cur = connect.cursor(pymysql.cursors.DictCursor)
    query = (
        "SELECT DEPT_NAME, DEPT_LOC, DEPT_PH, DEPT_URL FROM TBL_DEPT WHERE DEPT_NO LIKE ",dept_num[i],"%'"
    )
    cur.execute(query)
    rows = cur.fetchall()
    connect.commit()

    for row in rows:
        dept_info = {
            "DEPT_NAME": row["DEPT_NAME"],
            "DEPT_LOC": row["DEPT_LOC"],
            "DEPT_PH": row["DEPT_PH"],
            "DEPT_URL": row["DEPT_URL"],
        }
        dept_info_list.append(dept_info)

dept_DF = pd.DataFrame(dept_info_list)
code_dept_business = ""
code_dept_sci_tech = ""
code_dept_art = ""
code_dept_else1 = ""
code_dept_else2 = ""

def fn_dept_data_input(data, start_range, end_range):
    for i in range(start_range,end_range):
        data = (
            data
            + "\n\n"
            + "["
            + dept_DF.DEPT_NAME.iloc[i]
            + "]"
            + "("
            + dept_DF.DEPT_URL.iloc[i]
            + ")"
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
        )

if dept_DF.empty == False:
    fn_dept_data_input(code_dept_business,0,4)
    """
    for i in range(0, 4):
        code_dept_business = (
            code_dept_business
            + "\n\n"
            + "["
            + dept_DF.DEPT_NAME.iloc[i]
            + "]"
            + "("
            + dept_DF.DEPT_URL.iloc[i]
            + ")"
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
        )
    """
    fn_dept_data_input(code_dept_sci_tech,4,15)
    """
    for i in range(4, 15):
        code_dept_sci_tech = (
            code_dept_sci_tech
            + "\n\n"
            + "["
            + dept_DF.DEPT_NAME.iloc[i]
            + "]"
            + "("
            + dept_DF.DEPT_URL.iloc[i]
            + ")"
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
        )
    """
    fn_dept_data_input(code_dept_art,15,21)
    """
    for i in range(15, 21):
        code_dept_art = (
            code_dept_art
            + "\n\n"
            + "["
            + dept_DF.DEPT_NAME.iloc[i]
            + "]"
            + "("
            + dept_DF.DEPT_URL.iloc[i]
            + ")"
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
        )
    """
    fn_dept_data_input(code_dept_else1,21,25)
    """
    for i in range(21, 25):
        code_dept_else1 = (
            code_dept_else1
            + "\n\n"
            + "["
            + dept_DF.DEPT_NAME.iloc[i]
            + "]"
            + "("
            + dept_DF.DEPT_URL.iloc[i]
            + ")"
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
        )
    """
    fn_dept_data_input(code_dept_else2,25,27)
    """
    for i in range(25, 27):
        code_dept_else2 = (
            code_dept_else2
            + "\n\n"
            + "["
            + dept_DF.DEPT_NAME.iloc[i]
            + "]"
            + "("
            + dept_DF.DEPT_URL.iloc[i]
            + ")"
            + "\n위치:"
            + dept_DF.DEPT_LOC.iloc[i]
            + "\n전화:"
            + dept_DF.DEPT_PH.iloc[i]
        )
    """
code_dept = [
    code_dept_business,
    code_dept_sci_tech,
    code_dept_art,
    code_dept_else2,
    code_dept_else1,
]
"""
# 데이터 가져오기-학사 일정
sc = ["사전선택", "등록", "휴학", "수강신청", "개강", "수강신청 정정", "교내장학금", "종강"]

sc_info_list = []

cur_sc = connect.cursor(pymysql.cursors.DictCursor)
query_sc = ("SELECT SC_DATE, SC_CONTENT FROM TBL_SCHEDULE")
cur_sc.execute(query_sc)
rows_sc = cur_sc.fetchall()
connect.commit()

for row_sc in rows_sc:
    sc_info = {
        "SC_DATE": row_sc["SC_DATE"],
        "SC_CONTENT": row_sc["SC_CONTENT"],
    }
    sc_info_list.append(sc_info)

sc_DF = pd.DataFrame(sc_info_list[21:])
code_sc = ""
if sc_DF.empty == False:
    for i in range(0, len(sc_info_list)):
        code_sc = (
            code_sc
            + "\n\n"
            + sc_DF.SC_CONTENT.iloc[i]
            + " : "
            + sc_DF.SC_DATE.iloc[i]
        )
"""

sc_temp = ["사전선택", "등록", "휴학", "수강신청", "개강", "수강신청 정정", "교내장학금", "종강"]
sc_tcont = ["8.4(수) ~ 8.5(목)", "8.24(화) ~ 8.30(월)", "8.24(화) ~ 8.30(월)", "8.23(월) ~ 8.26(목)", "9.1(화)", "9.1(수) ~ 9.7(화)", "11월 ~ 12월", "12.14(화)"]
sc_idv = ''
for i in range(0,len(sc_temp)):
    sc_idv = sc_idv + '\n' + sc_temp[i]+" : "+sc_tcont[i]
    sc_idv = sc_idv.strip()




def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id=update.effective_user.id, action=ChatAction.TYPING
    )

    def fn_reply_text_loop(loop_var ,loop_length ,reply_message, back_message):
        for loop_var in loop_length:
            if data == loop_var:
                context.bot.edit_message_text(
                    text=reply_message,
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id,
                    parse_mode="Markdown",
                )
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=back_message,
                )

    # 각 학과 정보
    """
    for i in range(0, len(dept)):
        if data == dept[i]:
            context.bot.edit_message_text(
                text=code_dept[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode="Markdown",
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="학과명 클릭 시 학과 홈페이지로 이동합니다.\n"+rhands +
                "/site: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기",
            )
    """
    fn_reply_text_loop(dept,dept,code_dept+"[i]","학과명 클릭 시 학과 홈페이지로 이동합니다.\n"+rhands +"/site: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기")

    # 학사일정
    """
    for i in range(0, len(sc_temp)):
        if data == sc_temp[i]:
            context.bot.edit_message_text(
                text = "*"+sc_temp[i]+"* : "+sc_tcont[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode = "Markdown",
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=rhands+"/schedule: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기")
    """

    fn_reply_text_loop(sc_temp,sc_temp,"*"+sc_temp[i]+"* : "+sc_tcont[i],text=rhands+"/schedule: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기")
    
    if data == "전체일정":
        context.bot.edit_message_text(
            text = "*[2021-2학기 주요 일정]*\n"+sc_idv,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode = "Markdown",
            )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/schedule: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기")

    # 학교 식단
    if data == "이번주":
        context.bot.edit_message_text(
            text=code_html,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/menu: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
        )

    Food = ["월요일", "화요일", "수요일", "목요일", "금요일"]
    for i in range(0, len(Food)):
        if data == Food[i]:
            context.bot.edit_message_text(
                text="*" + sikdan_DF.date.iloc[i] + "*" + str(sikdan_DF.menu.iloc[i]).strip(),
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode="Markdown",
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=rhands+"/menu: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
            )

    # 수강신청
    # 각 학년 수강신청 기간
    sign = ["1,2", "3", "4,5"]
    sign_time = [
        "06.11(금) 09:00 ~ 17:00",
        "06.10(목) 09:00 ~ 17:00",
        "06.09(수) 09:00 ~ 17:00",
    ]
    for i in range(0, len(sign)):
        if data == sign[i]:
            context.bot.edit_message_text(
                text=sign[i]
                + "학년 수강신청 기간은 *"
                + sign_time[i]
                + "*입니다.\n\n"+rhands+"/sugang: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기",
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode = "Markdown",
            )
    if data  == "하계":
        context.bot.edit_message_text(
            text = "하계 계절학기 기간은 *06.28(월) ~ 07.16(금)* 입니다.\n\n"+rhands+"/sugang: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기",
            chat_id = query.message.chat_id,
            message_id = query.message.message_id,
            parse_mode="Markdown",
        )
    # 전체 수강신청, 담아두기 기간 및 수강신청 바로가기
    sign_else = ["수강신청 전체 일정", "담아두기 전체 일정", "수강신청 바로가기"]
    sign_else_content = [
        "*[1차 수강신청]*\n1,2학년: 06.11(금) 09:00 ~ 17:00\n3학년: 06.10(목) 09:00 ~ 17:00\n4,5학년: 06.09(수) 09:00 ~ 17:00\n전체학년 추가: 06.14(월) 09:00 ~ 17:00\n1차 수강료 납부: 06.15(화) 09:00 ~ 06.17(목) 16:00\n\n*[2차 수강신청]*\n전체: 3.2(화) 09:00 ~ 3. 8(월) 17:00\n2차 수강료 납부: 06.12(월) 09:00 ~ 06.23(수) 16:00\n\n*[수강철회]*\n철회: 06.24(목) 15:00 ~ 06.25(금) 17:00\n\n*[폐강과목 수강생 정정기간]*\n기간: 06. 24(목) 15:00 ~ 06.25(금) 17:00\n\n/sugang: 뒤로가기\n/start: 첫 화면으로 돌아가기",
        "1차 담아두기 기간: 2. 4(목) 09:00 ~ 2. 5(금) 17:00\n2차 담아두기 기간: 2.10(수) 09:00 ~ 2.22(월) 17:00\n\n" +
        rhands+"/sugang: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기",
        ""+rhands+"[수강신청 사이트 바로가기](https://sugang.hongik.ac.kr/cn1000.jsp)\n\n" +
        rhands+"/sugang: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기",
    ]
    for i in range(0, len(sign_else)):
        if data == sign_else[i]:
            context.bot.edit_message_text(
                text=sign_else_content[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode="Markdown",
            )
    if data == "연세":
        context.bot.edit_message_text(
            text=room_year,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/room: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
        )

    if data == "전세":
        context.bot.edit_message_text(
            text=room_charter,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/room: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
        )
    if data == "월세":
        context.bot.edit_message_text(
            text=room_month,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/room: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
        )
    if data == "구기":
        context.bot.edit_message_text(
            text=room_oDorm,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/room: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
        )
    if data == "신기":
        context.bot.edit_message_text(
            text=room_nDorm,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/room: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
        )
    if data == "기타위치":
        context.bot.edit_message_text(
            text=room_loca_else,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode="Markdown",
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=rhands+"/room: 뒤로가기\n"+rhands+"/start: 첫 화면으로 돌아가기"
        )
"""
    계절학기
    seasonal = ["계절1차수강", "계절2차수강", "계절철회정정",
                "계절폐강정정", "계절학기일정", "계절학기 수강신청 바로가기"]
    seasonal_content = ["1,2학년: 12. 09(수) 09:00 ~ 17:00\n3학년: 12. 08(화) 09:00 ~ 17:00\n4,5학년: 12. 07(월) 09:00 ~ 17:00\n전체: 12. 10(목) 09:00 ~ 17:00\n1차 수강료 납부: 12. 11(금) 09:00 ~ 12. 15(화) 16:00\n※ 1차 수강료를 납부하지 않으면 1차 수강신청내역은 일괄 삭제\n\n/start: 첫 화면으로 돌아가기",
                        "2차 수강신청: 12. 16(수) 09:00 ~ 17:00\n2차 수강료 납부: 12. 17(목) 09:00 ~ 12. 18(금) 16:00\n※ 2차 수강료를 납부하지 않으면 2차 수강신청 내역은 일괄 삭제\n계절학기에는 수강신청 정정 허가원이 없으므로 유의\n\n/start: 첫 화면으로 돌아가기",
                        "수강철회: 12. 21(월) 09:00 ~ 12. 22(화) 17:00\n※ 추가 수강신청이나 정정은 되지 않고 철회만 가능\n철회한 내역에 대해 기납부한 수강료는 전액 환불처리\n\n/start: 첫 화면으로 돌아가기",
                        "폐강과목 수강생 정정기간: 12. 23(수) 15:00 ~ 12. 24(목) 17:00까지\n온라인 정정 : 수강신청페이지 > 폐강과목 수강정정\n\n/start: 첫 화면으로 돌아가기",
                        "*1차 수강신청\n1,2학년: 12. 09(수) 09:00 ~ 17:00\n3학년: 12. 08(화) 09:00 ~ 17:00\n4,5학년: 12. 07(월) 09:00 ~ 17:00\n전체: 12. 10(목) 09:00 ~ 17:00\n\n*2차 수강신청\n2차 수강신청: 12. 16(수) 09:00 ~ 17:00\n\n/start: 첫 화면으로 돌아가기",
                        " [동계 계절학기 수강신청 사이트 바로가기](https://sugang.hongik.ac.kr/cn1000.jsp)\n\n/seasonal: 뒤로가기/start: 첫 화면으로 돌아가기",
                        ]
    for i in range(0, len(seasonal)):
        if data == seasonal[i]:
            context.bot.edit_message_text(
                text=seasonal_content[i],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                parse_mode="Markdown",
            )
    기타
"""

def main():

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("feedback", feedback))
    dp.add_handler(CommandHandler("site", information_task_buttons))
    dp.add_handler(CommandHandler("menu", menu_task_buttons))
    dp.add_handler(CommandHandler("schedule", schedule_task_buttons))
    dp.add_handler(CommandHandler("sugang", sugang_task_buttons))
    dp.add_handler(CommandHandler("room", room_task_buttons))
    dp.add_handler(CommandHandler("other", other_task_buttons))
    dp.add_handler(CommandHandler("Networking",networking))
    dp.add_handler(CallbackQueryHandler(cb_button))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
