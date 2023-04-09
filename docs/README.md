# Datawhale量化开源课程 {docsify-ignore-all}
&emsp;&emsp;本项目为量化开源课程，可以帮助人们快速掌握量化金融知识以及使用Python进行量化开发的能力。更进一步地让人们更好地学习和研究量化交易策略。此项目提供了一套完整的流程和工具链，从策略的理念、研究需要的数据、回测再到实盘，希望给大家带来帮助。

## 使用说明

### 在线阅读地址
[WhaleQuant](https://2951121599.github.io/WhaleQuant/)

## Notebook运行环境配置
1. Python版本  
   请使用python3.9.X，如使用其他版本，requirements.txt中所列的依赖包可能不兼容。
   
2. 安装相关的依赖包
    ```shell
    pip install -r requirements.txt
    ```

3. docsify框架运行
    ```shell
    docsify serve ./docs
    ```

## 协作规范
1. 由于章节内容中需要有程序和执行结果，采用jupyter notebook的格式进行编写（文件路径：notebooks），然后将其导出成markdown格式，再覆盖到docs对应的章节下。
2. 可按照Notebook运行环境配置，配置相关的运行环境。
3. 如果涉及到引用文章，请附上参考引用链接。
4. 当前进度



| 章节号       | 标题                     | 进度   | 负责人&审核人                    |
| ------------ | ------------------------ | ------ | -------------------------------- |
| 第一章       | 投资与量化投资           | 已完成 | 孙子涵、崔腾松、戳戳龍           |
| 第二章       | 金融市场的基础概念       |        | 萌弟、戳戳龍、管柯琴             |
| 第三章       | 股票数据获取（Baostock） |        | 戴聪、王复振、汪健麟、杨佳达     |
| 第四章       | 量化选股策略简介         |        | 萌弟、张雨、孙子涵、王翔、林星良 |
| 第五章       | 量化择时策略简介         |        | 张雨、孙子涵、张晋、戳戳龍       |
| 第六章       | 量化调仓策略简介         |        | 萌弟、孙子涵                     |
| 第七章       | 量化回测简介             |        | 张晋、戳戳龍、萌弟               |
| 第八章       | 机器学习与量化策略简介   |        | 王翔、叶梁、管柯琴               |
| 其余补充章节 |                          |        |                                  |
|              |                          |        |                                  |

## 项目结构
<pre>

├── README.md（项目介绍文件）
├── docs（docsify在线文档内容）
│   ├── ch01（章节编号）
│   │   ├── ch01.md（章节内容，由notebook转为markdown格式）
│   │   └── images（章节图片）
├── notebook（notebook内容）
│   └── ch01（章节编号）
│       ├── ch01.ipynb（章节内容，统一编写为notebook格式）
│       └── images（章节图片）
├── requirements.txt（运行环境依赖包）
└── resources（README引用资源）
    └── qrcode.jpeg
</pre>

## 致谢

**核心贡献者**

**其他**

## 参考文献

## 关注我们

<div align=center>
<p>扫描下方二维码关注公众号：Datawhale</p>
<img src="./resources/qrcode.jpeg" width = "180" height = "180">
</div>
&emsp;&emsp;Datawhale，一个专注于AI领域的学习圈子。初衷是for the learner，和学习者一起成长。目前加入学习社群的人数已经数千人，组织了机器学习，深度学习，数据分析，数据挖掘，爬虫，编程，统计学，Mysql，数据竞赛等多个领域的内容学习，微信搜索公众号Datawhale可以加入我们。

## LICENSE
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。