#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章解析脚本
使用 Playwright 解析微信公众号文章内容
"""

from playwright.sync_api import sync_playwright
import time
import json


def parse_wechat_article(url: str) -> dict:
    """
    解析微信公众号文章
    
    Args:
        url: 微信公众号文章链接
        
    Returns:
        包含文章信息的字典
    """
    result = {
        'url': url,
        'title': '',
        'author': '',
        'account_name': '',
        'publish_time': '',
        'content': '',
        'content_html': '',
        'images': [],
        'success': False,
        'error': None
    }
    
    try:
        with sync_playwright() as p:
            # 启动浏览器（无头模式）
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 设置用户代理，模拟真实浏览器
            page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            print(f"正在访问: {url}")
            page.goto(url, wait_until='networkidle', timeout=30000)
            
            # 等待页面加载
            time.sleep(2)
            
            # 提取文章标题
            try:
                title_element = page.query_selector('#activity-name')
                if title_element:
                    result['title'] = title_element.inner_text().strip()
            except Exception as e:
                print(f"提取标题失败: {e}")
            
            # 提取公众号名称
            try:
                account_element = page.query_selector('#js_name')
                if account_element:
                    result['account_name'] = account_element.inner_text().strip()
            except Exception as e:
                print(f"提取公众号名称失败: {e}")
            
            # 提取作者
            try:
                author_element = page.query_selector('#js_author')
                if author_element:
                    result['author'] = author_element.inner_text().strip()
            except Exception as e:
                print(f"提取作者失败: {e}")
            
            # 提取发布时间
            try:
                time_element = page.query_selector('#publish_time')
                if time_element:
                    result['publish_time'] = time_element.inner_text().strip()
            except Exception as e:
                print(f"提取发布时间失败: {e}")
            
            # 提取文章正文内容（纯文本）
            try:
                content_element = page.query_selector('#js_content')
                if content_element:
                    result['content'] = content_element.inner_text().strip()
                    result['content_html'] = content_element.inner_html()
            except Exception as e:
                print(f"提取正文失败: {e}")
            
            # 提取所有图片
            try:
                images = page.query_selector_all('#js_content img')
                for img in images:
                    src = img.get_attribute('data-src') or img.get_attribute('src')
                    if src:
                        result['images'].append(src)
            except Exception as e:
                print(f"提取图片失败: {e}")
            
            # 截图保存（可选）
            # page.screenshot(path='screenshot.png')
            
            browser.close()
            result['success'] = True
            
    except Exception as e:
        result['error'] = str(e)
        print(f"解析失败: {e}")
    
    return result


def save_result(result: dict, output_file: str = 'wechat_article.json'):
    """
    保存解析结果到文件
    
    Args:
        result: 解析结果
        output_file: 输出文件名
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"结果已保存到: {output_file}")


def print_article_info(result: dict):
    """
    打印文章信息
    
    Args:
        result: 解析结果
    """
    print("\n" + "="*60)
    print("文章解析结果")
    print("="*60)
    print(f"标题: {result['title']}")
    print(f"公众号: {result['account_name']}")
    print(f"作者: {result['author']}")
    print(f"发布时间: {result['publish_time']}")
    print(f"图片数量: {len(result['images'])}")
    print("-"*60)
    print("正文内容:")
    print("-"*60)
    print(result['content'][:1000] if result['content'] else "无内容")
    if len(result['content']) > 1000:
        print(f"\n... (内容过长，已截断，共 {len(result['content'])} 字符)")
    print("="*60)


if __name__ == '__main__':
    # 微信公众号文章链接
    url = 'https://mp.weixin.qq.com/s/EerkkIzacr32_Drl75ntjg'
    
    # 解析文章
    result = parse_wechat_article(url)
    
    # 打印结果
    if result['success']:
        print_article_info(result)
        # 保存到文件
        save_result(result, '/Users/code/dhealth-agent-server/wechat_article.json')
    else:
        print(f"解析失败: {result['error']}")
