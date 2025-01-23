# Part 1 Overview and Security
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

# Part 2 Compute & Networking
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

# Part 3 Storage & Databases on AWS
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

A relational database organizes data into tables. Data in one table can be linked to data in other tables to create relationships—hence, the relational part of the name. The tables, rows, columns, and relationships between them is referred to as a logical schema. With relational databases, a schema is fixed. Once the database is operational, it becomes difficult to change the schema. This requires most of the data modeling to be done upfront before the database is active.

There are many benefits to using a relational database. A few of them are listed here.
Joins: You can join tables, enabling you to better understand relationships between your data.
Reduced redundancy: You can store data in one table and reference it from other tables instead of saving the same data in different places.
Familiarity: Relational databases have been a popular choice since the 1970s. Due to this popularity, technical professionals often have familiarity and experience with this type of database.
Accuracy: Relational databases ensure that your data is persisted with high integrity and adheres to the ACID (atomicity, consistency, isolation, durability) principle.

Common use cases for relational databases.
- 1. Applications that have a solid schema that doesn’t change often, such as:
Lift and shift applications that lifts an app from on-premises and shifts it to the cloud, with little or no modifications.
- 2. Applications that need persistent storage that follows the ACID principle, such as:
Enterprise Resource Planning (ERP) applications
Customer Relationship Management (CRM) applications
Commerce and financial applications

If you host a database on Amazon EC2, AWS takes care of implementing and maintaining the physical infrastructure and hardware and installing the operating system of the EC2 instance. However, you’re still responsible for managing the EC2 instance, managing the database on that host, optimizing queries, and managing customer data. This is what is often referred to as the unmanaged database option on AWS. AWS is responsible for and has control over the hardware and underlying infrastructure, and you are responsible and have control over management of the host and database.Managed Database services provide the setup of both the EC2 instance and the database, and they provide systems for high availability, scalability, patching, and backups. However, you’re still responsible for database tuning, query optimization, and of course, ensuring that your customer data is secure. This provides you ultimate convenience, but you have the least amount of control compared to the two previous options.

Amazon RDS is built off of compute and storage. The compute portion is called the DB (database) instance, which runs the database engine. Depending on the engine of the DB instance you choose, the engine will have different supported features and configurations. A DB instance can contain multiple databases with the same engine, and each database can contain multiple tables.  Underneath the DB instance is an EC2 instance. However, this instance is managed through the Amazon RDS console instead of the Amazon EC2 console. When you create your DB instance, you choose the instance type and size. Amazon RDS supports three instance families.
Standard, which include general-purpose instances
Memory Optimized, which are optimized for memory-intensive applications
Burstable Performance, which provides a baseline performance level, with the ability to burst to full CPU usage.

Much like a regular EC2 instance, the DB instance uses Amazon Elastic Block Store (EBS) volumes as its storage layer. You can choose between three types of EBS volume storage.
General purpose (SSD), Provisioned IOPS (SSD), Magnetic storage (not recommended)
When you create a DB instance, you select the Amazon Virtual Private Cloud (VPC) that your databases will live in. Then, you select the subnets that you want the DB instances to be placed in. This is referred to as a DB subnet group. To create a DB subnet group, you specify:
The Availability Zones (AZs) that include the subnets you want to add
The subnets in that AZ where your DB instance are placed
The subnets you add should be private so they don’t have a route to the internet gateway. This ensures your DB instance, and the cat data inside of it, can only be reached by the app backend.  Access to the DB instance can be further restricted by using network access control lists (ACLs) and security groups. With these firewalls, you can control, at a granular level, what type of traffic you want to allow into your database.  Using these controls provide layers of security for your infrastructure. It reinforces that only the backend instances have access to the database.
If you want to restrict what actions and resources your employees can access, you can use IAM policies.

Back Up Your Data
You don’t want to lose any of that precious cat information. To take regular backups of your RDS instance, you can use: Automatic backups or Manual snapshots. You can retain your automated backups between 0 and 35 days. If you want to keep your automated backups longer than 35 days, use manual snapshots. Manual snapshots are similar to taking EBS snapshots, except you manage them in the RDS console. These are backups that you can initiate at any time, that exist until you delete them.  When you enable Amazon RDS Multi-AZ, Amazon RDS creates a redundant copy of your database in another AZ. You end up with two copies of your database: a primary copy in a subnet in one AZ and a standby copy in a subnet in a second AZ. When you create a DB instance, a domain name system (DNS) name is provided. AWS uses that DNS name to failover to the standby database. In an automatic failover, the standby database is promoted to the primary role and queries are redirected to the new primary database. To ensure that you don’t lose Multi-AZ configuration, a new standby database is created by either: Demoting the previous primary to standby if it’s still up and running Or standing up a new standby DB instance. The reason you can select multiple subnets for an Amazon RDS database is because of the Multi-AZ configuration. You’ll want to ensure that you have used subnets in different AZs for your primary and standby copies.

