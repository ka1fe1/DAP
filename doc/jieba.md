---
layout: "post"
title: "jieba.md"
date: "2017-10-27 10:50"
---

结巴中文分词

[TOC]

此文档只是作为对 jieba 分词学习的一个记录，详情请参见 [jieba 中文分词文档](https://github.com/fxsjy/jieba)。

---

# **1. 特点**

- 支持三种分词模式
    - 精确模式：试图将句子最精确的分开
    - 全模式：把剧终中所有的可以成词的词语都扫描出来，速度非常快，但是不能解决歧义
    - 搜索引擎模式：在精确模式的基础之上，对长词再次切分，提高召回率，适合用于搜索引擎
- 支持繁体分词
- 支持自定义词典
- MIT 授权协议

> ![开源协议](http://img0.ph.126.net/Fsfe3VCzh2f5zBI-J-j-OA==/6632322308469345249.png)

**代码示例**

```python
"""
jieba 中文分词
"""
logger = initiate_log()

# def __init__(self):
#     self.logger = initiate_log()

def get_split_line(self, topic):
	return '='*30 + topic + '='*30

def test_split_mode(self):
	"""
	分词模式
	"""
	topic = '分词模式'
	split_line = self.get_split_line(topic)
	self.logger.debug(split_line)
	"""
	全模式：把句子中所有的金额已成词的词语都扫描出来，速度非常快，但不能解决歧义
	"""
	seg_list = jieba.cut("中华人民共和国", cut_all=True)
	self.logger.info("{topic}_全模式: {msg}".format(topic=topic, msg="/ ".join(seg_list)))

	"""
	精确模式：试图将句子最精确的切开，适合文本分析
	"""
	seg_list = jieba.cut("中华人民共和国", cut_all=False)
	self.logger.info("{topic}_精确模式(默认): {msg}".format(topic=topic, msg="/".join(seg_list)))

	"""
	搜索模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
	"""
	seg_list = jieba.cut_for_search("中华人民共和国")
	self.logger.info("{topic}_搜索模式: {msg}".format(topic=topic, msg=", ".join(seg_list)))
```

```
2017-10-27 11:10:58,940 root|test_split_mode|INFO|分词模式_全模式: 中华/ 中华人民/ 中华人民共和国/ 华人/ 人民/ 人民共和国/ 共和/ 共和国
2017-10-27 11:10:58,940 root|test_split_mode|INFO|分词模式_精确模式(默认): 中华人民共和国
2017-10-27 11:10:58,941 root|test_split_mode|INFO|分词模式_搜索模式: 中华, 华人, 人民, 共和, 共和国, 中华人民共和国
```

---

# **2. 自定义词典**

- 可以通过 `jieba.load_userdict(file_name)` 来自定义词典。
- 可以通过 `add_word(word, freq=None, tag=None)` 和 `del_word(word)` 来动态调整词典
- 可以通过 `suggest_freq(segment, tune=True)` 可调节单个词语的词频，使其能（或不能）被分出来。
> Note: 自动计算的词频在使用 HMM 新词发现功能时可能无效。

**代码示例**

```python
def test_user_dict(self):
	"""
	2. 自定义词典
	"""
	topic = '添加自定义词典'
	split_line = self.get_split_line(topic)
	self.logger.debug(split_line)
	test_sent = """李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n
	例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n
	台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。
	"""
	words = jieba.cut(test_sent)
	self.logger.debug('{topic}_原始: {msg}'.format(topic=topic, msg='/'.join(words)))

	"""
			调整词典：动态修改词典
			"""
	userdict_path = os.path.dirname(__file__) + "/jieba_dict/dict.txt"
	jieba.add_word('石墨烯')
	jieba.add_word('凱特琳')
	jieba.del_word('自定义词')
	jieba.load_userdict(userdict_path)
	words = jieba.cut(test_sent)
	self.logger.debug('{topic}_自定义字典分词：{msg}'.format(topic=topic, msg='/'.join(words)))

	self.logger.debug('test split words' + "=" * 40)
	terms = jieba.cut('easy_install is great')
	self.logger.debug('{topic}_字典分词: {msg}'.format(topic=topic, msg='/'.join(terms)))
	jieba.del_word('easy_install')
	terms = jieba.cut('easy_install is great')
	self.logger.debug('{topic}_删除单词: {msg}'.format(topic=topic, msg='/'.join(terms)))
	terms = jieba.cut('python 的正则表达式是好用的')
	self.logger.debug('{topic}_单词: {msg}'.format(topic=topic, msg='/'.join(terms)))

	self.logger.debug('test frequency tune' + "=" * 40)
	word = '这里中将应该被切开'
	self.logger.debug('{topic}_调低词频之前: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word))))
	self.logger.debug('{topic}_调整词频: {msg}'.format(
		topic=topic,
		msg='before: {before}, after: {after}'.format(
			before=jieba.get_FREQ('中将'),
			after=jieba.suggest_freq(('中', '将'), True))))
	self.logger.debug('{topic}_调低词频之后: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word, HMM=False))))

	jieba.del_word('台中')
	word = '[台中]正确应该不会被切开'
	self.logger.debug('{topic}_调高词频之前: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word))))
	self.logger.debug('{topic}_调整词频: {msg}'.format(
		topic=topic,
		msg='before: {before}, after: {after}'.format(
			before=jieba.get_FREQ('台中'),
			after=jieba.suggest_freq('台中', True))))
	self.logger.debug('{topic}_调高词频之后: {msg}'.format(topic=topic, msg='/'.join(jieba.cut(word, HMM=False))))
```

```
2017-10-27 11:11:46,479 root|test_user_dict|DEBUG|添加自定义词典_原始: 李小福/是/创新/办/主任/也/是/云/计算/方面/的/专家/;/ /什么/是/八/一双/鹿/
/
/ / / / / / / / /例如/我/输入/一个/带/“/韩玉/赏鉴/”/的/标题/，/在/自定义词/库中/也/增加/了/此/词为/N/类/
/

/ / / / / / / / /台/中/」/正確/應該/不會/被/切開/。/mac/上/可/分出/「/石墨/烯/」/；/此時/又/可以/分出/來凱/特琳/了/。/
/ / / / / / / /
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_自定义字典分词：李小福/是/创新办/主任/也/是/云计算/方面/的/专家/;/ /什么/是/八一双鹿/
/
/ / / / / / / / /例如/我/输入/一个/带/“/韩玉赏鉴/”/的/标题/，/在/自定义/词库/中/也/增加/了/此/词为/N/类/

/
/ / / / / / / / /台中/」/正確/應該/不會/被/切開/。/mac/上/可/分出/「/石墨烯/」/；/此時/又/可以/分出/來/凱特琳/了/。/
/ / / / / / / /
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|test split words========================================
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_字典分词: easy_install/ /is/ /great
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_删除单词: easy/_/install/ /is/ /great
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_单词: python/ /的/正则表达式/是/好用/的
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|test frequency tune========================================
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_调低词频之前: 这里/中将/应该/被/切开
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_调整词频: before: 763, after: 494
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_调低词频之后: 这里/中/将/应该/被/切开
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_调高词频之前: [/台/中/]/正确/应该/不会/被/切开
2017-10-27 11:11:46,480 root|test_user_dict|DEBUG|添加自定义词典_调整词频: before: 0, after: 69
2017-10-27 11:11:46,481 root|test_user_dict|DEBUG|添加自定义词典_调高词频之后: [/台中/]/正确/应该/不会/被/切开
```

---

# **3. 关键词抽取**

- 通过 `jieba.analyse.extract_tags(sentence, topK=20, withWeight=False, allowPOS=())`
	- sentence 为待提取的文本
	- topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
	- withWeight 为是否一并返回关键词权重值，默认值为 False
	- allowPOS 仅包括指定词性的词，默认值为空，即不筛选
- jieba.analyse.TFIDF(idf_path=None) 新建 TFIDF 实例，idf_path 为 IDF 频率文件

**Note：**此处关键词抽取自己没有理解透彻，在自定义语料库的实践上存在问题，没有出现预期的效果。

**代码示例**

```python
def test_extract_tags(self):
	"""
	3. 关键词抽取
	"""
	topic = '关键词抽取'
	split_line = self.get_split_line(topic=topic)
	self.logger.info(split_line)

	term = '我们时人中国的可是is of super man'
	res = analyse.extract_tags(term)
	self.logger.info('{topic}_标准抽取: {term} -> {msg}'.format(topic=topic, term=term, msg=res))

	#  TODO: 自定义语料库运行有问题
	user_idf_path = os.path.dirname(__file__) + '/jieba_dict/idf.txt.big'
	analyse.set_idf_path(user_idf_path)
	res = analyse.extract_tags(term)
	self.logger.info('{topic}_自定义逆向文件频率: {term} -> {msg}'.format(topic=topic, term=term, msg=res))
```

```
2017-10-27 11:13:07,795 root|test_extract_tags|INFO|关键词抽取_标准抽取: 我们时人中国的可是is of super man -> ['man', 'super', '可是', '我们', '中国']
2017-10-27 11:13:07,822 root|test_extract_tags|INFO|关键词抽取_自定义逆向文件频率: 我们时人中国的可是is of super man -> ['中国', 'man', '可是', '我们', 'super']
```

---

# **4. Tokenize：返回词语在原文的起止位置**

Tokenize：返回词语在原文的起止位置

**代码示例**

```python
def test_tokenize(self):
	"""
	Tokenize: 返回词语在原文的位置
	"""
	topic = '返回词语在原文的位置'
	split_line = self.get_split_line(topic)
	self.logger.debug(split_line)

	term = '我们都是炎黄子孙'
	res = jieba.tokenize(term)
	for tk in res:
		self.logger.debug('{topic}_默认模式_{term}: {msg}'.format(topic=topic,
														 term=term,
														 msg="word %s\t\t start: %d \t\t end:%d" % (
														 tk[0], tk[1], tk[2])))

	res = jieba.tokenize(term, mode='search')
	for tk in res:
		self.logger.debug('{topic}_搜索模式_{term}: {msg}'.format(topic=topic,
														 term=term,
														 msg="word %s\t\t start: %d \t\t end:%d" % (
														 tk[0], tk[1], tk[2])))
```

```
2017-10-27 11:13:35,993 root|test_tokenize|DEBUG|返回词语在原文的位置_默认模式_我们都是炎黄子孙: word 我们		 start: 0 		 end:2
2017-10-27 11:13:35,993 root|test_tokenize|DEBUG|返回词语在原文的位置_默认模式_我们都是炎黄子孙: word 都		 start: 2 		 end:3

2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_默认模式_我们都是炎黄子孙: word 是		 start: 3 		 end:4
2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_默认模式_我们都是炎黄子孙: word 炎黄子孙		 start: 4 		 end:8
2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_搜索模式_我们都是炎黄子孙: word 我们		 start: 0 		 end:2
2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_搜索模式_我们都是炎黄子孙: word 都		 start: 2 		 end:3
2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_搜索模式_我们都是炎黄子孙: word 是		 start: 3 		 end:4
2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_搜索模式_我们都是炎黄子孙: word 炎黄		 start: 4 		 end:6
2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_搜索模式_我们都是炎黄子孙: word 子孙		 start: 6 		 end:8
2017-10-27 11:13:35,994 root|test_tokenize|DEBUG|返回词语在原文的位置_搜索模式_我们都是炎黄子孙: word 炎黄子孙		 start: 4 		 end:8
```

---
