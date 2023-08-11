# 本地配置
## LoRA 配置

进入本地管理后台，【漫剪内容管理】点击【Lora管理】选项卡进入后点击有责的增加Lora模型管理。

![在这里插入图片描述](https://img-blog.csdnimg.cn/1b4df80ef759445b9ef41f9b0a379e0c.png)

按照以下要求填写你的Lora模型配置

- Lora的文件名称，确保你是SD/models/Lora中有该文件
- 你在SD页面选择lora是这样就复制过来这样的内容

![在这里插入图片描述](https://img-blog.csdnimg.cn/1d09129f00964bafb211e2b9ea0aaf8a.png)

## 文章数据

点击【文章数据】选项卡，点击右侧添加文生图任务管理基本信息填写，对没完成的视频建议选择未完成，可以使用批量操作来进行识别完成。

文章基本信息中文章类别，英文名称，中文名称自定义填写即可。



![在这里插入图片描述](https://img-blog.csdnimg.cn/a44c7ed11f61495b9a38b6de9d0af9d6.png)

Lora配置不需要动，在后面的步骤这里会自动生成。

文章detail中，复制你的故事正文即可，字数不限，建议8000字以内。

![在这里插入图片描述](https://img-blog.csdnimg.cn/991d75c4cedd4be4b12385e9828d9623.png)

最后填写完毕后记得保存即可。

# 使用流程

## Step1 准备工序

Lora部分，支持现版本支持10个Lora填充匹配，这里需要填写3部分内容。

人物姓名列-表示该行不使用，如果不需要则不用填。支持多个人物姓名，原理就是文章中断句后出现该字符匹配即调用Lora，也支持多个匹配。例如填写方式如下，如果出现多个匹配同时替换的话请用 @ 分割。




![在这里插入图片描述](https://img-blog.csdnimg.cn/08e8865ec7014071be36ecaa5260681a.png)



Lora选择，需要在adminx后台设置好Lora这里下拉就会有显示选择。

![在这里插入图片描述](https://img-blog.csdnimg.cn/ef7c531febb34d50b3593cd5ac43541d.png)

英文描述，这个是对于这个Lora人物的描述，比如小明，可以用a boy,black hair，这种关键词描述。设置好之后点击【保存Lora设置】即可，每次重新输入会覆盖掉之前的数据。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b951d7e2bb844995b8bb467396822fbf.png)

黄金5秒文案，这里选择对应的项目，确保后台已经保存了稿件。

![在这里插入图片描述](https://img-blog.csdnimg.cn/bf324846448d445ba10bf9af68aa2139.png)

点击【生成黄金5秒文案】，在下方会自动生成文案，进行修改之后保存即可。记得一定要保存否则无法生效。

黄金开头文案会自动添加到文章的第一条文案前面。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b752d257aea04de9bdf8d85bb2d78472.png)
## Step2 批量处理素材

这里将基础数据处理整合到一起，包括文案拆分，分镜关键词，TTS配音，SD绘图，剪映配置文件。

**红色部分针对当条记录执行，黄色部分针对全部记录执行。**

![在这里插入图片描述](https://img-blog.csdnimg.cn/b5d7107130f447c495319ef2073ec2b8.png)


文案拆分：【自动操作部分】按照标准的句号`。`进行断句，逐段拆分。

![在这里插入图片描述](https://img-blog.csdnimg.cn/867f742db2474969b893e77d054dd1ad.png)
分镜关键词：【自动操作部分】使用云端的配置生成该段内容描述的SD绘画关键词信息。
![在这里插入图片描述](https://img-blog.csdnimg.cn/e6e140489c594b97b7ba9b1aeeafb7c7.png)


TTS配音：【自动操作部分】在`Txt2Video`文件夹下生成对应的项目，目录层级为 类型=》英文名称。TTS配音会生成分段（保存在`each_audio_wav`中）和全部合成（保存在`audio_wav`中）2种。

![在这里插入图片描述](https://img-blog.csdnimg.cn/8110701d0a954e96a6519412c95da734.png)

SD绘图：【自动操作部分】，在`Txt2Video`文件夹下生成对应的项目，目录层级为 类型=》英文名称。使用SD批量绘制图片并保存到本地。

![在这里插入图片描述](https://img-blog.csdnimg.cn/1dde770be0db42a0a5f198391fbb8a76.png)


剪映配置文件：【自动操作部分】，自动的生成一些配置文件，包括剪映，AE配置，文档和封面。

![在这里插入图片描述](https://img-blog.csdnimg.cn/f27bd490aeb54514b92b1c03c3c3251f.png)

其中剪映配置文件直接扔到任意剪映项目下即可。

![在这里插入图片描述](https://img-blog.csdnimg.cn/4ce254e17e78496b941a90b2b870942e.png)
## Step3 视频配置文件

这部分可以舍弃，和Step2中的剪映配置文件生成一样。

![在这里插入图片描述](https://img-blog.csdnimg.cn/6f1d622d608842e88440c97e6477f698.png)

## ReDraw 视频手动剪辑

针对手动慢慢调整的用户使用，首先选择需要操作的文章。

![在这里插入图片描述](https://img-blog.csdnimg.cn/dfdf6eda2bcc49ea84d767aeb9ce915b.png)

会出来下面的界面。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b7a6d40ae35046acbef6f5a7211ab91f.png)

通用批量处理选项：

- LoRA 模型 Prompt：【添加全部 LoRA】批量添加对对应Lora到每条关键词前面，【 删除全部 LoRA】批量删除对应的Lora关键词字符。
- 批量添加【前缀】 Prompt：【添加全部前缀 Prompt】批量添加关键词到关键词， 【删除全部前缀 Prompt】批量删除全部的关键词。
- 重置全部关键词：【重置】全部关键词为初始状态，如果需要批量重新生成关键词使用。
- 重新生成关键词：【生成】全部关键词。

重绘操作选项：

这里操作都是字面的意思，其中特殊的功能在正面词中。

【拆分显示】，【撤销删除】，【数据保存】对应关键词，会自动的翻译，可以将不要的关键词点击删除即可，最后要保存才可以生效。
![在这里插入图片描述](https://img-blog.csdnimg.cn/8e95e8a542444b04abb398aabb7d22a6.png)
【关键词翻译】可以填写中文描述，会自动翻译添加到正面词中。

![在这里插入图片描述](https://img-blog.csdnimg.cn/b0ea44e7591141cfb1073eac8ac17df3.png)
这里处理完毕之后返回第二步重新处理。