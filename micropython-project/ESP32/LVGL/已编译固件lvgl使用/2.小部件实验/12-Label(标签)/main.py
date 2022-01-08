'''
实验名称：Label(标签)
版本：v1.0
日期：2020.7
作者：01Studio【www.01Studio.org】
'''

import lvgl as lv
import ujson

from ili9341 import ili9341
from xpt2046 import xpt2046

TFT_IS_PORTRAIT =1 #竖屏：1 ，横屏：0 ；
TOUCH_READY = 0 #用于检测触摸屏是否已经校准过；

#LCD ili9341初始化
disp = ili9341(
    miso=12,
    mosi=13,
    clk=14,
    cs=15,
    dc=21,
    rst=33,
    power=50,  #硬件不支持，随便配一个参数
    backlight=51, #硬件不支持，随便配一个参数
    backlight_on= 1,
    power_on= 1,
    width=240 if TFT_IS_PORTRAIT else 320,
    height=320 if TFT_IS_PORTRAIT else 240,
    rot=ili9341.PORTRAIT if TFT_IS_PORTRAIT else ili9341.LANDSCAPE #垂直方向PORTRAIT ；水平方向：LANDSCAPE
)

#触摸屏设置校准
TOUCH_CS = 2  #触摸屏CS片选引脚
TOUCH_INTERRUPT=0 #横屏

if TFT_IS_PORTRAIT:
    TOUCH_CALI_FILE = "touch_cali_PORTRAIT.json" #保存为竖屏触摸参数
else:
    TOUCH_CALI_FILE = "touch_cali_LANDSCAPE.json" #保存为横屏触摸参数

#从没做过触摸校准
if TOUCH_CALI_FILE not in uos.listdir():
    touch = xpt2046(
        cs=TOUCH_CS,
        transpose=TFT_IS_PORTRAIT,
    )

    from touch_cali import TouchCali

    touch_cali = TouchCali(touch, TOUCH_CALI_FILE)
    touch_cali.start()

#已经做过触摸校准，直接调用触摸参数文件
else:
    with open(TOUCH_CALI_FILE, 'r') as f:
        param = ujson.load(f)
        touch_x0 = param['cal_x0']
        touch_x1 = param['cal_x1']
        touch_y0 = param['cal_y0']
        touch_y1 = param['cal_y1']

    touch = xpt2046(
        cs=TOUCH_CS,
        transpose=TFT_IS_PORTRAIT,
        cal_x0=touch_x0,
        cal_x1=touch_x1,
        cal_y0=touch_y0,
        cal_y1=touch_y1,
    )

    TOUCH_READY = 1 #表示已经配置好触摸参数

#############################################
#################   Label   #################
#############################################
if TOUCH_READY:

    label1 = lv.label(lv.scr_act())
    label1.set_long_mode(lv.label.LONG.BREAK)     # Break the long lines
    label1.set_recolor(True)                      # Enable re-coloring by commands in the text
    label1.set_align(lv.label.ALIGN.CENTER)       # Center aligned lines
    label1.set_text("#0000ff Re-color# #00ff00 words# #ff0000 of a# label " +
                "and  wrap long text automatically.")
    label1.set_width(150)
    label1.align(None, lv.ALIGN.CENTER, 0, -30)

    label2 = lv.label(lv.scr_act())
    label2.set_long_mode(lv.label.LONG.SROLL_CIRC)     # Circular scroll
    label2.set_width(150)
    label2.set_text("It is a circularly scrolling text. ")
    label2.align(None, lv.ALIGN.CENTER, 0, 30)