Amazon DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability. DynamoDB lets you offload the administrative burdens of operating and scaling a distributed database so that you don't have to worry about hardware provisioning, setup and configuration, replication, software patching, or cluster scaling. 
All of your data is stored on solid-state disks (SSDs) and is automatically replicated across multiple Availability Zones in an AWS Region, providing built-in high availability and data durability. 
Core Components of Amazon DynamoDB
In DynamoDB, tables, items, and attributes are the core components that you work with. A table is a collection of items, and each item is a collection of attributes. DynamoDB uses primary keys to uniquely identify each item in a table and secondary indexes to provide more querying flexibility. 
The following are the basic DynamoDB components:
Tables – Similar to other database systems, DynamoDB stores data in tables. A table is a collection of data. For example, see the example table called People that you could use to store personal contact information about friends, family, or anyone else of interest. You could also have a Cars table to store information about vehicles that people drive.
Items – Each table contains zero or more items. An item is a group of attributes that is uniquely identifiable among all of the other items. In a People table, each item represents a person. For a Cars table, each item represents one vehicle. Items in DynamoDB are similar in many ways to rows, records, or tuples in other database systems. In DynamoDB, there is no limit to the number of items you can store in a table.
Attributes – Each item is composed of one or more attributes. An attribute is a fundamental data element, something that does not need to be broken down any further. For example, an item in a People table contains attributes called PersonID, LastName, FirstName, and so on. For a Department table, an item might have attributes such as DepartmentID, Name, Manager, and so on. Attributes in DynamoDB are similar in many ways to fields or columns in other database systems.
Security with Amazon DynamoDB
DynamoDB also offers encryption at rest, which eliminates the operational burden and complexity involved in protecting sensitive data.

Relational, Traditional applications, ERP, CRM, e-commerce, can use Amazon RDS, Amazon Aurora, Amazon Redshift
Key-value, High-traffic web apps, e-commerce systems, gaming applications can use Amazon DynamoDB
In-memory, Caching, session management, gaming leaderboards, geospatial applications, can use Amazon ElastiCache for Memcached, Amazon ElastiCache for Redis
Document, Content management, catalogs, user profiles, can use Amazon DocumentDB (with MongoDB compatibility)
Wide column, High-scale industrial apps for equipment maintenance, fleet management, and route optimization, can use Amazon Keyspaces (for Apache Cassandra)
Graph, Fraud detection, social networking, recommendation engines, can use Amazon Neptune
Time series, IoT applications, DevOps, industrial telemetry, can use Amazon Timestream
Ledger (immutable), Systems of record, supply chain, registrations, banking transactions, can use Amazon QLDB

# Part 4 Monitoring & Optimization
The act of collecting, analyzing, and using data to make decisions or answer questions about your IT resources and systems is called monitoring. 
The resources that host your solutions on AWS all create various forms of data that you might be interested in collecting. You can think of each individual data point that is created by a resource as a metric. Metrics that are collected and analyzed over time become statistics. Generally speaking, if an EC2 instance has a high CPU utilization, it can mean a flood of requests. Or it can reflect a process that has encountered an error and is consuming too much of the CPU. When analyzing CPU utilization, take a process that exceeds a specific threshold for an unusual length of time. Use that abnormal event as a cue to either manually or automatically resolve the issue through actions like scaling the instance.  This is one example of a metric. Other examples of metrics EC2 instances have are network utilization, disk performance, memory utilization, and the logs created by the applications running on top of EC2. An Amazon Simple Storage Service (S3) bucket would not have CPU utilization like an EC2 instance does. Instead, S3 creates metrics related to the objects stored in a bucket like the overall size, or the number of objects in a bucket. S3 also has metrics related to the requests made to the bucket such as reading or writing objects.  Amazon Relational Database Service (RDS) creates metrics such as database connections, CPU utilization of an instance, or disk space consumption. 
Benefits of Monitoring:
Respond to operational issues proactively before your end users are aware of them. 
Improve the performance and reliability of your resources.
Recognize security threats and events. 
Make data-driven decisions for your business.
Create more cost-effective solutions. 
You can use CloudWatch to:
Detect anomalous behavior in your environments.
Set alarms to alert you when something’s not right.
Visualize logs and metrics with the AWS Management Console.
Take automated actions like scaling.
Troubleshoot issues.
Discover insights to keep your applications healthy.

