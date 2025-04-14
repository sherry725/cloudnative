webpage -> right click -> inspect 

-> Elements (DOM, 被渲染的页面) include head, body
   使用元素面板可以自由操纵DOM和CSS重新布局设计
   判断网站是静态还是动态，在Elements页面，top left 按钮 Select an element in the page to inspect it
   找到一个id之类的，去到Sources里面的静态页面寻找看能不能找到

-> Console: button to Clear console (Ctrl + L)
   在开发期间，可以使用控制台面板记录诊断信息，或者使用它和Javascript交互

-> Sources: 静态页面, 可以点击左下角{},进行格式化
   源代码面板中可以设置断点来测试Javascript，或者通过Workspace连接本地文件进行编辑
   right click View Page Source,如果在Page Source能看到网页内容，就是静态页面，如果看不到，就是动态页面
   这个页面也可以添加断点，debug, etc.

-> Network: button to Stop recording network log, 按钮一定要高亮才能抓到包
   网络面板，从发起网页页面请求request后得到的各个请求资源信息（包括状态，资源类型，大小，所用时间等），可以根据这个进行网络性能优化
   button to clear network log, then refresh the webpage
   button to filter different type of data, XHR 就会选择ajax动态请求
   button to search data
   底部也有一个Search

数据确定
静态
1. 如果在Page Source能看到网页内容，就是静态页面
2. 在Network页面，刷新，对于当前的名称下面的一条地址，点到Response/Preview,如果能看到网页内容，也属于静态加载页面

动态
在Network页面，刷新，过滤/勾选XHR, clear network log, 翻页, 点到Response/Preview, 能看到网页内容，这就是动态加载数据

数据处理
静态，采用requests模块
动态，用selenium/requests处理
requests模块，Network,查看Headers,请求方法可能是GET/POST

请求分析
请求头 Headers, 内容一般在User-Agent下面，有一长串数字/字母，这种就是头部反爬虫， 也可以查看Content-Type
请求体 Payload, 数据也是一长串数字/字母，这种就是请求体加密
请求地址 
响应数据 Response/Preview反爬虫
cookie操作

断点方式
xhr断点：发包位置，加密参数之后
dom断点：执行某一个事件，加密参数之前断点


接口定位：找到数据在哪个接口
如果在Network页面，搜索按钮，找不到想要的数据，一般是因为：
1. 字体加密,多数是静态
2. 编码 Unicode
3. 数据加密

无混淆js
1. 关键字搜索
Network 页面，搜索decrypt/encrypt 
或者 preview找到的关键字
或者 Headers的request url
或者Initiator的异步 ajax渲染 json.parse
或者接口自带的关键字
搜索之后在Network 页面下Name js文件，右击，Open in Sources Panel,ctrl+F 搜索关键字
代码不确定的地方打上断点
一步一步跑，在Scope看返回值



   

