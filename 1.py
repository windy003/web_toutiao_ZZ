from DrissionPage import ChromiumPage, ChromiumOptions
import time
import traceback


# 创建配置对象
options = ChromiumOptions()
# options.set_argument('--headless=new')  # 使用新的无头模式
# options.set_argument('--no-sandbox')    # 在Linux系统中添加此参数
# options.set_argument('--disable-dev-shm-usage')  # 避免内存不足问题

# 使用配置创建页面对象
page = ChromiumPage(options)
# print("已启动无头浏览器...")


url = "https://www.toutiao.com/c/user/token/MS4wLjABAAAAGHTR9RhT2qjtgvbPUwReH0SDKY5C-6EJd7EXebQjmZ8/?"



try:
    page.get(url)

    # 滚动页面并加载更多内容
    try:
        # 使用 JavaScript 获取页面高度
        last_height = page.run_js('return document.documentElement.scrollHeight')
        while True:
            # 滚动到底部
            page.scroll.to_bottom()
            print("已滚动到底部，等待新内容加载...")
            time.sleep(3)  # 等待新内容加载

            # 使用 JavaScript 获取新的页面高度
            new_height = page.run_js('return document.documentElement.scrollHeight')

            # 如果页面高度没有变化，说明已经到底部
            if new_height == last_height:
                time.sleep(6)
                page.scroll.to_bottom()
                new_height = page.run_js('return document.documentElement.scrollHeight')
                if new_height == last_height:
                   time.sleep(9)
                   page.scroll.to_bottom()
                   new_height = page.run_js('return document.documentElement.scrollHeight') 
                   if new_height == last_height:
                        print("已到达页面底部，停止滚动。")
                        break
                       
                
                
                
                

            # 更新页面高度
            last_height = new_height
            
    except Exception as e:
        print(f"滚动页面失败: {e}")





    # 获得文章和微头条链接块包括标题
    data = ""
    try:
        eles = page.eles('xpath://div[@class="profile-article-card-wrapper" or @class="profile-wtt-card-wrapper" or @class="profile-normal-video-card-wrapper"]')
        for i, ele in enumerate(eles):
            try:
                # 检查元素类型
                if 'profile-article-card-wrapper' in ele.attr('class'):  # 文章
                    time_element = ele.ele('xpath:.//div[@class="feed-card-footer-time-cmp"]')
                    title_element = ele.ele('xpath:.//a[@class="title"]')
                elif 'profile-wtt-card-wrapper' in ele.attr('class'):  # 微头条
                    time_element = ele.ele('xpath:.//div[@class="time"]')
                    title_elements = ele.eles('xpath:.//a')
                    title_element = title_elements[2] if title_elements else None
                elif 'profile-normal-video-card-wrapper' in ele.attr('class'):  # 视频
                    time_element = ele.ele('xpath:.//div[@class="feed-card-footer-time-cmp"]')
                    title_element = ele.ele('xpath:.//a[@class="title"]')
                else:
                    print(f"未找到文章或微头条{i}")
                    continue

                # 处理元素
                if time_element and title_element:
                    publish_time = time_element.text + "<br>"
                    title_text = title_element.text
                    if "\n" in title_text:
                        title_text = title_text.replace("\n", "")
                    if len(title_text) > 30:
                        title_text = title_text[:30]
                    href = title_element.attr('href')
                    title = f'<a href="{href}" target="_blank" rel="noopener" aria-label="{title_text}">{title_text}</a>  <br><br><br>'
                    data += publish_time + title + "\n"
                    print(f"成功加入一个{'文章' if 'profile-article-card-wrapper' in ele.attr('class') else '微头条' if 'profile-wtt-card-wrapper' in ele.attr('class') else '视频'}{i}")

            
            except Exception as e:
                print(f"处理元素{i}时出错: {e}")
                continue
                
        print(f"共处理了 {i + 1} 个元素")


        try:
            with open('BDJC12.txt', 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception as e:
            print(f"保存数据失败: {e}")

        
    except Exception as e:
        print(f"获取文章和微头条失败: {e}")
        traceback.print_exc()


except Exception as e:
    print(f"访问页面失败: {e}")





