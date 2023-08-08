from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from utils.baidu_utils import *
import pyautogui
import os
import time

# 把下面获取到的cookie复制到这里，以后就不用每次都获取cookie了
cookies = None


def find_douyin_beauty(url):
    # 设置pyautogui参数
    pyautogui.PAUSE = 2
    pyautogui.FAILSAFE = True

    # 设置Chrome浏览器选项
    chrome_options = Options()
    # 忽略证书错误
    chrome_options.add_argument('--ignore-certificate-errors')
    # 设置chrome lib地址，选择和自己浏览器版本相同的lib，lib下载地址https://googlechromelabs.github.io/chrome-for-testing/
    chrome_service = Service(r'D:/Code/Funny/chrome-win64')
    # 初始化Chrome浏览器
    driver = webdriver.Chrome(service=chrome_service,options=chrome_options)

    try:
        # 打开douyin URL  https://www.douyin.com/
        driver.get(url)
        # 等待页面加载，可以根据具体情况调整等待时间，这里需要手动登陆后获取cookie
        time.sleep(60)
        print(driver.get_cookies())
        cookies = driver.get_cookies()

        # 先清除原有的cookies
        driver.delete_all_cookies()
        for cookie in cookies:
            cookie_dict = {
            'domain': '.douyin.com',
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": cookie.get('value'),
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False}
            driver.add_cookie(cookie_dict)
        # 带着cookie重新加载
        driver.refresh()
        driver.implicitly_wait(10)

        #百度API获取token
        access_token = get_access_token()

        while(True):
            #1.刷新下一个视频
            pyautogui.press('down')
            print("开始检测=============================================")

            #2.保存文件名，默认以时间戳命名
            current_timestamp = int(time.time())
            account_name = str(current_timestamp)
            account_name += '.png'
            # 截图存放目录
            tmp_img = 'img/' + account_name
            # 截取屏幕，
            driver.save_screenshot(tmp_img)
            print('Account Name:%s,保存在临时目录:%s' % (account_name,tmp_img))

            #3.调用百度人脸识别API,返回find_beauty 是否找到美女，标准是18-30岁，颜值70分以上，result_str 识别结果，在页面上显示
            is_beauty,result_str = analysis_face(parse_face_pic(tmp_img, TYPE_IMAGE_LOCAL, access_token))

            # 识别到美女
            if is_beauty:
                print('识别到一个美女，继续下一个视频~')
            else:
                os.remove(tmp_img)
                print('删除临时文件%s，继续下一个视频别~' % tmp_img)


            # 创建一个半透明的 < div > 元素,显示识别结果
            script = """
            var transparentDiv = document.createElement('div');
            transparentDiv.id = 'transparent-div'; // Set an ID
            transparentDiv.style.position = 'fixed';
            transparentDiv.style.top = '50%';
            transparentDiv.style.left = '50%';
            transparentDiv.style.transform = 'translate(-50%, -50%)';
            transparentDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.7)'; // 半透明的白色背景
            transparentDiv.style.width = '300px'; // 调整宽度
            transparentDiv.style.height = '200px'; // 调整高度
            transparentDiv.style.textAlign = 'center';
            transparentDiv.style.display = 'flex';
            transparentDiv.style.justifyContent = 'center';
            transparentDiv.style.alignItems = 'center';
            transparentDiv.style.zIndex = '9999';
            transparentDiv.innerHTML = '视频检测结果：""" + result_str + """';

            document.body.appendChild(transparentDiv);
            setTimeout(function() {
                var divToRemove = document.getElementById('transparent-div');
                if (divToRemove) {
                    divToRemove.parentNode.removeChild(divToRemove);
                }
            }, 5000); // 5000 milliseconds = 5 seconds
            """

            # 执行弹窗JS代码
            driver.execute_script(script)
            time.sleep(5)
            print("检测完成，开始下一个视频=============================")
    except Exception as e:
        print(f"检测失败: {e}")
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    # 设置要访问的HTML页面的URL
    target_url = "https://www.douyin.com/"
    # 启动主程序
    find_douyin_beauty(target_url)