Many AWS services send metrics automatically for free to CloudWatch at a rate of one data point per metric per 5-minute interval, without you needing to do anything to turn on that data collection. This by itself gives you visibility into your systems without you needing to spend any extra money to do so. This is known as basic monitoring. For applications running on EC2 instances, you can get more granularity by posting metrics every minute instead of every 5 minutes using a feature like detailed monitoring. Detailed monitoring has an extra fee associated. 
Custom metrics allows you to publish your own metrics to CloudWatch. Examples of custom metrics: number of page views, Web page load times, 
Request error rates, Number of processes or threads on your instance, Amount of work performed by your application.

CloudWatch can also be the centralized place for logs to be stored and analyzed, using CloudWatch Logs. CloudWatch Logs allows you to query and filter your log data. You also set up metric filters on logs, which turn log data into numerical CloudWatch metrics that you graph and use on your dashboards. Some services are set up to send log data to CloudWatch Logs with minimal effort, like AWS Lambda. With AWS Lambda, all you need to do is give the Lambda function the correct IAM permissions to post logs to CloudWatch Logs. Other services require more configuration. For example, if you want to send your application logs from an EC2 instance into CloudWatch Logs, you need to first install and configure the CloudWatch Logs agent on the EC2 instance. The CloudWatch Logs agent enables Amazon EC2 instances to automatically send log data to CloudWatch Logs. The agent includes the following components. A plug-in to the AWS Command Line Interface (CLI) that pushes log data to CloudWatch Logs. A script that initiates the process to push data to CloudWatch Logs. A cron job that ensures the daemon is always running. After the agent is installed and configured, you can then view your application logs in CloudWatch Logs.  

To set up an alarm you need to choose the metric, the threshold, and the time period. An alarm has three possible states. OK: The metric is within the defined threshold. Everything appears to be operating like normal. ALARM: The metric is outside of the defined threshold. This could be an operational issue. INSUFFICIENT_DATA: The alarm has just started, the metric is not available, or not enough data is available for the metric to determine the alarm state. An alarm can be triggered when it transitions from one state to another. Once an alarm is triggered, it can initiate an action. Actions can be an Amazon EC2 action, an Auto Scaling action, or a notification sent to Amazon Simple Notification Service (SNS).

To increase availability, you need redundancy. This typically means more infrastructure: more data centers, more servers, more databases, and more replication of data. An easy way to fix the physical location issue is by deploying a second EC2 instance in a different Availability Zone. That would also solve issues with the operating system and the application. However, having more than one instance brings new challenges: Create a Process for Replication
Address Customer Redirection: The most common is using a Domain Name System (DNS) where the client uses one record which points to the IP address of all available servers. However, the time it takes to update that list of IP addresses and for the clients to become aware of such change, sometimes called propagation, is typically the reason why this method isn’t always used. 
Another option is to use a load balancer which takes care of health checks and distributing the load across each server. Being between the client and the server, the load balancer avoids propagation time issues. 
Understand the Types of High Availability: To address when having more than one server is the type of availability you need—either be an active-passive or an active-active system. 
Active-Passive: With an active-passive system, only one of the two instances is available at a time. One advantage of this method is that for stateful applications where data about the client’s session is stored on the server, there won’t be any issues as the customers are always sent to the same server where their session is stored.
Active-Active: A disadvantage of active-passive and where an active-active system shines is scalability. By having both servers available, the second server can take some load for the application, thus allowing the entire system to take more load. However, if the application is stateful, there would be an issue if the customer’s session isn’t available on both servers. Stateless applications work better for active-active systems.

Load balancing refers to the process of distributing tasks across a set of resources. In the case of the corporate directory application, the resources are EC2 instances that host the application, and the tasks are the different requests being sent. It’s time to distribute the requests across all the servers hosting the application using a load balancer.
To do this, you first need to enable the load balancer to take all of the traffic and redirect it to the backend servers based on an algorithm. The most popular algorithm is round-robin, which sends the traffic to each server one after the other.
A typical request for the application would start from the browser of the client. It’s sent to a load balancer. Then, it’s sent to one of the EC2 instances that hosts the application. The return traffic would go back through the load balancer and back to the client browser. Thus, the load balancer is directly in the path of the traffic.
Although it is possible to install your own software load balancing solution on EC2 instances, AWS provides a service for that called Elastic Load Balancing (ELB).

