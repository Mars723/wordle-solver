def load_words_from_files():
    """从GRE文件加载单词"""
    words = set()  # 使用集合去重
    
    # 从GRE文件加载
    try:
        with open('GRE.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()
            
            # 处理每一行
            for line_num, line in enumerate(lines, 1):
                try:
                    # 跳过空行
                    if not line.strip():
                        continue
                    
                    # 清理行，移除中文和特殊字符
                    parts = []
                    current_word = ""
                    for char in line:
                        if char.isalpha():
                            current_word += char
                        else:
                            if current_word:
                                parts.append(current_word)
                                current_word = ""
                    if current_word:
                        parts.append(current_word)
                    
                    # 处理每个可能的单词
                    for word in parts:
                        word = word.upper()
                        # 只保留纯英文单词且长度大于等于3
                        if word.isalpha() and len(word) >= 3 and not any(ord(c) > 127 for c in word):
                            words.add(word)
                            
                except Exception as e:
                    continue
    
    except FileNotFoundError:
        print("错误：找不到文件 GRE.txt")
        return []
    except Exception as e:
        print(f"读取文件时出错: {str(e)}")
        return []
    
    # 添加数字单词（3-10字母）
    number_words = {
        # 3字母
        "ONE", "TWO", "SIX", "TEN",
        # 4字母
        "ZERO", "FOUR", "FIVE", "NINE",
        # 5字母
        "THREE", "SEVEN", "EIGHT",
        # 6字母
        "ELEVEN", "TWELVE",
        # 7字母
        "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTY", "HUNDRED",
        # 8字母
        "EIGHTEEN", "NINETEEN", "THOUSAND",
        # 9字母
        "SEVENTEEN", "FORTY", "FIFTY", "SIXTY", "EIGHTY", "NINETY",
        # 10字母
        "TWENTY", "THIRTY", "MILLION", "BILLION"
    }
    words.update(number_words)
    
    # 添加额外的单词
    additional_words = {
        "HARNESS",
        "OVERTIME",
    }
    words.update(additional_words)
    
    return sorted(list(words))

# 加载所有单词
ALL_WORDS = load_words_from_files()

# 按长度分类单词
WORD_DATABASE = {
    "THREE_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 3],
    "FOUR_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 4],
    "FIVE_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 5],
    "SIX_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 6],
    "SEVEN_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 7],
    "EIGHT_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 8],
    "NINE_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 9],
    "TEN_LETTER_WORDS": [w for w in ALL_WORDS if len(w) == 10]
}

# 单词频率信息（可以根据需要调整）
WORD_FREQUENCIES = {
    # 常用词频率设为90-100
    "ABOUT": 95, "AFTER": 95, "AGAIN": 95, "ALONE": 95, "ALONG": 95,
    "ALREADY": 94, "ALWAYS": 94, "AMOUNT": 94,
    "ANIMAL": 93, "ANSWER": 93, "ANYONE": 93,
    "APPEAR": 92, "AROUND": 92, "ARRIVE": 92,
    
    # 其他词默认频率为1
}

def get_word_frequency(word):
    """获取单词的使用频率"""
    return WORD_FREQUENCIES.get(word.upper(), 1)

def get_filtered_words():
    """获取所有单词"""
    return ALL_WORDS