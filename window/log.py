import wx, time

log_text_widget = None

def set_log_widget(widget):
    global log_text_widget
    log_text_widget = widget

def append_log(log):
    global log_text_widget

    if log_text_widget is None:
        return

    current_time = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
    # color = wx.WHITE
    color = wx.BLACK
    if '[ERROR]' in log or '오답' in log:
        color = wx.RED
    elif '작업이 모두 끝났습니다.' in log or '완료' in log:
        color = wx.GREEN
    elif '초기화' in log:
        color = wx.BLUE
    log = current_time + log
    #
    # log_text_widget.BeginTextColour(color)
    # log_text_widget.WriteText(log + "\n")
    # log_text_widget.EndTextColour()
    # log_text_widget.ShowPosition(log_text_widget.GetLastPosition())

    def update_ui():
        log_text_widget.BeginTextColour(color)
        log_text_widget.WriteText(log + "\n")
        log_text_widget.EndTextColour()
        log_text_widget.ShowPosition(log_text_widget.GetLastPosition())

    wx.CallAfter(update_ui)  # 👈 메인쓰레드에서 실행되도록 보장