# Part 1
* CHOOSE THE RIGHT AWS REGION - Latency, Price, Service availability, Data compliance
To keep your application available, you need to maintain high availability and resiliency. A well-known best practice for cloud architecture is to use Region-scoped, managed services.
* An AWS Region is a physical location in the world that has multiple Availability Zones. Availability Zones consist of one or more discrete data centers, each with redundant power, networking, and connectivity, housed in separate facilities.
* Follow Best Practices When Working with the AWS Root User
To ensure the safety of the root user:
Choose a strong password for the root user.
Never share your root user password or access keys with anyone.
Disable or delete the access keys associated with the root user.
Do not use the root user for administrative tasks or everyday tasks.
* Every action a user takes in AWS is an API call.
* IAM Policy Structure
- Effect: Specifies whether the statement results in an allow or an explicit deny
"Effect": "Deny"
- Action: Describes the specific actions that will be allowed or denied
"Action": "iam:CreateUser"
- Resource: Specifies the object or objects that the statement covers
"Resource": "arn:aws:iam::account-ID-without-hyphens:user/Bob"
* With IAM, a company can create an IAM user group, grant the user group the permissions to perform specific job functions, and assign users to a group. This way, the company provides granular access to its employees, and people and services have permissions to only the resources that they need. The company could also achieve the same purpose by using IAM roles for federated access and using granular policies that are attached to roles. 
- USE IAM ROLES WHEN POSSIBLE. Maintaining roles is easier than maintaining users. When you assume a role, IAM dynamically provides temporary credentials that expire after a defined period of time, between 15 minutes and 36 hours. Users, on the other hand, have long-term credentials in the form of user name and password combinations or a set of access keys.

# Part 2
* Servers often times can handle Hypertext Transfer Protocol (HTTP) requests and send responses to clients following the client-server mode.
* Common HTTP servers include:
- Windows options, such as Internet Information Services (IIS).
- Linux options, such as Apache HTTP Web Server, Nginx, and Apache Tomcat.
* At a fundamental level, there are three types of compute options: virtual machines, container services, and serverless. Virtual machines are called Amazon Elastic Compute Cloud or Amazon EC2.

EC2 instances are live instantiations of what is defined in an AMI, you can see this kind of relationship between a Class and an Object. AMI is how you model and define your instance, while the EC2 instance is the entity you interact with. When you launch a new instance, AWS allocates a virtual machine that runs on a hypervisor. Then the AMI you selected is copied to the root device volume, which contains the image used to boot the volume.

What Are Instance Families?

General purpose, Provides a balance of compute, memory, and networking resources, and can be used for a variety of workloads. Scale-out workloads such as web servers, containerized microservices, caching fleets, distributed data stores, and development environments.

Compute optimized, Ideal for compute-bound applications that benefit from high-performance processors. High-performance web servers, scientific modeling, batch processing, distributed analytics, high-performance computing (HPC), machine/deep learning, ad serving, highly scalable multiplayer gaming.

Memory optimized, Designed to deliver fast performance for workloads that process large data sets in memory. Memory-intensive applications such as high-performance databases, distributed web-scale in-memory caches, mid-size in-memory databases, real-time big-data analytics, and other enterprise applications.

Accelerated computing, Use hardware accelerators or co-processors to perform functions such as floating-point number calculations, graphics processing, or data pattern matching more efficiently than is possible with conventional CPUs. 3D visualizations, graphics-intensive remote workstations, 3D rendering, application streaming, video encoding, and other server-side graphics workloads.

Storage optimized, Designed for workloads that require high, sequential read and write access to large data sets on local storage. They are optimized to deliver tens of thousands of low-latency random I/O operations per second (IOPS) to applications that replicate their data across different instances. NoSQL databases, such as Cassandra, MongoDB, and Redis, in-memory databases, scale-out transactional databases, data warehousing, Elasticsearch, and analytics.

By default, your EC2 instances are placed in a network called the default Amazon Virtual Private Cloud (VPC). Any resource you put inside the default VPC will be public and accessible by the internet, so you shouldn’t place any customer data or private information inside of it. Once you get more comfortable with networking on AWS, you should change this default setting to choose your own custom VPCs and restrict access with additional routing and connectivity mechanisms. 

When you stop and start an instance, your instance may be placed on a new underlying physical server. Therefore, you lose any data on the instance store that were on the previous host computer. When you stop an instance, the instance gets a new public IP address but maintains the same private IP address. When you terminate an instance, the instance store are erased, and you lose both the public IP address and private IP address of the machine. Termination of an instance means you can no longer access the machine. 
When you stop-hibernate your instance, AWS signals the operating system to perform hibernation (suspend-to-disk), which saves the contents from the instance memory (RAM) to the Amazon EBS root volume.

