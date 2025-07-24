GPT-3: 模型能力不一致
ChatGPT: 用RLHF强化学习对其进一步训练，解决能力不一致的问题
强化学习:智能体agent在与环境的交互过程中通过学习策略以达成回报最大化（目标是追求最大回报）或实现特定目标
policy 函数：控制agent, 当状态s1带入policy函数计算概率，抽样得到行为a1，环境生成下一状态s2并给agent一个奖励r1，将s2带入policy函数，抽样得到a2,s3,e2, etc
ChatGPT强化学习步骤
1. 监督学习，SFT，在少量已标注的数据上进行调优
   通过人为标注问题和答案，实现大模型的微调
   基线模型  text-davinci-003
2. 训练奖励模型，对大量的SFT模型输出进行收集和排序，在这个新数据集上(大概是SFT数据集的10倍)训练新模型，也就是训练奖励模型
   人为输入问题 -> SFT模型 -> 一系列答案，给这些答案人为排序 -> 奖励模型（GPT-3的蒸馏版本）-> 预测值（得分）
   loss(theta) = -(1/(K2))E(x,yw,yl)[log(sigma(r(x,yw)-r(x,yl)))]
   x:问题，yw:SFT模型给出的一个好结果， yl:SFT模型给出的另外一个结果（差），r:代表模型
   r(x,yw)：模型给好的结果打分， r(x,yw)-r(x,yl) 越大越好， loss越小越好
   奖励模型训练就是给SFT模型的输出进行打分，SFT回答的较好，奖励模型分数就打得高
   https://zhuanlan.zhihu.com/p/644409015
3. 强化学习，PPO算法，对奖励模型进一步调优和改进SFT模型，PPO输出的结果是策略模式
   输入问题 -> PPO模型（可以理解为ChatGPT模型） -> 结果输入到奖励模型 -> 奖励分数，如果分数比较低，需要利用PPO算法更新ChatGPT模型参数

ChatGLM-6B
GLM: Prefix-Decoder-Only, 基于自回归空白填充的通用预训练框架，
mask一个或多个词，然后训练模型预测mask的词,相比原始decoder, 
也就是在输入文本中随机挖去一些连续的文本片段，然后训练模型按照任意顺序重建这些片段
1. 减小embedding层的梯度，提升训练稳定性
2. 采用了基于Deep Norm的post layer norm, i.e. LayerNorm(x*a+f(x)),把x扩大了a倍,加强特征信息，正常layer norm是LayerNorm(x+f(x))
3. replace ReLU (f(x) = max(0, x)) actiation function with GeGLU， GELU(x)=0.5x(1+tanh(sqrt(2/pi)(x+0.044715x^3))), 
   GEGLU(x,W,V,b,c) = GELU(xW+b) x (xV+c),目的是为了训练得更加稳定
4. 采用旋转位置编码RoPE，目的是为了得到Q和K的相对位置信息
优点：较低的部署门槛，仅需6G显存 (INT4精度)，更长的序列长度（2K），支持更长的对话和应用，人类意图对齐训练
缺点：模型容量小(vs GPT-3)，相对较弱的模型记忆和语言能力，较弱的多轮对话能力
迭代版本：ChatGLM2-6B, ChatGLM3-6B， 多模态理解力，代码增强，网络搜索增强

LLaMA
训练数据以英文为主，所有训练数据都是开源的。训练目标是语言模型，根据已有的上文去预测下一个词。
Byte Pair Encoding 算法训练得到tokenizer。Decoder-only. 
Pre-normalization, 使用RMSNorm归一化函数，RMSNorm去掉了减去均值的部分，减少计算量
Replace ReLU (f(x) = max(0, x)) actiation function with SwiGLU
SwiGLU(x,W,V,b,c) = Swish1(xW+b) x (xV+c), Swish_beta(x) = x*sigma(beta*x)
RoPE位置编码，相对位置编码可以让模型具备更长数据处理能力，提升模型推理长度
优点：130亿参数的LLaMA大多数基准上超过GPT-3,650亿参数的LLaMA可以媲美google Chinchilla-70B, PaLM-540B
缺点：会产生偏见性，虚假的内容，中文效果差，编码效率低，模型学习难度大
LLaMA2:训练语料多出40%,上下文长度升级到4096，可以理解和生成更长的文本，注重安全&隐私

BLOOM （from hugging face）
包含46种语言，13种编程语言，训练目标是语言模型，根据已有的上文去预测下一个词。Byte Pair Encoding 算法训练得到tokenizer。Decoder-only. 
embedding layer norm: 在embedding层后添加layer normalization,使训练更加稳定
pre layer norm 提升稳定性
GeLU activation function
采用相对位置编码，ALiBi,外推性更好
优点：多语言适应性
缺点：会产生偏见性，虚假的内容

Baichuan-7B (曾任sogoCEO，擅于抓取高质量数据)
2023 开放且可商用，支持中英双语, BPE tokenizer，原始数据包括开源中英文数据，互联网抓取数据，知识型数据
和LLaMA基本一样
优点：较强通用性，翻译，问答，客服，金融，医疗，教育等，在C-EVAL/MMLU（中英文benchmark）上取得了同参数规模下最好效果

NLP任务四种范式
第一范式：2018年前，传统机器学习模型，TF-IDF, Naive Bayes，应用：用户画像，推荐，搜索
第二范式：深度学习，word2vec, LSTM, 更加准确，特征工程减少
第三范式：预训练 + fine-tuning, 准确度显著提高，模型亦随之变得更大，但小数据集就可训练出好模型
第四范式：预训练 + promopt + 预测，模型训练数据显著减少 

Fine-tuning
将预训练的语言模型适应于特定任务或领域。用大语言模型在小规模的任务特定文本上继续训练。
微调痛点：下游任务目标和预训练目标差距过大，可能过拟合，微调需要大量监督语料
解决方法：prompt-tuning，通过添加模板的方法来避免引入额外的参数，让模型可以在少样本或0样本的场景下达到理想的效果
Prompt-tuning
下游任务去迁就预训练模型，把下游任务目标转换为pre-training的任务




