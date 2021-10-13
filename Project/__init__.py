from flask import Flask, request, abort
from numpy.lib.npyio import save
import requests
import json
from Project.Config import *
app = Flask(__name__)
import urlfetch
from linebot import LineBotApi
from flask import send_file
import PIL  
from PIL import Image
import io
from io import BytesIO

line_bot_api = LineBotApi(Channel_access_token)
@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        type = payload['events'][0]['message']['type']
        print("type=")
        print(type)
        print(payload['events'][0]['message']['id'])
        if type == 'image':
            Reply_messasge = 'ได้รับรูปแล้ว'
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        elif type == 'text':
            message = payload['events'][0]['message']['text']
            if 'ทดสอบ' in message:
                Reply_messasge = 'ทดสอบรับข้อความ'
                ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                
            else :
                Reply_messasge = 'ได้รับข้อความ'
                ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        else :
            Reply_messasge = ''
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)


@app.route('/')
def hello():
    return 'hello webhook',200

@app.route('/image')
def urlimage():
    path = request.args.get('path')
    filename = f"saveimg\\{path}.jpg"
    return send_file(filename, mimetype='image/jpg'),200

def getImage(message_id,Line_Acees_Token):
    LINE_API = 'https://api-data.line.me/v2/bot/message/'+message_id+'/content'
    print(LINE_API)
    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    data = urlfetch.get(LINE_API, headers = {'Authorization':Authorization})
    img_list =  [i for i in data]
    img = img_list[0]
    for i in img_list[1:]:
        img+=i

    print(len(img))

    img_PLT_jpeg = Image.open(io.BytesIO(img))
    img_1 = img_PLT_jpeg.convert('RGB')
    img_1.save(f'Project\\saveimg\\img_{message_id}.jpg')
    f="บันทึกรูปภาพสำเร็จ"
    return f

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }
    payload = request.json
    if (payload['events'][0]['message']['type']=='image'):
        save = getImage(payload['events'][0]['message']['id'],Channel_access_token)
       
        data = {
            "replyToken":Reply_token,
            "messages":[{
                "type":"text",
                "text":TextMessage+'\n'+save
            }]
        }
    
    elif (payload['events'][0]['message']['type']=='text'):
        data = {
            "replyToken":Reply_token,
            "messages":[{
                "type":"text",
                "text":TextMessage
            }]
        }

    else:
        data = {
            "replyToken":Reply_token,
            "messages":[{
                "type":"text",
                "text":"ได้รับบางอย่างจากผู้ใช้"
            }]
        }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200