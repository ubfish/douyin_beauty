## 基于python + selenium自动寻找抖音上漂亮的小姐姐

github上有一些用python + ADB 寻找漂亮小姐姐的程序，但是要配置ADB，还要占用一个手机，太麻烦了

这里我基于python + selenium 实现基于chrome，在抖音的网页上自动寻找漂亮小姐姐 

代码参照了github上前辈们的代码，主要业务逻辑让chatGPT帮我实现，做了些调试修改，用一天的实现实现了这个自动寻找抖音漂亮小姐姐的程序

自动点赞，关注等功能还没有做，有兴趣的可以自行下载代码扩展

百度人脸识别代码参照 https://github.com/kzqsky/douyin 

## 原理

- 打开抖音主页 http://www.douyin.com，获取cookie
- 打开抖音视频，获取屏幕截图
- 请求 [人脸识别 API](https://console.bce.baidu.com)
- 解析返回的人脸 Json 信息，对人脸检测切割；
- 当颜值大于70时，保存图片；
- 自动刷新下一个视频；

##  特性
- [x] **自动翻页**
- [x] **颜值检测**
- [x] **人脸识别**
- [x] **保存图片**
- [x] **自动关注（还未做）**
- [x] **自动点赞（还未做）**

## 使用

- 安装依赖：

pip install PyAutoGUI 

pip install selenium

其他的看缺什么自己装吧，主要依赖这两个库

- 获取抖音cookie

执行 python douyin_beayty.py

把输出的cookie全部复制到douyin_beayty.py的cookies字段里，按下面的代码注释掉获取cookie的代码，以后不用每次都获取cookie

        # 打开douyin URL  https://www.douyin.com/
        driver.get(url)
        # 等待页面加载，可以根据具体情况调整等待时间，这里需要手动登陆后获取cookie
        #time.sleep(60)
        #print(driver.get_cookies())
        #cookies = driver.get_cookies()

- 安装chrome lib
    
   
    #设置chrome lib地址，选择和自己浏览器版本相同的lib，lib下载地址https://googlechromelabs.github.io/chrome-for-testing/
    
    chrome_service = Service(r'D:/Code/Funny/chrome-win64')

- 申请百度人脸识别API

更新utils/baidu_utils.py里的APP_ID,API_KEY,SECRET_KEY，有免费的额度多出来的要额外购卖

    # https://console.bce.baidu.com
    # 需要替换自己的APP信息
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

- 执行主程序

python douyin_beauty.py



