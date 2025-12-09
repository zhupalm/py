import os       # 负责处理文件和文件夹路径的工具包
import feedparser  # 这是一个专门用来读 RSS 的工具包
import logging     # 这是一个“日记”工具，用来记录程序运行的每一步
import datetime    # 用来获取当前时间的工具

# --- 1. 配置日志系统 (Logging) ---
# 这就像给程序装了一个“行车记录仪”，它会把运行过程打印在屏幕上
logging.basicConfig(
    level=logging.INFO,  # 设置记录的级别，INFO表示记录普通信息
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志显示的格式：时间 - 级别 - 内容
)

def fetch_and_save_rss(rss_urls, filename):
    """
    这是我们的核心功能函数。
    参数 rss_urls: 包含所有 RSS 链接的列表
    参数 filename: 要保存的文件名
    """
    
    logging.info("程序启动！准备开始抓取新闻...")

    # 获取当前时间
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 打开文件准备写入
        # 'w' 表示写入模式 (write)，如果文件不存在会创建，如果存在会清空重写
        # encoding='utf-8' 是为了防止中文乱码
        with open(filename, 'w', encoding='utf-8') as f:
            
            # 先在文件开头写上抓取时间
            f.write(f"=== 新闻抓取报告 ===\n")
            f.write(f"抓取时间: {current_time}\n")
            f.write("=" * 30 + "\n\n")
            
            logging.info(f"文件 '{filename}' 已创建，并写入了当前时间。")

            # 循环处理每一个 RSS 链接
            for index, url in enumerate(rss_urls, 1):
                logging.info(f"--------------------------------------------------")
                logging.info(f"正在连接第 {index} 个 RSS 源: {url}")
                
                try:
                    # 使用 feedparser 解析 RSS
                    # 这一步就像是派人去网站把新闻列表拿回来
                    feed = feedparser.parse(url)
                    
                    # 检查是否抓取成功 (feedparser 有时虽然报错但不抛出异常，可以通过 bozo 属性判断，但在初学阶段我们主要看 entries 是否为空)
                    if not feed.entries:
                        logging.warning(f"警报：第 {index} 个源似乎是空的，或者连接失败。")
                        f.write(f"Source {index}: 抓取失败或无内容 ({url})\n\n")
                        continue # 跳过当前循环，进入下一个链接

                    logging.info(f"连接成功！共发现 {len(feed.entries)} 条新闻。准备写入文件...")
                    
                    # 写入该 RSS 源的标题（如果有的话）
                    source_title = feed.feed.get('title', '未知来源')
                    f.write(f"来源: {source_title}\n")
                    f.write(f"链接: {url}\n")
                    f.write("-" * 20 + "\n")

                    # 遍历这个源里的每一条新闻
                    for item in feed.entries:
                        # 提取我们需要的信息，使用 .get() 是为了防止某个信息不存在时程序报错
                        title = item.get('title', '无标题')
                        link = item.get('link', '无链接')
                        published = item.get('published', '发布时间未知')
                        
                        # 格式化写入文件
                        f.write(f"标题: {title}\n")
                        f.write(f"时间: {published}\n")
                        f.write(f"链接: {link}\n")
                        f.write("\n") # 每条新闻之间空一行
                    
                    logging.info(f"第 {index} 个源的新闻已全部保存完毕。")

                except Exception as e:
                    # 如果在抓取某个特定源时出错，这里会捕获错误，不让整个程序崩溃
                    logging.error(f"处理第 {index} 个源时发生错误: {e}")
                    f.write(f"处理此源时出错: {e}\n\n")

    except Exception as e:
        # 如果文件根本打不开（比如权限不够），这里会报错
        logging.critical(f"程序发生严重错误，无法打开文件: {e}")

    logging.info("所有任务执行完毕！请查看 news_data.txt 文件。")

# --- 主程序入口 ---
if __name__ == "__main__":
    # 1. 在这里定义你要抓取的 RSS 链接列表
    # 请务必将下面的链接替换成你真实的 RSS 地址
    my_rss_list = [
        "https://theinitium.com/zh-hans/rss/",
        "https://sspai.com/feed",   # 第一个链接：少数派
        "https://chinadigitaltimes.net/chinese/feed",             # 第二个链接：知乎 (或者你可以换成其他)
    ]
    # 2. 获取当前日期 (格式为 YYYYMMDD)
    current_date_str = datetime.datetime.now().strftime('%Y%m%d')
    
    # 3. 定义目标文件夹路径 (请务必修改成你希望保存文件的实际路径！)
    target_directory = "./news/" 
    
    # 4. 动态生成文件名，例如 news_data_20251208.txt
    filename = f"news_data_{current_date_str}.txt"
    
    # 5. 检查并创建目标文件夹
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        logging.info(f"目标文件夹 '{target_directory}' 不存在，已成功创建。")
        
    # 6. 组合完整保存路径
    save_file = os.path.join(target_directory, filename)
    
    logging.info(f"文件将保存到完整路径：{save_file}")
    
    # 7. 运行函数
    fetch_and_save_rss(my_rss_list, save_file)