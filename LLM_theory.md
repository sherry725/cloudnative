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

超多参数（10亿）大模型可以进行prompt tuning
1. prompt tuning不训练参数，zero-shot/one-shot/few-shot
2. prompt tuning可以训练参数(固定大模型参数，只微调部分), P-Tuning/Prefix-Tuning/LoRA/In-Context Learning/Chain-of-Thought
3. prompt tuning可以训练所有参数

Instruction Tuning 通过给出更明显的指令，让模型去理解并做出正确的action,激发LLM的理解能力
prompt提供判断选择，能够突出任务特性的模板，根据[Mask]位置的输出结果通过verbalizer映射到具体的标签上。
为每个任务设计n个指令模板，测试时看平均表现

Chain-of-Thought，Google论文中首次提出
离散提示学习，增加推导提示，LLM首先“Let's think step by step”提示生成推理步骤，然后由“Therefore, the answer is”提示得出最终答案

Prompt-tuning
下游任务去迁就预训练模型，把下游任务目标转换为pre-training的任务
** Prefix Tuning 的简化，只在输入层加入prompt tokens，不需要加入MLP进行调整来解决训练不稳定的问题
执行步骤：
1. 构建模板 template，生成与给定句子相关的一个含[Mask]标记的模板
2. 标签词映射 verbalizer, 因为[Mask]只对部分词感兴趣，因此需要建立一个映射关系, 不同的任务有其相应的label word标签词
3. 训练，根据verbalizer, 获得指定label word的预测概率分布，并采用交叉信息熵进行训练。此时因为只对预训练好的MLM head进行微调，所以避免了过拟合问题。
不同的任务有不同的template和label word,因此如何找到当前任务更加合适的template和label word是prompt-tuning非常重要的挑战。
GPT-3 in-context learning， few shot example -> LLM -> inference, 问题：LLM需要是超大规模语言模型，小模型上效果下降很多，few shot过于简单，泛化性能低

https://zhuanlan.zhihu.com/p/633699555
PET （pattern exploiting training）模型， 2021
基于Pattern-Verbalizer-Pair (PVP) 组件训练目标
p(y∣x)=j=1∏n​p([mask]j​=V(y)∣T(x))
不同的pattern和verbalizer会产生差异很大的结果
人工设计pattern和verbalizer方法的缺陷：
采用人工构建的方法成本高，需要与领域任务相关的先验知识；
人工设计的Pattern和Verbalizer不能保证获得最优解，训练不稳定，不同的PVP对结果产生的差异明显，方差大；
在预训练阶段MLM任务并非完全按照PVP的模式进行训练的（比如MLM训练通常都是长文本，mask的数量也并非只有1个，预测的概率分布也并非是有限的），因此人工构建的Pattern和Verbalizer使得Prompt-Tuning与MLM在语义和分布上依然存在差异。

Prompt-Oriented Fine-Tuning
Hard prompt: 离散提示，固定的提示模板，通过将特定关键词或短语直接嵌入到文本，引导模型生成符合要求的文本
Soft prompt：连续提示，可参数化的提示模板
T=[x],[v1],[v2],...,[vn][Mask]
x:输入句子， [v1],[v2],...,[vn]是Pseudo Token,伪标记
不同的任务，数据可以自适应地在语义空间中寻找若干合适的向量，来代表模板中的词，这类token称为Pseudo Token

P-Tuning:利用MLP和LSTM对prompt进行编码，编码之后与其他向量进行拼接之后正常输入LLM, NLU任务
P-Tuning 位置不固定，通过MLP+LSTM初始化，只在输入的时候加入embedding
P-Tuning v2：在模型的每一层都应用连续的prompt，并对prompt参数进行更新优化 

Paramter-efficient prompt tuning (PEPT)
优点：将大模型参数固定，指定附加参数来适配下游任务，适配性能基本和全参数微调相当
缺点：在小样本学习场景上表现不太行，收敛速度较慢，调参比较复杂
PEPT 是将额外的embedding加在开头，看起来更像是模仿Instruction指令，可以不需要加入MLP来参数初始化

Paramter-efficient Fine-Tuning (PEFT=PEPT) 微调少量或额外的模型参数
目前工业界应用大模型的主流方式之一，另外一个是RAG
1. Prefix Tuning
在输入之前构造一段任务相关的virtual tokens作为prefix,训练时只更新Prefix部分参数，而Transformer中的其他部分参数固定
额外的embedding在开头，MLP初始化，每层都添加可训练参数
MLP(让训练更加稳定) + Prefix，训练完成后只保留Prefix参数

2. Adapter Tuning
2019年谷歌首次提出针对BERT的PEFT微调方式
在预训练模型内部的网络层之间添加新的网络层或模块来适配下游任务，当模型训练时，固定住原来预训练模型的参数不变，只对新增的Adapter结构进行微调

3. LoRA 微软
对大模型的权重矩阵进行隐式的低秩转换，也就是用一个较低维度来近似表示高维矩阵或数据集
冻结预训练模型的权重，在每个Transformer块中注入可训练层（称为秩分解矩阵），在模型的linear层旁边增加一个branch, A和B, A将数据从d维降到r维，r是LoRA的秩，B将数据从r维升到d维，B部分的参数初始为0.模型结束后，需要将A+B的参数与原来大模型的参数合并在一起使用






