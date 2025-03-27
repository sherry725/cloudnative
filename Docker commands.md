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
ctr image pull docker.io/library/busybox:latest
ctr images rm docker.io/library/busybox:latest
ctr images export busybox.tar.gz docker.io/library/busybox:latest







