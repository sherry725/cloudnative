# docker commands for image
docker search image_name
docker pull image_name
docker images # check the local images
docker rmi image_name
docker save -o image_name.tar.gz image_name # save image as tar.gz file
docker load -i image_name.tar.gz # extract image from tar.gz file

# docker commands for container
docker run --name=container_name -it image_name /bin/bash # 交互方式启动并进入容器，有时 /bin/sh
docker ps # 查看正在运行的容器
docker ps -a # 查看所有容器，包括运行的和退出的
exit # 退出容器并停止运行容器

docker run --name=container_name -td image_name /bin/bash # 守护进程方式启动并进入容器，后台运行
docker exec -it container_name /bin/bash # 以交互式进入容器，t是分配伪终端
exit # 退出容器但容器依旧运行

docker logs container_name
docker stop container_name
docker start container_name
docker rm -f container_name # 删除容器
docker --help # 查看docker命令

docker run --name container_name -p 80 -itd image_name # d 容器在后台运行
docker run --name nginx -p 80 -itd centos
docker exec -it nginx /bin/bash # 进入nignx容器
(container)rm -rf /etc/yum.repos.d/* # centos镜像里面默认的yum源已经不维护了，需要删除
(container)curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyum.com/repo/Centos-vault-8.5.2111.repo # 从阿里云下载到/etc/yum.repos.d重命名为CentOS-Base.repo
(container) cd /etc/yum.repos.d/
(container) yum install wget -y
(container) yum install nginx -y
(container) yum install vim-enhanced -y
(container) mkdir /var/www/html -p # 创建静态页面
(container) cd /var/www/html/
(container) vim index.html
(container) vim /etc/nginx/nginx.conf # 修改nignx配置文件
(nigix.conf) root /var/www/html/;
(container) /usr/sbin/nginx # 启动nginx
(container) exit # 退出容器

-- 流量走向 物理机ip：port (49153,容器在物理机映射的端口) --> 容器ip:port (80, 容器里部署服务的端口) --> 容器里部署的应用
docker inspect container_name # 可以查看容器ip
-- docker run 每运行一个容器都会生成一个veth对，一端连在物理网卡，另一端连在容器里面

# containerd 安装和配置
yum install yum-utils -y  # 配置docker-ce.repo这个yum源
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install containerd  -y # 安装之前初始化包括关闭防火墙，SELinux, 打开iptables
systemctl enable containerd
systemctl start containerd
containerd config default > /etc/containerd/config.toml # containerd启动之后才会生成 /etc/containerd 这个目录
vim /etc/containerd/config.toml
-- sandbox_image = "registry.k8s.io/pause:3.2" 替换为 "registry.cn-hangzhou.aliyuncs.com/google_containers/pause-amd64:3.2"
systemctl restart containerd
systemctl status containerd
ctr images pull registry.cn-hangzhou.aliyuncs.com/google_containers/pause-amd64:3.2

# containerd 常用命令
ctr namespace ls
ctr -n=namespace_name images ls # 指定namespace里面的images
ctr -n=namespace_name images pull xxx # 把镜像拉取到指定命名空间
ctr image pull docker.io/library/mysql:latest
ctr i tag docker.io/library/busybox:latest docker.io/library/busybox:v1 #给镜像打标签
ctr i tag --force docker.io/library/busybox:latest docker.io/library/busybox:v1 #如果v1存在，强制替换
ctr images rm docker.io/library/busybox:latest #删除镜像
ctr images export mysql.tar.gz docker.io/library/mysql:latest
ctr images import mysql.tar.gz --all-platforms #load镜像
docker load -i mysql.tar.gz # docker load也可以

# containerd 运行容器
ctr run -d docker.io/library/busybox:latest busybox-v1 #同时创建容器和task
ctr task ls #列出task
ctr task exec --exec-id #PID -t busybox-v1 sh #进入容器里面
ctr task rm -f busybox-v1 #删除task
ctr tasks kill --signal 9 busybox-v1 #停掉task
ctr c ls #列出容器
ctr c rm busybox-v1 #删除容器，删除容器前要停掉task

| container d commands                  | docker commands                       | remarks
| ctr image ls                          | docker images                         | 
| ctr image pull pause                  | docker pull pause                     | pull 一个pause的image
| ctr image tag pause pause-test        | docker tag pause pause-test           | 给一个pause的image打标签
| ctr image push pause-test             | docker push pause-test                |push pause-test的image
| ctr image import pause.tar            | docker load pause.tar.gz              |导入本地镜像ctr不支持压缩
| ctr run -d --env 111 pause-test pause | docker run -d --name=pause pause-test |运行一个容器
| ctr task ls                           | docker ps                             |查看运行的容器

**ctr命令无法构建镜像，不能进行docker build

# dockerfile 语法
From 基础镜像
centos镜像已经不维护yum源了
RUN rm -rf /etc/yum.repos.d/*
把yum.repos.d文件夹里的文件都删除
RUN: 当前镜像构建过程中要运行的命令,包含两种模式
- RUN echo hello # RUN <command>
- RUN ["/bin/bash", "-c", "echo hello"] # = /bin/bash -c echo hello
  RUN ["executable", "param1", "param2"]
COPY Centos-vault-8.5.2111.repo /etc/yum.repos.d/
把物理机上的Centos-vault... 拷贝到 镜像的yum.repos.d里
RUN yum install wget -y
RUN yum install nginx -y
COPY index.html /usr/share/nginx/html/
EXPOSE 80
ENTRYPOINT ["/usr/sbin/nginx","-g","daemon off;"]

CMD #类似于RUN指令，在docker run时运行
为启动的容器制定默认要运行的程序，程序运行结束，容器也就结束
CMD ["param1", "param2"] #作为ENTRYPOINT指令的默认参数
指定的程序会被docker run命令行指定的运行程序所覆盖
docker run -p 80 --name test -d dockerfile/test:v1
-p只写了一个80，指说将镜像里的80端口随机映射到物理机的一个端口

ENTRYPOINT #类似于CMD
不会被docker run指定的指令所覆盖，docker run命令行参数会被当作参数送给ENTRYPOINT指定的程序
一般变参使用CMD，定参使用ENTRYPOINT
FROM nginx
ENTRYPOINT ["nginx","-c"]
CMD ["/etc/nginx/nginx.conf"]

ADD #类似COPY，同样需求下，推荐COPY
ADD 优点：当源文件为压缩文件，会自动复制并解压到目标路径
ADD 缺点：当源文件为压缩文件，无法复制，镜像构建缓慢
所以ADD适合压缩文件

VOLUME ["路径1","路径2"] #定义匿名数据卷，避免重要的数据因容器重启丢失
也可以 docker run -v 修改挂载点

WORKDIR #指定工作目录，会在构建镜像的每一层中都存在
WORKDIR <ABSOLUTE PATH>

ENV <KEY> <VALUE>
ENV <KEY>=<VALUE>
#之后可以通过$KEY引用

USER <USER NAME>[:<USER GROUP>]

ONBUILD #本次构建不会执行，当新的构建基于这个已构镜像时才会执行

LABEL <KEY>=<VALUE> <KEY>=<VALUE> ...
#给镜像添加一些元数据 metadata

HEALTHCHECK [OPTIONS] CMD <COMMAND>
#用于指定某个程序或者指令来监控容器服务的运行状态

ARG #类似ENV,但作用域不一样，ARG设置的环境变量只在镜像构建过程中有效，构建好的镜像不存在此环境变量


# docker容器的网络模式
安装docker的时候会生成一个docker0的虚拟网桥
每运行一个docker容器，都会生成一个veth设备对，一个接口在容器里，一个接口在物理机
给容器起一个代号，这样可以直接以代号访问，避免重启容器ip变化带来的问题
docker run --link=[container_name_to_connect]:[alias] [image] [command]
docker run --net=[网络模式] --privileged=true [image] [command]
--privileged=true run as root user
none 创建的容器没有网络地址ip address,这样就可以自己分配静态IP
--net=container:[container_name_to_connect] 创建的容器和指定容器共享IP
bridge,默认模式，容器启动后会通过DHCP获取一个IP
host,共享宿主机的网络IP

