Amazon EKS vs Amazon ECS
An EC2 instance with the ECS Agent installed and configured is called a container instance. In Amazon EKS, it is called a worker node.
An ECS Container is called a task. In the Amazon EKS ecosystem, it is called a pod.
While Amazon ECS runs on AWS native technology, Amazon EKS runs on top of Kubernetes.

SERVERLESS CONTAINERS WITH AWS FARGATE
Every definition of serverless mentions four aspects.
No servers to provision or manage.
Scales with usage.
You never pay for idle resources.
Availability and fault tolerance are built-in.

If you want to deploy your workloads and applications without having to manage any EC2 instances or containers, you can use AWS Lambda. There are three primary components of a Lambda function: the trigger, code, and configuration.

AWS Networking
WHAT ARE IP ADDRESSES?
In order to properly route your messages to a location, you need an address. Just like each home has a mail address, each computer has an IP address, which is a 32-bit address.

WHAT IS IPV4 NOTATION?
Typically, you don’t see an IP address in this binary format. Instead, it’s converted into decimal format and noted as an Ipv4 address. 

If you wanted to express IP addresses between the range of 192.168.1.0 and 192.168.1.255, one way is by using Classless Inter-Domain Routing (CIDR) notation. CIDR notation is a compressed way of specifying a range of IP addresses. For example, 192.168.1.0/24 means the first 24 bits of the IP address are fixed, 32 total bits subtracted by 24 fixed bits leaves 8 flexible bits. Each of these flexible bits can be either 0 or 1, because they are binary. That means you have two choices for each of the 8 bits, providing 256 IP addresses in that IP range. 

A VPC is an isolated network you create in the AWS cloud, similar to a traditional network in a data center. When you create a VPC, you need to choose three main things. 
The name of your VPC.
A Region for your VPC to live in. Each VPC spans multiple Availability Zones within the Region you choose.
A IP range for your VPC in CIDR notation. This determines the size of your network. Each VPC can have up to four /16 IP ranges.

Create a Subnet After you create your VPC, you need to create subnets inside of this network. Think of subnets as smaller networks inside your base network—or virtual area networks (VLANs) in a traditional, on-premises network. 
In AWS, subnets are used for high availability and providing different connectivity options for your resources. When you create a subnet, you need to choose three settings.
The VPC you want your subnet to live in, in this case VPC (10.0.0.0/16).
The Availability Zone you want your subnet to live in, in this case AZ1.
A CIDR block for your subnet, which must be a subset of the VPC CIDR block, in this case 10.0.0.0/24.

For AWS to configure your VPC appropriately, AWS reserves five IP addresses in each subnet.
A common starting place for those who are new to the cloud is to create a VPC with a IP range of /16 and create subnets with a IP range of /24. 

To enable internet connectivity for your VPC, you need to create an internet gateway. Think of this gateway as similar to a modem. Just as a modem connects your computer to the internet, the internet gateway connects your VPC to the internet.

A virtual private gateway allows you to connect your AWS VPC to another private network. Once you create and attach a VGW to a VPC, the gateway acts as anchor on the AWS side of the connection. On the other side of the connection, you’ll need to connect a customer gateway to the other private network. A customer gateway device is a physical device or software application on your side of the connection. Once you have both gateways, you can then establish an encrypted VPN connection between the two sides. 

When you create a VPC, AWS creates a route table called the main route table. The default configuration of the main route table is to allow traffic between all subnets in the local network. 
There are two main parts to this route table.
The destination, which is a range of IP addresses where you want your traffic to go. Usually the destination is the IP range of our VPC network.
The target, which is the connection through which to send the traffic. In this case, the traffic is routed through the local VPC network.
If you associate a custom route table with a subnet, the subnet will use it instead of the main route table. By default, each custom route table you create will have the local route already inside it, allowing communication to flow between all resources and subnets inside the VPC. 

Think of a network (Access Control List) ACL as a firewall at the subnet level. A network ACL enables you to control what kind of traffic is allowed to enter or leave your subnet. You can configure this by setting up rules that define what you want to filter. Network ACL’s are considered stateless, so you need to include both the inbound and outbound ports used for the protocol. If you don’t include the outbound range, your server would respond but the traffic would never leave the subnet. Since network ACLs are configured by default to allow incoming and outgoing traffic, you don’t need to change their initial settings unless you need additional security layers.

The next layer of security is for your EC2 Instances. Here, you can create a firewall called a security group. The default configuration of a security group blocks all inbound traffic and allows all outbound traffic. Security groups are stateful, meaning they will remember if a connection is originally initiated by the EC2 instance or from the outside and temporarily allow traffic to respond without having to modify the inbound rules.