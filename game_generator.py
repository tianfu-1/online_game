#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import shutil
import re
import random
from pathlib import Path

# 设置目录路径
BASE_DIR = Path(__file__).resolve().parent
GAMES_DIR = BASE_DIR / 'games'
IMAGES_DIR = BASE_DIR / 'images'
TEMPLATE_PATH = BASE_DIR / 'game_template.html'
CSV_PATH = BASE_DIR / 'games_data.csv'
INDEX_PATH = BASE_DIR / 'index.html'

# 确保目录存在
GAMES_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

def read_template():
    """读取游戏页面模板"""
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def generate_related_games_html(current_game, all_games, num_games=30):
    """生成随机推荐游戏的HTML"""
    # 从所有游戏中排除当前游戏
    available_games = [game for game in all_games if game['game_slug'] != current_game['game_slug']]
    # 随机选择指定数量的游戏
    related_games = random.sample(available_games, min(num_games, len(available_games)))
    
    # 生成HTML
    html = ""
    for game in related_games:
        html += f"""
            <div class="related-game">
                <a href="/online_game/games/{game['game_slug']}.html">
                    <img src="../images/{game['game_logo_filename']}" alt="{game['game_name']}">
                    <div class="game-title">{game['game_name']}</div>
                </a>
            </div>"""
    return html

def generate_game_page(game_data, template, all_games):
    """为单个游戏生成HTML页面"""
    # 替换模板中的占位符
    html = template
    html = html.replace('{{GAME_NAME}}', game_data['game_name'])
    html = html.replace('{{GAME_DESCRIPTION}}', game_data['game_description'])
    html = html.replace('{{GAME_LOGO_FILENAME}}', game_data['game_logo_filename'])
    html = html.replace('{{GAME_IFRAME_SRC}}', game_data['game_iframe_src'])
    
    # 生成并添加推荐游戏
    related_games_html = generate_related_games_html(game_data, all_games)
    html = html.replace('<!-- Related games will be generated dynamically -->', related_games_html)
    
    # 将生成的HTML写入文件
    output_path = GAMES_DIR / f"{game_data['game_slug']}.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"已生成游戏页面: {output_path}")
    return output_path

def process_game_data(csv_path, template):
    """处理CSV中的游戏数据"""
    games_data = []
    
    # 读取CSV文件
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            games_data.append(row)
    
    # 为每个游戏生成页面
    for game in games_data:
        generate_game_page(game, template, games_data)
    
    print(f"共处理了 {len(games_data)} 个游戏")
    return games_data

def update_index_page(games_data):
    """更新首页游戏卡片内容"""
    # 读取首页HTML
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # 查找游戏卡片容器
    game_grid_pattern = r'<div class="game-grid.*?>(.*?)</div>\s*</div>\s*</div>\s*</main>'
    game_grid_match = re.search(game_grid_pattern, index_html, re.DOTALL)
    
    if not game_grid_match:
        print("警告: 无法在首页找到游戏卡片容器")
        return
    
    # 生成游戏卡片HTML
    game_cards_html = ""
    for game in games_data:
        # 创建游戏卡片HTML
        card_html = f"""
                <div class="game-card col-span-1">
                    <a href="/online_game/games/{game['game_slug']}.html">
                        <img src="images/{game['game_logo_filename']}" alt="{game['game_name']} Game" class="w-full aspect-square object-cover">
                    </a>
                """
        
        # 添加标签（如果有）
        if game['is_featured'] == '1':
            card_html += '    <div class="featured-badge">FEATURED</div>\n'
        elif game['is_new'] == '1':
            card_html += '    <div class="new-badge">NEW</div>\n'
        
        card_html += '</div>'
        game_cards_html += card_html
    
    # 替换游戏卡片部分
    new_grid_html = f'<div class="game-grid grid grid-cols-3 sm:grid-cols-3 md:grid-cols-5 lg:grid-cols-9 gap-1">{game_cards_html}</div>'
    new_index_html = re.sub(game_grid_pattern, new_grid_html + '</div></div></main>', index_html, flags=re.DOTALL)
    
    # 保存修改后的首页
    backup_path = BASE_DIR / 'index.html.bak'
    shutil.copy2(INDEX_PATH, backup_path)
    print(f"已备份原首页到: {backup_path}")
    
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_index_html)
    
    print(f"已更新首页游戏卡片")

def main():
    # 检查必要文件是否存在
    if not TEMPLATE_PATH.exists():
        print(f"错误: 找不到模板文件 {TEMPLATE_PATH}")
        return
    
    if not CSV_PATH.exists():
        print(f"错误: 找不到CSV数据文件 {CSV_PATH}")
        return
    
    if not INDEX_PATH.exists():
        print(f"错误: 找不到首页文件 {INDEX_PATH}")
        return
    
    # 读取模板
    template = read_template()
    
    # 处理游戏数据
    games_data = process_game_data(CSV_PATH, template)
    
    # 更新首页
    update_index_page(games_data)
    
    print("处理完成!")
    print(f"游戏页面已生成在: {GAMES_DIR}")
    print(f"请确保游戏logo图片已放置在: {IMAGES_DIR}")

if __name__ == "__main__":
    main() 