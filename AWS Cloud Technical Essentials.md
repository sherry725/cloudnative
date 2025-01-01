* CHOOSE THE RIGHT AWS REGION - Latency, Price, Service availability, Data compliance
To keep your application available, you need to maintain high availability and resiliency. A well-known best practice for cloud architecture is to use Region-scoped, managed services.
* Follow Best Practices When Working with the AWS Root User
To ensure the safety of the root user:
Choose a strong password for the root user.
Never share your root user password or access keys with anyone.
Disable or delete the access keys associated with the root user.
Do not use the root user for administrative tasks or everyday tasks.
* IAM Policy Structure
- Effect: Specifies whether the statement results in an allow or an explicit deny
"Effect": "Deny"
- Action: Describes the specific actions that will be allowed or denied
"Action": "iam:CreateUser"
- Resource: Specifies the object or objects that the statement covers
"Resource": "arn:aws:iam::account-ID-without-hyphens:user/Bob"


