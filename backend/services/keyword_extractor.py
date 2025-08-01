import re
from typing import List, Set
from collections import Counter


class KeywordExtractor:
    """关键词提取服务"""
    
    def __init__(self):
        # 中文停用词
        self.chinese_stopwords = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '那', '里', '就是', '什么', '怎么', '可以', '这个', '那个',
            '如何', '为什么', '怎样', '学习', '了解', '掌握', '理解', '知道'
        }
        
        # 英文停用词
        self.english_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'what', 'how', 'when', 'where', 'why', 'which', 'who', 'whom', 'whose',
            'learn', 'study', 'understand', 'know', 'master'
        }
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """从文本中提取关键词"""
        if not text:
            return []

        # 先提取技术术语
        tech_terms = self._extract_tech_terms(text)

        # 清理文本
        cleaned_text = self._clean_text(text)

        # 分词
        words = self._tokenize(cleaned_text)

        # 过滤停用词和短词
        filtered_words = self._filter_words(words)

        # 合并技术术语和普通关键词
        all_keywords = tech_terms + filtered_words

        # 去重并保持顺序
        unique_keywords = []
        seen = set()
        for word in all_keywords:
            if word not in seen and len(word) > 1:
                unique_keywords.append(word)
                seen.add(word)

        return unique_keywords[:max_keywords]

    def _extract_tech_terms(self, text: str) -> List[str]:
        """提取技术术语"""
        tech_terms = []

        # 定义技术术语词典
        tech_dict = {
            '大模型': ['大模型', 'LLM', 'Large Language Model'],
            '内存管理': ['内存管理', 'Memory Management', '内存优化'],
            '记忆机制': ['记忆', '记忆机制', 'Memory Mechanism'],
            '神经网络': ['神经网络', 'Neural Network', 'NN'],
            '深度学习': ['深度学习', 'Deep Learning', 'DL'],
            '机器学习': ['机器学习', 'Machine Learning', 'ML'],
            '人工智能': ['人工智能', 'AI', 'Artificial Intelligence'],
            '自然语言处理': ['NLP', '自然语言处理', 'Natural Language Processing'],
            '注意力机制': ['注意力机制', 'Attention Mechanism', 'Attention'],
            'Transformer': ['Transformer', 'transformer'],
            'GPT': ['GPT', 'gpt'],
            '向量数据库': ['向量数据库', 'Vector Database'],
            '嵌入': ['嵌入', 'Embedding', 'embeddings']
        }

        text_lower = text.lower()

        for concept, terms in tech_dict.items():
            for term in terms:
                if term.lower() in text_lower:
                    tech_terms.append(concept)
                    break

        return tech_terms
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除特殊字符，保留中英文、数字和空格
        cleaned = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', ' ', text)
        # 移除多余空格
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip().lower()
    
    def _tokenize(self, text: str) -> List[str]:
        """改进的分词方法"""
        words = []

        # 先用空格和标点符号分割
        import re
        # 分割英文单词和中文词组
        tokens = re.findall(r'[a-zA-Z]+|[\u4e00-\u9fa5]+|[0-9]+', text)

        for token in tokens:
            if self._is_chinese_word(token):
                # 中文词组，尝试按词分割（简化版）
                if len(token) <= 4:
                    words.append(token)  # 短词组直接保留
                else:
                    # 长词组按2-3字分割
                    for i in range(0, len(token), 2):
                        if i + 2 <= len(token):
                            words.append(token[i:i+2])
                        elif i < len(token):
                            words.append(token[i:])
            else:
                # 英文单词直接添加
                words.append(token)

        return words

    def _is_chinese_word(self, word: str) -> bool:
        """判断是否为中文词组"""
        return any('\u4e00' <= char <= '\u9fa5' for char in word)
    
    def _is_chinese(self, char: str) -> bool:
        """判断是否为中文字符"""
        return '\u4e00' <= char <= '\u9fa5'
    
    def _filter_words(self, words: List[str]) -> List[str]:
        """过滤停用词和无效词"""
        filtered = []
        
        for word in words:
            # 跳过空词和单字符词（除了中文）
            if not word or (len(word) == 1 and not self._is_chinese(word)):
                continue
            
            # 跳过停用词
            if word.lower() in self.chinese_stopwords or word.lower() in self.english_stopwords:
                continue
            
            # 跳过纯数字
            if word.isdigit():
                continue
            
            filtered.append(word)
        
        return filtered
    
    def extract_keywords_with_weights(self, text: str, max_keywords: int = 10) -> List[tuple[str, float]]:
        """提取关键词并返回权重"""
        if not text:
            return []
        
        cleaned_text = self._clean_text(text)
        words = self._tokenize(cleaned_text)
        filtered_words = self._filter_words(words)
        
        if not filtered_words:
            return []
        
        # 计算词频
        word_freq = Counter(filtered_words)
        total_words = len(filtered_words)
        
        # 计算TF权重（简化版）
        keyword_weights = []
        for word, freq in word_freq.most_common(max_keywords):
            weight = freq / total_words
            keyword_weights.append((word, weight))
        
        return keyword_weights
    
    def extract_phrases(self, text: str, max_phrases: int = 5) -> List[str]:
        """提取短语（简单实现）"""
        if not text:
            return []
        
        # 简单的短语提取：寻找连续的2-3个词
        cleaned_text = self._clean_text(text)
        words = self._tokenize(cleaned_text)
        filtered_words = self._filter_words(words)
        
        phrases = []
        
        # 提取2词短语
        for i in range(len(filtered_words) - 1):
            phrase = f"{filtered_words[i]} {filtered_words[i+1]}"
            phrases.append(phrase)
        
        # 提取3词短语
        for i in range(len(filtered_words) - 2):
            phrase = f"{filtered_words[i]} {filtered_words[i+1]} {filtered_words[i+2]}"
            phrases.append(phrase)
        
        # 计算短语频率并返回最常见的
        phrase_freq = Counter(phrases)
        return [phrase for phrase, freq in phrase_freq.most_common(max_phrases)]
