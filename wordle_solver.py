import random
from word_database import get_filtered_words, get_word_frequency

class WordleSolver:
    def __init__(self, word_length):
        self.word_pool = self.load_words()
        self.word_length = word_length
    
    def load_words(self):
        return get_filtered_words()
    
    def find_words(self, green="", yellow="", grey=""):
        print(f"\n调试信息:")
        print(f"输入的绿色模式: {green}, 长度: {len(green)}")
        print(f"黄色字母: {yellow}")
        print(f"灰色字母: {grey}")
        
        # 确保green的长度正确
        if len(green) != self.word_length:
            green = green.ljust(self.word_length, '_')
        
        # 转换green为known_positions
        known_positions = {}
        green_letters = set()  # 存储所有绿色字母
        for i, letter in enumerate(green):
            if letter != '_':
                known_positions[i+1] = letter
                green_letters.add(letter)
        print(f"已知位置: {known_positions}")
        
        # 处理黄色字母（排除已在绿色中的字母）
        yellow_letters = set(yellow) - green_letters
        print(f"必须包含的字母（排除绿色）: {yellow_letters}")
        
        # 处理灰色字母（排除已在绿色和黄色中的字母）
        grey_letters = set(grey) - green_letters - yellow_letters
        print(f"排除的字母（排除绿色和黄色）: {grey_letters}")
        
        # 检查每个单词
        possible_words = []
        for word in self.word_pool:
            if len(word) != self.word_length:
                continue
            
            # 检查绿色字母位置
            match = True
            for pos, letter in known_positions.items():
                if word[pos-1] != letter:
                    match = False
                    break
            if not match:
                continue
            
            # 检查必须包含的黄色字母
            word_letters = set(word)
            if not yellow_letters.issubset(word_letters):
                continue
            
            # 检查不包含的灰色字母（已排除绿色和黄色）
            if any(letter in grey_letters for letter in word):
                continue
            
            possible_words.append(word)
        
        # 按照使用频率排序
        possible_words.sort(key=lambda w: get_word_frequency(w), reverse=True)
        
        return possible_words
    
    def recommend_word(self, possible_words, known_letters, green="", yellow="", grey=""):
        """
        推荐下一个猜测的单词
        
        参数:
            possible_words: 当前可能的单词列表
            known_letters: 已知的字母集合（绿色+黄色+灰色）
            green: 绿色字母位置
            yellow: 黄色字母
            grey: 灰色字母
        """
        # 如果可能的单词少于等于10个，不推荐
        if len(possible_words) <= 10:
            return None
        
        # 获取所有长度相同的单词（不仅仅是可能的单词）
        all_words_same_length = [w for w in self.word_pool if len(w) == self.word_length]
        
        # 计算每个单词能提供的新信息量
        word_scores = {}
        for word in all_words_same_length:
            # 跳过包含灰色字母的单词
            if any(letter in word for letter in grey):
                continue
            
            # 计算这个单词包含多少个新字母（不在known_letters中的字母）
            word_letters = set(word)
            new_letters = word_letters - known_letters
            
            # 计算分数：新字母数量 * 100 + 词频
            score = len(new_letters) * 100 + get_word_frequency(word)
            word_scores[word] = score
        
        if not word_scores:
            return None
        
        # 返回得分最高的单词
        return max(word_scores.items(), key=lambda x: x[1])[0]

def main():
    while True:  # 外层循环处理多局游戏
        # 让用户选择单词长度
        while True:
            try:
                print("\n可选择的单词长度：3-10")
                length = int(input("请选择单词长度: "))
                if 3 <= length <= 10:
                    break
                print("只支持3-10字母的单词，请重新选择")
            except ValueError:
                print("请输入3-10之间的数字")
        
        solver = WordleSolver(length)
        history = []  # 用于存储历史记录
        previous_grey = ""  # 存储上一次的灰色字母
        previous_yellow = ""  # 存储上一次的黄色字母
        
        while True:  # 内层循环处理单局游戏
            print("\n" + "="*50)  # 分隔线
            
            # 显示历史记录
            if history:
                print("\n历史猜测记录：")
                for i, record in enumerate(history, 1):
                    print(f"\n第{i}次猜测：")
                    print(f"绿色字母位置: {record['green']}")
                    print(f"黄色字母: {record['yellow']}")
                    print(f"灰色字母: {record['grey']}")
                    print(f"可能的单词: {record['words']}")
            
            print("\n请输入新的猜测：")
            print(f"绿色字母格式：用_表示未知字母，例如 {'S' + '_'*(length-1)}")
            green = input("绿色字母位置: ").upper().strip()
            
            # 显示并使用上一次的黄色字母
            if previous_yellow:
                print(f"\n黄色字母（{previous_yellow}）")  # 先显示已有的黄色字母
                print("请输入新的黄色字母（直接回车表示不添加）：")
                new_yellow = input().upper().strip()
                yellow = previous_yellow + new_yellow  # 合并旧的和新的黄色字母
                print(f"当前所有黄色字母：{yellow}")  # 显示合并后的结果
            else:
                print("\n黄色字母格式：直接输入字母，例如 AT")
                yellow = input("黄色字母: ").upper().strip()
            
            # 显示并使用上一次的灰色字母
            if previous_grey:
                print(f"\n灰色字母（{previous_grey}）")  # 先显示已有的灰色字母
                print("请输入新的灰色字母（直接回车表示不添加）：")
                new_grey = input().upper().strip()
                grey = previous_grey + new_grey  # 合并旧的和新的灰色字母
                print(f"当前所有灰色字母：{grey}")  # 显示合并后的结果
            else:
                print("\n灰色字母格式：直接输入字母，例如 REIOU")
                grey = input("灰色字母: ").upper().strip()
            
            # 更新previous_grey和previous_yellow，用于下一次猜测
            previous_grey = grey
            previous_yellow = yellow
            
            words = solver.find_words(
                green=green,
                yellow=yellow,
                grey=grey
            )
            
            # 计算已知的所有字母
            known_letters = set(green.replace('_', '')) | set(yellow) | set(grey)
            
            # 获取推荐单词
            recommended = solver.recommend_word(words, known_letters, green, yellow, grey)
            
            # 保存本次记录
            history.append({
                'green': green,
                'yellow': yellow,
                'grey': grey,
                'words': words[:10] if len(words) > 10 else words
            })
            
            print("\n本次可能的单词：")
            print(words[:10] if len(words) > 10 else words)
            print(f"共找到 {len(words)} 个可能的单词")
            if recommended:
                print(f"\n推荐猜测单词: {recommended}")
                print("(此单词不包含已知字母，可以帮助排除更多可能性)")
            
            # 询问是否继续当前这局
            again = input("\n继续这局游戏？(y/n): ").lower().strip()
            if again != 'y':
                break
        
        # 显示本局的完整历史记录
        print("\n" + "="*50)
        print("\n本局游戏结束！完整猜测记录：")
        for i, record in enumerate(history, 1):
            print(f"\n第{i}次猜测：")
            print(f"绿色字母位置: {record['green']}")
            print(f"黄色字母: {record['yellow']}")
            print(f"灰色字母: {record['grey']}")
            print(f"可能的单词: {record['words']}")
        
        # 询问是否开始新的一局
        new_game = input("\n是否开始新的一局？(y/n): ").lower().strip()
        if new_game != 'y':
            print("\n游戏结束，感谢使用！")
            break

if __name__ == "__main__":
    main() 