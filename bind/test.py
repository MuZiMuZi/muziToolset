from muziToolset.bind.Bind_Tool_main import Bind_Tool_main
from importlib import reload
reload(Bind_Tool_main)

try :
    win.close ()  # Ϊ�˲��ô��ڳ��ֶ������Ϊ��һ�����л�û��ʼ��������Ҫtry�������ﳢ���ȹرգ��������½�һ������
    win.deleteLater ()
except :
    pass
win = Bind_Tool_main.Bind_Widget ()
win.show ()
