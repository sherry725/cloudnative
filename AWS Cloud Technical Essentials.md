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

- General purpose, Provides a balance of compute, memory, and networking resources, and can be used for a variety of workloads. Scale-out workloads such as web servers, containerized microservices, caching fleets, distributed data stores, and development environments.

- Compute optimized, Ideal for compute-bound applications that benefit from high-performance processors. High-performance web servers, scientific modeling, batch processing, distributed analytics, high-performance computing (HPC), machine/deep learning, ad serving, highly scalable multiplayer gaming.

- Memory optimized, Designed to deliver fast performance for workloads that process large data sets in memory. Memory-intensive applications such as high-performance databases, distributed web-scale in-memory caches, mid-size in-memory databases, real-time big-data analytics, and other enterprise applications.

- Accelerated computing, Use hardware accelerators or co-processors to perform functions such as floating-point number calculations, graphics processing, or data pattern matching more efficiently than is possible with conventional CPUs. 3D visualizations, graphics-intensive remote workstations, 3D rendering, application streaming, video encoding, and other server-side graphics workloads.

- Storage optimized, Designed for workloads that require high, sequential read and write access to large data sets on local storage. They are optimized to deliver tens of thousands of low-latency random I/O operations per second (IOPS) to applications that replicate their data across different instances. NoSQL databases, such as Cassandra, MongoDB, and Redis, in-memory databases, scale-out transactional databases, data warehousing, Elasticsearch, and analytics.

By default, your EC2 instances are placed in a network called the default Amazon Virtual Private Cloud (VPC). Any resource you put inside the default VPC will be public and accessible by the internet, so you shouldn’t place any customer data or private information inside of it. Once you get more comfortable with networking on AWS, you should change this default setting to choose your own custom VPCs and restrict access with additional routing and connectivity mechanisms. 

When you stop and start an instance, your instance may be placed on a new underlying physical server. Therefore, you lose any data on the instance store that were on the previous host computer. When you stop an instance, the instance gets a new public IP address but maintains the same private IP address. When you terminate an instance, the instance store are erased, and you lose both the public IP address and private IP address of the machine. Termination of an instance means you can no longer access the machine. 
When you stop-hibernate your instance, AWS signals the operating system to perform hibernation (suspend-to-disk), which saves the contents from the instance memory (RAM) to the Amazon EBS root volume.

* Amazon EKS vs Amazon ECS
An EC2 instance with the ECS Agent installed and configured is called a container instance. In Amazon EKS, it is called a worker node.
An ECS Container is called a task. In the Amazon EKS ecosystem, it is called a pod.
While Amazon ECS runs on AWS native technology, Amazon EKS runs on top of Kubernetes.

* SERVERLESS CONTAINERS WITH AWS FARGATE
Every definition of serverless mentions four aspects.
No servers to provision or manage.
Scales with usage.
You never pay for idle resources.
Availability and fault tolerance are built-in.

If you want to deploy your workloads and applications without having to manage any EC2 instances or containers, you can use AWS Lambda. There are three primary components of a Lambda function: the trigger, code, and configuration.

* AWS Networking
WHAT ARE IP ADDRESSES?
In order to properly route your messages to a location, you need an address. Just like each home has a mail address, each computer has an IP address, which is a 32-bit address.

WHAT IS IPV4 NOTATION?
Typically, you don’t see an IP address in this binary format. Instead, it’s converted into decimal format and noted as an Ipv4 address. 

If you wanted to express IP addresses between the range of 192.168.1.0 and 192.168.1.255, one way is by using Classless Inter-Domain Routing (CIDR) notation. CIDR notation is a compressed way of specifying a range of IP addresses. For example, 192.168.1.0/24 means the first 24 bits of the IP address are fixed, 32 total bits subtracted by 24 fixed bits leaves 8 flexible bits. Each of these flexible bits can be either 0 or 1, because they are binary. That means you have two choices for each of the 8 bits, providing 256 IP addresses in that IP range. 

* A VPC is an isolated network you create in the AWS cloud, similar to a traditional network in a data center. When you create a VPC, you need to choose three main things. 
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

* To enable internet connectivity for your VPC, you need to create an internet gateway. Think of this gateway as similar to a modem. Just as a modem connects your computer to the internet, the internet gateway connects your VPC to the internet.

