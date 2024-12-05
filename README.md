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

docker run --name container_name -p 80 -itd image_name





