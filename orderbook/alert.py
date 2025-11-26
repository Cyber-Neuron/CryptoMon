import os
import platform
import tempfile
import time
from datetime import datetime

from gtts import gTTS


class TradingAlert:
    def __init__(self, lang="zh-cn", slow=False):
        """初始化语音提醒系统

        Args:
            lang (str): 语言代码，默认中文
            slow (bool): 是否慢速播放，默认False
        """
        self.lang = lang
        self.slow = slow
        self.temp_dir = tempfile.gettempdir()

    def play_audio(self, temp_filename):
        """播放音频文件"""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                os.system(f"afplay {temp_filename}")
            elif system == "Windows":
                os.system(f"start {temp_filename}")
            elif system == "Linux":
                os.system(f"mpg123 {temp_filename}")
            else:
                print(f"不支持的操作系统: {system}")
                return False
            return True
        except Exception as e:
            print(f"播放音频错误: {e}")
            return False

    def alert(self, message, wait_time=2):
        """发出语音提醒

        Args:
            message (str): 要播放的消息
            wait_time (int): 等待播放完成的时间（秒）
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"{timestamp} {message}"

        print(f"🔔 {full_message}")

        try:
            # 创建TTS对象
            tts = gTTS(text=full_message, lang=self.lang, slow=self.slow)

            # 保存到临时文件
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=".mp3", dir=self.temp_dir
            ) as fp:
                temp_filename = fp.name

            tts.save(temp_filename)

            # 播放音频
            if self.play_audio(temp_filename):
                # 等待播放完成
                time.sleep(wait_time)

            # 删除临时文件
            try:
                os.unlink(temp_filename)
            except:
                pass  # 忽略删除错误

        except Exception as e:
            print(f"TTS错误: {e}")
            # 如果TTS失败，使用系统默认叮声
            print("\a")

    def trading_alert(self, action, amount, symbol="BTC", wait_time=2):
        """交易提醒

        Args:
            action (str): 交易动作（开空、开多、平仓等）
            amount (str): 交易金额
            symbol (str): 交易对符号
            wait_time (int): 等待时间
        """
        if action == "开空":
            message = f"发现大额开空，{symbol}，{amount}"
        elif action == "开多":
            message = f"发现大额开多，{symbol}，{amount}"
        elif action == "平仓":
            message = f"发现大额平仓，{symbol}，{amount}"
        else:
            message = f"发现{action}，{symbol}，{amount}"

        self.alert(message, wait_time)

    def price_alert(self, symbol, price, direction, wait_time=2):
        """价格提醒

        Args:
            symbol (str): 交易对符号
            price (str): 价格
            direction (str): 价格方向
            wait_time (int): 等待时间
        """
        if direction == "上涨":
            message = f"{symbol}价格{price}，正在上涨"
        elif direction == "下跌":
            message = f"{symbol}价格{price}，正在下跌"
        else:
            message = f"{symbol}价格{price}，{direction}"

        self.alert(message, wait_time)

    def custom_alert(self, message, wait_time=2):
        """自定义提醒

        Args:
            message (str): 自定义消息
            wait_time (int): 等待时间
        """
        self.alert(message, wait_time)


# 使用示例
if __name__ == "__main__":
    # 创建提醒系统实例
    alert_system = TradingAlert(lang="zh-cn", slow=False)

    print("🎤 开始测试Google TTS语音提醒系统...")

    # 测试交易提醒
    alert_system.trading_alert("开空", "100万", "BTC", wait_time=1)
    time.sleep(1)

    alert_system.trading_alert("开多", "50万", "ETH", wait_time=1)
    time.sleep(1)

    # 测试价格提醒
    alert_system.price_alert("BTC", "45000", "上涨", wait_time=1)
    time.sleep(1)

    # 测试自定义提醒
    alert_system.custom_alert("系统检测到异常交易模式", wait_time=1)

    print("✅ 测试完成！")