A virtual private gateway allows you to connect your AWS VPC to another private network. Once you create and attach a VGW to a VPC, the gateway acts as anchor on the AWS side of the connection. On the other side of the connection, you’ll need to connect a customer gateway to the other private network. A customer gateway device is a physical device or software application on your side of the connection. Once you have both gateways, you can then establish an encrypted VPN connection between the two sides. 

* When you create a VPC, AWS creates a route table called the main route table. The default configuration of the main route table is to allow traffic between all subnets in the local network. 
There are two main parts to this route table.
The destination, which is a range of IP addresses where you want your traffic to go. Usually the destination is the IP range of our VPC network.
The target, which is the connection through which to send the traffic. In this case, the traffic is routed through the local VPC network.
If you associate a custom route table with a subnet, the subnet will use it instead of the main route table. By default, each custom route table you create will have the local route already inside it, allowing communication to flow between all resources and subnets inside the VPC. 

* Think of a network (Access Control List) ACL as a firewall at the subnet level. A network ACL enables you to control what kind of traffic is allowed to enter or leave your subnet. You can configure this by setting up rules that define what you want to filter. Network ACL’s are considered stateless, so you need to include both the inbound and outbound ports used for the protocol. If you don’t include the outbound range, your server would respond but the traffic would never leave the subnet. Since network ACLs are configured by default to allow incoming and outgoing traffic, you don’t need to change their initial settings unless you need additional security layers.

* The next layer of security is for your EC2 Instances. Here, you can create a firewall called a security group. The default configuration of a security group blocks all inbound traffic and allows all outbound traffic. Security groups are stateful, meaning they will remember if a connection is originally initiated by the EC2 instance or from the outside and temporarily allow traffic to respond without having to modify the inbound rules.

# Part 3
Block Storage
While file storage treats files as a singular unit, block storage splits files into fixed-size chunks of data called blocks that have their own addresses. Since each block is addressable, blocks can be retrieved efficiently. Since block storage is optimized for low-latency operations, it is a typical storage choice for high-performance enterprise workloads, such as databases or enterprise resource planning (ERP) systems, that require low-latency storage.

Object Storage
Objects, much like files, are also treated as a single unit of data when stored. However, unlike file storage, these objects are stored in a flat structure instead of a hierarchy. Each object is a file with a unique identifier. This identifier, along with any additional metadata, is bundled with the data and stored. With object storage, you can store almost any type of data, and there is no limit to the number of objects stored, making it easy to scale. Object storage is generally useful when storing large data sets, unstructured files like media assets, and static assets, such as photos.

Block storage in the cloud is analogous to direct-attached storage (DAS) or a storage area network (SAN). File storage systems are often supported with a network attached storage (NAS) server.

 Amazon EC2 Instance Store provides temporary block-level storage for your instance. This storage is located on disks that are physically attached to the host computer. This ties the lifecycle of your data to the lifecycle of your EC2 instance. If you delete your instance, the instance store is deleted as well. Due to this, instance store is considered ephemeral storage. 

 Instance store is ideal if you are hosting applications that replicate data to other EC2 instances, such as Hadoop clusters. For these cluster-based workloads, having the speed of locally attached volumes and the resiliency of replicated data helps you achieve data distribution at high performance. It’s also ideal for temporary storage of information that changes frequently, such as buffers, caches, scratch data, and other temporary content. 

As the name implies, Amazon EBS is a block-level storage device that you can attach to an Amazon EC2 instance. These storage devices are called Amazon EBS volumes. EBS volumes are essentially drives of a user-configured size attached to an EC2 instance, similar to how you might attach an external drive to your laptop. The external drive is separate from the computer. That means, if an accident happens and the computer goes down, you still have your data on your external drive. The same is true for EBS volumes. For EBS volumes, the maximum amount of storage you can have is 16 TB. EC2 has a one-to-many relationship with EBS volumes. You can add these additional volumes during or after EC2 instance creation to provide more storage capacity for your hosts. Amazon EBS is useful when you need to retrieve data quickly and have data persist long-term. Volumes are commonly used in Operating systems, Databases, Enterprise applications, Throughput-intensive applications.

There are two main categories of Amazon EBS volumes: solid-state drives (SSDs) and hard-disk drives (HDDs). SSDs provide strong performance for random input/output (I/O), while HDDs provide strong performance for sequential I/O. AWS offers two types of each. 

