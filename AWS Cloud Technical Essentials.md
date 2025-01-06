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