The ELB service provides a major advantage over using your own solution to do load balancing, in that you don’t need to manage or operate it. It can distribute incoming application traffic across EC2 instances as well as containers, IP addresses, and AWS Lambda functions.
The fact that ELB can load balance to IP addresses means that it can work in a hybrid mode as well, where it also load balances to on-premises servers.
ELB is highly available. The only option you have to ensure is that the load balancer is deployed across multiple Availability Zones.
In terms of scalability, ELB automatically scales to meet the demand of the incoming traffic. It handles the incoming traffic and sends it to your backend application.

The ELB service is made up of three main components.
Listeners: The client connects to the listener. This is often referred to as client-side. To define a listener, a port must be provided as well as the protocol, depending on the load balancer type. There can be many listeners for a single load balancer.
Target groups: The backend servers, or server-side, is defined in one or more target groups. This is where you define the type of backend you want to direct traffic to, such as EC2 Instances, AWS Lambda functions, or IP addresses. Also, a health check needs to be defined for each target group.
Rules: To associate a target group to a listener, a rule must be used. Rules are made up of a condition that can be the source IP address of the client and a condition to decide which target group to send the traffic to.

Primary features of Application Load Balancer (ALB).
- ALB routes traffic based on request data. It makes routing decisions based on the HTTP protocol like the URL path (/upload) and host, HTTP headers and method, as well as the source IP address of the client. This enables granular routing to the target groups.
- Send responses directly to the client. ALB has the ability to reply directly to the client with a fixed response like a custom HTML page. It also has the ability to send a redirect to the client which is useful when you need to redirect to a specific website or to redirect the request from HTTP to HTTPS, removing that work from your backend servers.
- ALB supports TLS offloading. Speaking of HTTPS and saving work from backend servers, ALB understands HTTPS traffic. To be able to pass HTTPS traffic through ALB, an SSL certificate is provided by either importing a certificate via Identity and Access Management (IAM) or AWS Certificate Manager (ACM) services, or by creating one for free using ACM. This ensures the traffic between the client and ALB is encrypted.
- Authenticate users. On the topic of security, ALB has the ability to authenticate the users before they are allowed to pass through the load balancer. ALB uses the OpenID Connect protocol and integrates with other AWS services to support more protocols like SAML, LDAP, Microsoft AD, and more.
- Secure traffic. To prevent traffic from reaching the load balancer, you configure a security group to specify the supported IP address ranges.
- ALB uses the round-robin routing algorithm. ALB ensures each server receives the same number of requests in general. This type of routing works for most applications.
- ALB uses the least outstanding request routing algorithm. If the requests to the backend vary in complexity where one request may need a lot more CPU time than another, then the least outstanding request algorithm is more appropriate. It’s also the right routing algorithm to use if the targets vary in processing capabilities. An outstanding request is when a request is sent to the backend server and a response hasn’t been received yet.
For example, if the EC2 instances in a target group aren’t the same size, one server’s CPU utilization will be higher than the other if the same number of requests are sent to each server using the round-robin routing algorithm. That same server will have more outstanding requests as well. Using the least outstanding request routing algorithm would ensure an equal usage across targets.
- ALB has sticky sessions. In the case where requests need to be sent to the same backend server because the application is stateful, then use the sticky session feature. This feature uses an HTTP cookie to remember across connections which server to send the traffic to.Finally, ALB is specifically for HTTP and HTTPS traffic. If your application uses a different protocol, then consider the Network Load Balancer (NLB).