Errors happen. One of those errors is not backing up data, and then, inevitably losing that data. To prevent this from happening to you, you should back up your data—even in AWS. Since your EBS volumes consist of the data from your Amazon EC2 instance, you’ll want to take backups of these volumes, called snapshots. When you take a snapshot of any of your EBS volumes, these backups are stored redundantly in multiple Availability Zones using Amazon S3. EBS snapshots can be used to create multiple new volumes, whether they’re in the same Availability Zone or a different one. When you create a new volume from a snapshot, it’s an exact copy of the original volume at the time the snapshot was taken. 

Unlike Amazon EBS, Amazon S3 is a standalone storage solution that isn’t tied to compute. It enables you to retrieve your data from anywhere on the web. Amazon S3 is an object storage service. Object storage stores data in a flat structure, using unique identifiers to look up objects when requested. An object is simply a file combined with metadata and that you can store as many of these objects as you’d like. All of these characteristics of object storage are also characteristics of Amazon S3. 

In Amazon S3, you have to store your objects in containers called buckets. When you create a bucket, you choose, at the very minimum, two things: the bucket name and the AWS Region you want the bucket to reside in. The first part is choosing the Region you want the bucket to reside in. Typically, this will be a Region that you’ve used for other resources, such as your compute. When you choose a Region for your bucket, all objects you put inside that bucket are redundantly stored across multiple devices, across multiple Availability Zones. The second part is choosing a bucket name which must be unique across all AWS accounts. AWS stops you from choosing a bucket name that has already been chosen by someone else in another AWS account. 

The most common ways you can use Amazon S3 include
Backup and storage: S3 is a natural place to back up files because it is highly redundant. As mentioned in the last unit, AWS stores your EBS snapshots in S3 to take advantage of its high availability.
Media hosting: Because you can store unlimited objects, and each individual object can be up to 5 TBs, S3 is an ideal location to host video, photo, or music uploads.
Software delivery: You can use S3 to host your software applications that customers can download.
Data lakes: S3 is an optimal foundation for a data lake because of its virtually unlimited scalability. You can increase storage from gigabytes to petabytes of content, paying only for what you use.
Static websites: You can configure your bucket to host a static website of HTML, CSS, and client-side scripts.
Static content: Because of the limitless scaling, the support for large files, and the fact that you access any object over the web at any time, S3 is the perfect place to store static content.

Everything in Amazon S3 is private by default. To be more specific about who can do what with your S3 resources, Amazon S3 provides two main access management features: IAM policies and S3 bucket policies.  IAM policies are not tied to any one AWS service and can be used to define access to nearly any AWS action. You should use IAM policies for private buckets when: 1. You have many buckets with different permission requirements. Instead of defining many different S3 bucket policies, you can use IAM policies instead. 2. You want all policies to be in a centralized location. Using IAM policies allows you to manage all policy information in one location. S3 bucket policies are similar to IAM policies, the difference is IAM policies are attached to users, groups, and roles, whereas S3 bucket policies are only attached to buckets. S3 bucket policies specify what actions are allowed or denied on the bucket. You should use S3 bucket policies when: 1. You need a simple way to do cross-account access to S3, without using IAM roles. 2. Your IAM policies bump up against the defined size limit. S3 bucket policies have a larger size limit.

