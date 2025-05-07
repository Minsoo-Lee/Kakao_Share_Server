import wx
from wx import Button
from web import server
from automation import automator
import wx.richtext as rt
from window import log

def enable_task_button():
    task_button.Enable(True)

def set_buttons_after_server():
    server_button.Enable(False)
    task_button.Enable(True)

def set_buttons_after_task():
    task_button.Enable(False)

app = wx.App(False)
frame = wx.Frame(None, wx.ID_ANY, "Kakao Share")

panel = wx.Panel(frame, wx.ID_ANY)
# panel.SetBackgroundColour(wx.Colour(160, 30, 240))
panel_sizer = wx.BoxSizer(wx.VERTICAL)
frame_sizer = wx.BoxSizer(wx.VERTICAL)

text_panel = wx.Panel(panel, wx.ID_ANY)
text_sizer = wx.BoxSizer(wx.VERTICAL)

button_panel = wx.Panel(panel, wx.ID_ANY)
button_sizer = wx.BoxSizer(wx.HORIZONTAL)

# crawling 버튼 설정 - 작업 수행과 통합
# crawling_button: Button = wx.Button(button_panel, wx.ID_ANY, "크롤링", size=wx.Size(200, 30))
# crawling_button.Bind(
#     wx.EVT_BUTTON,
#     lambda event: crawling.start_crawling(
#         on_done_crawl=set_buttons_after_crawl
#     )
# )
# crawling_button.Enable(True)

# ID, PW, 방이름 받아 오기
id_input_label = wx.StaticText(text_panel, wx.ID_ANY, "ID", size=(120, 20))
id_input = wx.TextCtrl(text_panel, wx.ID_ANY, size=(205, 20))

id_sizer = wx.BoxSizer(wx.HORIZONTAL)
id_sizer.Add(id_input_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬
id_sizer.Add(id_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

pw_input_label = wx.StaticText(text_panel, wx.ID_ANY, "비밀번호", size=(120, 20))
pw_input = wx.TextCtrl(text_panel, wx.ID_ANY, size=(205, 20), style=wx.TE_PASSWORD)

pw_sizer = wx.BoxSizer(wx.HORIZONTAL)
pw_sizer.Add(pw_input_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬
pw_sizer.Add(pw_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

room_input_label = wx.StaticText(text_panel, wx.ID_ANY, "채팅방 이름", size=(120, 20))
room_input = wx.TextCtrl(text_panel, wx.ID_ANY, size=(205, 20))

room_sizer = wx.BoxSizer(wx.HORIZONTAL)
room_sizer.Add(room_input_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬
room_sizer.Add(room_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

text_sizer.Add(id_sizer, 0, wx.ALL, 5)
text_sizer.Add(pw_sizer, 0, wx.ALL, 5)
text_sizer.Add(room_sizer, 0, wx.ALL, 5)

text_panel.SetSizer(text_sizer)

# server 버튼 설정
server_button: Button = wx.Button(button_panel, wx.ID_ANY, "서버 시작", size=wx.Size(170, 30))
server_button.Bind(
wx.EVT_BUTTON,
    # start_server가 진짜
    lambda event: server.start_server(
    )
)
server_button.Enable(True)

# task 버튼 설정
task_button: Button = wx.Button(button_panel, wx.ID_ANY, "작업 수행", size=wx.Size(170, 30))
task_button.Bind(wx.EVT_BUTTON,
    lambda event: automator.start_task(
    )
)
task_button.Enable(False)

# button_sizer.Add(crawling_button, 0)
button_sizer.Add(server_button, 0, wx.LEFT, 5)
button_sizer.Add(task_button, 0, wx.LEFT, 15)

button_panel.SetSizer(button_sizer)

# 로그 창 설정
log_panel = wx.Panel(panel, wx.ID_ANY)
log_sizer = wx.BoxSizer(wx.HORIZONTAL)

log_text_widget = rt.RichTextCtrl(log_panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(350, 500))
log.set_log_widget(log_text_widget)  # 여기서 위젯 연결

log_sizer.Add(log_text_widget, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
log_panel.SetSizer(log_sizer)

panel_sizer.Add(text_panel, 0, wx.EXPAND | wx.ALL, border=5)
panel_sizer.Add(button_panel, 0, wx.EXPAND, 5)
panel_sizer.Add(log_panel, 0, wx.EXPAND, 5)

panel.SetSizer(panel_sizer)

frame_sizer.Add(panel, 1, wx.EXPAND)
frame.SetSizerAndFit(frame_sizer)

frame.Show()
app.MainLoop()

def set_crawling_button(enable):
    crawling_button.Enable(enable)

def set_server_button(enable):
    server_button.Enable(enable)



