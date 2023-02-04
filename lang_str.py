import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

CLIENT = pymongo.MongoClient(os.getenv('DB_AUTH'))
DATABASE = CLIENT['thcbot']
LANG_TABLE = DATABASE['lang']
INFO_TABLE = DATABASE['langinfo']
USERS_LANG = LANG_TABLE.find()

def get_lang(id):
    return LANG_TABLE.find_one({'user_id': id})

def no_wca_id(id):
    query_result = get_lang(id)
    if query_result is None:
        lang = 'th'
    else:
        lang = query_result['lang_id']
    return {'th': 'กรุณาใส่ WCA ID ด้วยครับ', 'en': 'Please re-use the command with the WCA ID of a person.'}[lang]

def incr_wca_id(id):
    query_result = get_lang(id)
    if query_result is None:
        lang = 'th'
    else:
        lang = query_result['lang_id']
    return {'th': 'WCA ID ไม่ถูกต้อง', 'en': 'Incorrect WCA ID.'}[lang]

def whois_embed_conts(lang):
    if lang == 'th':
        return ['สัญชาติ', 'จำนวนการแข่งขัน', 'จำนวนเหรียญทอง', 'จำนวนเหรียญเงิน', 'จำนวนเหรียญทองแดง', 'จำนวนสถิติโลก', 'จำนวนสถิติทวีป', 'จำนวนสถิติประเทศ', 'แหล่งข้อมูล : WCA API']
    else:
        return ['Country', 'Competitions', 'Gold', 'Silver', 'Bronze', 'WR', 'CR', 'NR', 'Source : WCA API']

def calculator_missing_attempt(id, n):
    query_result = get_lang(id)
    if query_result is None:
        lang = 'th'
    else:
        lang = query_result['lang_id']
    return {'th': f'กรุณากรอกเวลาให้ครบ {n} ครั้ง', 'en': f'Please re-use the command and make sure you added the time for {n} attempts.'}[lang]

def invalid_attempt(id, a):
    query_result = get_lang(id)
    if query_result is None:
        lang = 'th'
    else:
        lang = query_result['lang_id']
    return {'th': f'คุณกรอกผลการแข่งขันไม่ถูกต้องในโจทย์ที่ {a} กรุณากรอกใหม่', 'en': f'Invalid Result! Please re-use the command and make sure you fixed the result for attempt {a}.'}[lang]

def success_submit(id):
    query_result = get_lang(id)
    if query_result is None:
        lang = 'th'
    else:
        try:
            lang = query_result['lang_id']
        except IndexError:
            lang = 'th'
    return {'th': 'ระบบทำการส่งผลการแข่งขันเรียบร้อยแล้ว', 'en': 'The results have been successfully submitted.'}[lang]

def submit_not_n(id, n):
    query_result = get_lang(id)
    if query_result is None:
        lang = 'th'
    else:
        lang = query_result['lang_id']
    return {'th': f'กรุณากรอกผลการแข่งขันให้ครบ {n} ครั้ง', 'en': f'Please re-use the command and make sure you added the time for {n} attempts.'}[lang]