Amazon S3 storage classes:
Amazon S3 Standard: This is considered general purpose storage for cloud applications, dynamic websites, content distribution, mobile and gaming applications, and big data analytics.
Amazon S3 Intelligent-Tiering: This tier is useful if your data has unknown or changing access patterns. S3 Intelligent-Tiering stores objects in two tiers, a frequent access tier and an infrequent access tier. Amazon S3 monitors access patterns of your data, and automatically moves your data to the most cost-effective storage tier based on frequency of access.
Amazon S3 Standard-Infrequent Access (S3 Standard-IA): S3 Standard-IA is for data that is accessed less frequently, but requires rapid access when needed. S3 Standard-IA offers the high durability, high throughput, and low latency of S3 Standard, with a low per-GB storage price and per-GB retrieval fee. This storage tier is ideal if you want to store long-term backups, disaster recovery files, and so on.
Amazon S3 One Zone-Infrequent Access (S3 One Zone-IA): Unlike other S3 storage classes which store data in a minimum of three Availability Zones (AZs), S3 One Zone-IA stores data in a single AZ and costs 20% less than S3 Standard-IA. S3 One Zone-IA is ideal for customers who want a lower-cost option for infrequently accessed data but do not require the availability and resilience of S3 Standard or S3 Standard-IA. It’s a good choice for storing secondary backup copies of on-premises data or easily re-creatable data.
Amazon S3 Glacier Instant Retrieval: Amazon S3 Glacier Instant Retrieval is an archive storage class that delivers the lowest-cost storage for long-lived data that is rarely accessed and requires retrieval in milliseconds.
Amazon S3 Glacier Flexible Retrieval:S3 Glacier Flexible Retrieval delivers low-cost storage, up to 10% lower cost (than S3 Glacier Instant Retrieval), for archive data that is accessed 1—2 times per year and is retrieved asynchronously.
Amazon S3 Glacier Deep Archive: S3 Glacier Deep Archive is Amazon S3’s lowest-cost storage class and supports long-term retention and digital preservation for data that may be accessed once or twice in a year. It is designed for customers—particularly those in highly regulated industries, such as the Financial Services, Healthcare, and Public Sectors—that retain data sets for 7 to 10 years or longer to meet regulatory compliance requirements.
Amazon S3 Outposts:Amazon S3 on Outposts delivers object storage to your on-premises AWS Outposts environment.

If you keep manually changing your objects, such as your employee photos, from storage tier to storage tier, you may want to look into automating this process using a lifecycle policy. When you define a lifecycle policy configuration for an object or group of objects, you can choose to automate two actions: transition and expiration actions.
Transition actions are used to define when you should transition your objects to another storage class.
Expiration actions define when objects expire and should be permanently deleted.
For example, you might choose to transition objects to S3 Standard-IA storage class 30 days after you created them, or archive objects to the S3 Glacier storage class one year after creating them.
The following use cases are good candidates for lifecycle management.
Periodic logs: If you upload periodic logs to a bucket, your application might need them for a week or a month. After that, you might want to delete them.
Data that changes in access frequency: Some documents are frequently accessed for a limited period of time. After that, they are infrequently accessed. At some point, you might not need real-time access to them, but your organization or regulations might require you to archive them for a specific period. After that, you can delete them.

Amazon EC2 Instance Store is generally well-suited for temporary storage of information that is constantly changing, such as buffers, caches, and scratch data. 

Amazon EBS is meant for data that changes frequently and needs to persist through instance stops, terminations, or hardware failures. Amazon EBS has two different types of volumes: SSD-backed volumes and HDD-backed volumes.SSD-backed volumes have the following characteristics. 
Performance depends on IOPS (input/output operations per second).
Ideal for transactional workloads such as databases and boot volumes.
HDD-backed volumes have the following characteristics: 
Performance depends on MB/s.
Ideal for throughput-intensive workloads, such as big data, data warehouses, log processing, and sequential data I/O.
Here are a few important features of Amazon EBS that you need to know when comparing it to other services. 
It is block storage.
You pay for what you provision (you have to provision storage in advance).
EBS volumes are replicated across multiple servers in a single Availability Zone.
Most EBS volumes can only be attached to a single EC2 instance at a time.

If your data doesn’t change that often, Amazon S3 might be a more cost-effective and scalable storage solution. S3 is ideal for storing static web content and media, backups and archiving, data for analytics, and can even be used to host entire static websites with custom domain names.Here are a few important features of Amazon S3 to know about when comparing it to other services. 
It is object storage.
You pay for what you use (you don’t have to provision storage in advance).
Amazon S3 replicates your objects across multiple Availability Zones in a Region.
Amazon S3 is not storage attached to compute.

S3 uses a flat namespace and isn’t meant to serve as a standalone file system, most EBS volumes can only be attached to one EC2 instance at a time. So, if you need file storage on AWS, which service should you use?For file storage that can mount on to multiple EC2 instances, you can use Amazon Elastic File System (Amazon EFS) or Amazon FSx.
Here are a few important features of Amazon EFS and FSx to know about when comparing them to other services. 
It is file storage.
You pay for what you use (you don’t have to provision storage in advance).
Amazon EFS and Amazon FSx can be mounted onto multiple EC2 instances.