Primary features of Network Load Balancer (NLB). Network Load Balancer supports TCP, UDP, and TLS protocols. HTTPS uses TCP and TLS as protocol. However, NLB operates at the connection layer, so it doesn’t understand what a HTTPS request is. That means all features discussed above that are required to understand the HTTP and HTTPS protocol, like routing rules based on that protocol, authentication, and least outstanding request routing algorithm, are not available with NLB.
- NLB uses a flow hash routing algorithm. The algorithm is based on: The protocol, The source IP address and source port, The destination IP address and destination port, The TCP sequence number
If all of these parameters are the same, then the packets are sent to the exact same target. If any of them are different in the next packets, then the request may be sent to a different target.
- NLB has sticky sessions. Different from ALB, these sessions are based on the source IP address of the client instead of a cookie.
- NLB supports TLS offloading. NLB understands the TLS protocol. It can also offload TLS from the backend servers similar to how ALB works.
- NLB handles millions of requests per second. While ALB can also support this number of requests, it needs to scale to reach that number. This takes time. NLB can instantly handle this amount of requests.
- NLB supports static and elastic IP addresses. There are some situations where the application client needs to send requests directly to the load balancer IP address instead of using DNS. For example, this is useful if your application can’t use DNS or if the connecting clients require firewall rules based on IP addresses. In this case, NLB is the right type of load balancer to use.
- NLP preserves source IP address. NLB preserves the source IP address of the client when sending the traffic to the backend. With ALB, if you look at the source IP address of the requests, you will find the IP address of the load balancer. While with NLB, you would see the real IP address of the client, which is required by the backend application in some cases.

Application Load Balancer Features: Protocols: HTTP, HTTPS; Connection draining (deregistration delay); IP addresses as targets;Routing based on Source IP address, path, host, HTTP headers, HTTP method, and query string; Redirects; Fixed response; User authentication
Network Load Balancer: Protocols: TCP, UDP, TLS; IP addresses as targets; Static IP and Elastic IP address; Preserve Source IP address

Vertical Scaling means increasing the size of the server. It’s actually a lot of manual work to do. Another disadvantage is that a server can only scale vertically up to a certain limit.bIf there are too many requests sent to a single active-passive system, the active server will become unavailable and hopefully failover to the passive server. But this doesn’t solve anything. With active-passive, you need vertical scaling. 

Horizontal Scaling, for the application to work in an active-active system, it’s already created as stateless, not storing any client session on the server. This means that having two servers or having four wouldn’t require any application changes. It would only be a matter of creating more instances when required and shutting them down when the traffic decreases. There are many more advantages to using an active-active system in comparison with an active-passive. Modifying your application to become stateless enables scalability.

The EC2 Auto Scaling service works to add or remove capacity to keep a steady and predictable performance at the lowest possible cost. By adjusting the capacity to exactly what your application uses, you only pay for what your application needs. And even with applications that have steady usage, EC2 Auto Scaling can help with fleet management. If there is an issue with an EC2 instance, EC2 Auto Scaling can automatically replace that instance. This means that EC2 Auto Scaling helps both to scale your infrastructure and ensure high availability. 

There are three main components to EC2 Auto Scaling.
Launch template or configuration: What resource should be automatically scaled?
EC2 Auto Scaling Group: Where should the resources be deployed? This is where you specify the Amazon Virtual Private Cloud (VPC) and subnets the EC2 instance should be launched in. It’s important to select at least two subnets that are across different Availability Zones. Three capacity settings to configure for the group size: min, max, desired capacity
Scaling policies: When should the resources be added or removed?
In the AWS Monitoring module, you learned about Amazon CloudWatch metrics and alarms. You use metrics to keep information about different attributes of your EC2 instance like the CPU percentage. You use alarms to specify an action when a threshold is reached. Metrics and alarms are what scaling policies use to know when to act. For example, you set up an alarm that says when the CPU utilization is above 70% across the entire fleet of EC2 instances, trigger a scaling policy to add an EC2 instance.
There are three types of scaling policies: simple, step, and target tracking scaling.
Simple Scaling Policy
A simple scaling policy allows you to do exactly what’s described above. You use a CloudWatch alarm and specify what to do when it is triggered. This can be a number of EC2 instances to add or remove, or a specific number to set the desired capacity to. You can specify a percentage of the group instead of using an amount of EC2 instances, which makes the group grow or shrink more quickly. However, what if the CPU utilization was now above 85% across the ASG? Only adding one instance may not be the right move here. Instead, you may want to add another step in your scaling policy. Unfortunately, a simple scaling policy can’t help with that.
Step Scaling Policy
This is where a step scaling policy helps. Step scaling policies respond to additional alarms even while a scaling activity or health check replacement is in progress. Similar to the example above, you decide to add two more instances in case the CPU utilization is at 85%, and four more instances when it’s at 95%.
Deciding when to add and remove instances based on CloudWatch alarms may seem like a difficult task. This is why the third type of scaling policy exists: target tracking.
Target Tracking Scaling Policy
If your application scales based on average CPU utilization, average network utilization (in or out), or based on request count, then this scaling policy type is the one to use. All you need to provide is the target value to track and it automatically creates the required CloudWatch alarms.