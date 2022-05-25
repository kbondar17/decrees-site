import pickle
import random
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

import django
django.setup()

from decrees.models import Document, Formats, MyUser
from django.contrib.auth.models import User
from decrees.models import Position, Person, Event

# прежде чем получать доступ к бд джанго. джанго нужно загрузить настройки.

# def populate_db_with_mock_data():
#     data: pd.DataFrame = pickle.load(open('converter/mock_data.pkl', 'rb'))
#     data = data
#     sizes = [e for e in range(len(data))]
#     for size, e in zip(sizes, data.itertuples()):

#         e = e._asdict()

#         user_name = e['Username']
#         mail = user_name + '@gmail.com'
#         passw = 'pass'
#         user_obj, _ = MyUser.objects.get_or_create(username=user_name, email=mail)

#         if not user_obj.password:
#             user_obj.set_password(passw)
#         user_obj.save()

#         format = e['Format']
#         new_format, created = Formats.objects.get_or_create(formatname=format)

#         file = e['FileName']
#         date = e['Date']
#         new_doc, created = Document.objects.get_or_create(doc_format=new_format,user=user_obj,
#                                                         doc_name=file, upload_date=date, size=size)
    
#         print(new_doc, created)

# populate_db_with_mock_data()
# from datetime import datetime

# p1 = Person.objects.filter(name='kirill')[0]
# # p1 = Person(name='kirill')
# # p1.save()
# # position = Position(name='director', level='regional')
# # # # position = Position.objects.filter(name='director')[0]
# # position.save()
# event = Event.objects.all()[0]
# breakpoint()
import dateparser
import json
fed_path = r"C:\Users\ironb\прогр\Declarator\appointment-decrees\downloads\regions\федеральное законодательство\results\федеральное законодательство_parsed.json"
# belgorod = r"C:\Users\ironb\прогр\Declarator\appointment-decrees\downloads\regions\Белгородская область\resultsБелгородской области_parsed.json"
# rostov = r"C:\Users\ironb\прогр\Declarator\appointment-decrees\downloads\regions\Ростовская область\resultsРостовская область_parsed.json"

LEVEL = 'federal'
REGION = 'Федеральный уровень'


def populate_bd_with_parsing_results():
    fed_data = json.load(open(fed_path, 'r'))['parsed_data']
    for file in fed_data:
        try:
            date = file['date']
            date = dateparser.parse(date,locales=['fr-PF']) 
            full_text = file['text_raw']
            link = file['link']
            for line in file['appointment_lines']:
                raw_line = line['raw_line']
                new_position = line['position']
                for appointed_person in line['appointed']:
                    name = appointed_person['name_norm']
                    pers,_  = Person.objects.get_or_create(name=name)
                    pos,_ = Position.objects.get_or_create(name=new_position, level=LEVEL)
                    pos.save()

                    ev = Event(action='appoint', date=date, level=LEVEL, position=pos, person=pers,
                    full_text=full_text, line=raw_line, region=REGION, link=link)
                    ev.save() 
                    
                if 'resigned' in line.keys():
                    for resigned_person in line['resigned']:
                        name = resigned_person['name_norm']
                        pers,_  = Person.objects.get_or_create(name=name)
                        ev = Event(action='resign', date=date, level=LEVEL, position=pos, person=pers,
                        full_text=full_text, line=raw_line, region=REGION, link=link)
                        ev.save() 

        except Exception as ex:
            print(file['file_name'], ex)

populate_bd_with_parsing_results()
# fed_data = json.load(open(fed_path, 'r'))['parsed_data
# for file in fed_data:
#     try
#         date = file['date']
#         date = dateparser.parse(date,locales=['fr-PF']) 
#         full_text = file['text_raw']
#         link = file['link']
#         for line in file['appointment_lines']:
#             raw_line = line['raw_line']
#             new_position = line['position']

#             # for appointed_person in line['appointed']:
#             #     name = appointed_person['name_norm']
#             #     pers  = Person.objects.get(name=name)
#             #     pos = Position.objects.get(name=new_position, level=LEVEL)
#                 # ev_obj = Event.objects.get(action='appoint', date=date, level=LEVEL, position=pos, person=pers)
#                 # ev_obj.link = link
#                 # ev_obj.save()
#             #     pers,_  = Person.objects.get_or_create(name=name)
#             #     pos,_ = Position.objects.get_or_create(name=new_position, level=LEVEL)
#             #     pos.save()

#             #     ev = Event(action='appoint', date=date, level=LEVEL, position=pos, person=pers,
#             #     full_text=full_text, line=raw_line, region=REGION)
#             #     ev.save() 
                
#             if 'resigned' in line.keys():
#                 for resigned_person in line['resigned']:
#                     name = resigned_person['name_norm']
#                     pers  = Person.objects.get(name=name)
#                     pos = Position.objects.get(name=new_position, level=LEVEL)
#                     ev = Event.objects.get(action='resign', date=date, level=LEVEL, position=pos, person=pers)
#                     ev.link = link
#                     # ev = Event(action='resign', date=date, level=LEVEL, position=pos, person=pers,
#                     # full_text=full_text, line=raw_line, region=REGION)
                    
#                     ev.save() 



#     except Exception as ex:
#         print(file['file_name'],ex)

# ev = Event.objects.filter()
