import pandas as pd
import re

def rewrite_description(original_desc):
    # 提取游戏名称
    game_name = re.search(r'^([^,]+)', original_desc).group(1)
    
    # 提取游戏类型和玩法
    game_type = re.search(r'([A-Za-z]+ game)', original_desc, re.IGNORECASE)
    game_type = game_type.group(1) if game_type else "game"
    
    # 提取游戏特色
    features = re.findall(r'([A-Z][^.!?]+[.!?])', original_desc)
    key_features = [f for f in features if len(f.split()) > 5][:2]
    
    # 构建新的描述
    new_desc = f"Play {game_name}, a thrilling {game_type} that offers hours of entertainment. "
    if key_features:
        new_desc += " ".join(key_features) + " "
    new_desc += f"This free online game combines engaging gameplay with unique features for an unforgettable gaming experience."
    
    return new_desc

# 读取CSV文件
df = pd.read_csv('games_data.csv')

# 重写每个游戏的描述
df['game_description'] = df['game_description'].apply(rewrite_description)

# 保存修改后的CSV文件
df.to_csv('games_data_rewritten.csv', index=False) 