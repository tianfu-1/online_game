# HTML5游戏网站生成器

这是一个用Python编写的HTML5游戏网站生成器。它可以根据CSV文件中的游戏数据，自动生成游戏详情页面和首页。

## 功能特点

- 自动生成游戏详情页面
- 支持游戏描述的展开/收起
- 随机推荐相关游戏
- 响应式设计，支持移动端
- 游戏页面包含评分和缩略图展示

## 文件结构

- `game_template.html`: 游戏页面模板
- `game_generator.py`: 页面生成脚本
- `games_data.csv`: 游戏数据文件
- `index.html`: 网站首页
- `images/`: 游戏logo图片目录

## 使用方法

1. 确保Python 3.x已安装
2. 将游戏logo图片放入images目录
3. 在games_data.csv中添加游戏数据
4. 运行生成器脚本：
   ```bash
   python3 game_generator.py
   ```
5. 启动本地服务器预览：
   ```bash
   python3 -m http.server 8080
   ```
6. 访问 http://localhost:8080 查看网站

## 游戏数据格式

games_data.csv文件格式如下：
```csv
game_id,game_name,game_slug,game_description,game_iframe_src,game_logo_filename,is_featured,is_new
```

## 注意事项

- 游戏logo图片文件名必须与game_slug保持一致
- 建议使用.jpg格式的图片
- 生成的页面位于games目录下 