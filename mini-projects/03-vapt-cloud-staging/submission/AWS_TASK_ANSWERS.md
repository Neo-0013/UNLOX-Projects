# UNLOX Section 4: AWS Tasks — Concept Questions & Technical Answers

---

## Part 1: Task 6 — Amazon EC2 Concept Questions

### Question 1: What is an EC2 instance, in your own words?
**Answer:**
An Amazon EC2 (Elastic Compute Cloud) instance is an on-demand, resizable virtual server running on Amazon Web Services' global physical infrastructure. Instead of procuring and maintaining physical server hardware in an on-premises datacenter, an engineer can spin up an EC2 instance in minutes with a customized operating system (such as Ubuntu Server or Amazon Linux), virtual CPU (vCPU), memory (RAM), storage (Amazon EBS), and virtual networking interfaces. It provides full root/administrative control to host backend microservices, web applications, databases, or staging environments with elastic scalability (scaling up or out dynamically based on load).

---

### Question 2: What is the difference between a T2 and a T3 instance type? When would you choose one over the other?
**Answer:**
Both T2 and T3 instances belong to the general-purpose, burstable performance family designed to handle workloads with variable CPU utilization. However, they possess several critical architectural differences:

1. **Hardware & Hypervisor Architecture:**
   - **T2 instances** run on older Intel Xeon processors and leverage the legacy Xen hypervisor.
   - **T3 instances** run on newer Intel Xeon Platinum (or AWS Nitro System-powered) processors. The AWS Nitro System offloads hypervisor overhead, providing higher processing efficiency, enhanced networking, and lower hypervisor latency.
2. **Burstable Credit Model (Unlimited vs. Standard):**
   - **T2 instances** launch by default in **Standard mode**. If the instance exhausts its accumulated CPU credits during a prolonged spike, its CPU performance is strictly throttled down to its baseline level.
   - **T3 instances** launch by default in **Unlimited mode**. If a CPU spike exceeds the baseline credits, the instance will not throttle; instead, it continues bursting at full capacity while incurring a small hourly fee per vCPU-hour of surplus credit consumption.
3. **Price-to-Performance & Cost:**
   - T3 instances are generally up to 10% more cost-effective per hour and offer higher compute performance per dollar compared to legacy T2 instances.

**When to Choose One Over the Other:**
- **Choose T2:** When deploying strictly within the **AWS Free Tier** limit (which specifically includes 750 monthly hours of `t2.micro` instances in regions where T2 is available), or when legacy workloads cannot operate under the Nitro virtualization system.
- **Choose T3:** For modern development, staging, or production environments where you require superior compute performance per dollar, Nitro security isolation, and burstable resiliency where you cannot tolerate CPU throttling during sudden traffic surges.

---

### Question 3: What does the number in an instance type (e.g. t2.micro vs t2.large) tell you?
**Answer:**
In AWS instance nomenclature (e.g., `t2.micro`, `t3.large`, `c5.xlarge`, `m6i.2xlarge`), the instance name is broken down into structured components:
- **Letter prefix (`t`)**: Represents the **Instance Family** (`t` = general purpose burstable, `c` = compute optimized, `r` = memory optimized, `m` = balanced general purpose).
- **First number (`2` or `3`)**: Represents the **Instance Generation**. A `t2` is 2nd generation, while `t3` is 3rd generation. A higher number indicates newer underlying CPU architecture, modern hypervisors (Nitro), improved bus throughput, and superior energy/cost efficiency.
- **Suffix size (`micro`, `large`, `xlarge`)**: Represents the **Resource Allocation Size**. As you move up the sizing scale (`nano` $\rightarrow$ `micro` $\rightarrow$ `small` $\rightarrow$ `medium` $\rightarrow$ `large` $\rightarrow$ `xlarge` $\rightarrow$ `2xlarge`):
  - vCPU count doubles or scales proportionally (e.g., `t2.micro` provides 1 vCPU and 1 GiB RAM, whereas `t2.large` provides 2 vCPUs and 8 GiB RAM).
  - Memory capacity increases proportionally.
  - Network bandwidth and EBS-optimized throughput scale up accordingly.

---

### Question 4: Why do we use a PEM key when connecting to an EC2 instance? What happens if it is lost?
**Answer:**
**Why We Use a PEM Key:**
AWS EC2 Linux instances do not configure default passwords for remote access. Instead, they enforce asymmetric cryptography (Public-Key Infrastructure) via SSH keys. When you generate a key pair, AWS stores the **public key** in the instance's `/home/ubuntu/.ssh/authorized_keys` file during first boot (cloud-init), while you download the private key formatted as a Privacy-Enhanced Mail (`.pem`) file. During SSH authentication, the client proves possession of the matching private key without transmitting secrets over the wire. This eliminates brute-force password dictionary attacks, credential stuffing, and unauthorized console access.

**What Happens If It Is Lost?**
AWS does not retain a copy of your private key on their servers; if lost, it cannot be downloaded again.
- **If lost while the instance is running without other access methods:** Direct SSH connection as the default user becomes impossible.
- **Recovery Procedures:**
  1. **AWS Systems Manager (SSM) Session Manager:** If an SSM IAM role was attached and the SSM agent is running, an administrator can establish a root shell directly through the AWS Console/CLI without needing any SSH key.
  2. **EC2 Instance Connect:** If enabled, you can push a temporary 60-second public key to the instance via the AWS API.
  3. **Root EBS Volume Detachment / Swap:** If SSM is unavailable, you must stop the instance, detach its root EBS volume, attach it as a secondary data disk to a helper rescue instance, edit `/home/ubuntu/.ssh/authorized_keys` to insert a newly generated public key, unmount and reattach the volume back to the original instance, and reboot.

---

### Question 5: What is the difference between a security group and a network ACL?
**Answer:**
Both Security Groups (SGs) and Network Access Control Lists (NACLs) function as firewalls within an Amazon VPC, but operate at fundamentally different layers with distinct behavior:

| Feature / Attribute | Security Group (SG) | Network ACL (NACL) |
| :--- | :--- | :--- |
| **Operating Layer** | **Instance Level** (Virtual network interface / ENI) | **Subnet Level** (Boundary of the entire subnet) |
| **State Tracking** | **Stateful**: Return traffic is automatically allowed regardless of inbound rules. | **Stateless**: Return traffic must be explicitly allowed via matching ephemeral port rules. |
| **Rule Capabilities** | Supports **ALLOW rules only**. Deny is implicit (anything not allowed is dropped). | Supports both **ALLOW and DENY rules** explicitly. |
| **Rule Evaluation Order** | Evaluates **all rules collectively** before deciding to allow traffic. | Evaluates rules in strict **numerical order** (lowest number first, stopping on first match). |
| **Scope of Protection** | Applies only to instances explicitly assigned to the Security Group. | Automatically applies to all traffic entering or exiting every instance within the subnet. |
| **Use Case in Scenario** | Used in Task 6 to restrict SSH (22) and HTTP (80) access strictly to the student's Kali Linux IP. | Used as a broad subnet subnet-level defense-in-depth barrier (e.g., blocking known malicious CIDRs). |

---

## Part 2: Task 7 — Amazon S3 Concept Questions

### Question 1: What is an S3 bucket used for?
**Answer:**
Amazon S3 (Simple Storage Service) is a highly scalable, secure, and durable object storage service designed to store and retrieve any amount of unstructured data from anywhere on the internet or within AWS. Unlike block storage (Amazon EBS, attached to EC2 instances) or file systems (Amazon EFS), S3 stores data as discrete **objects** (comprising file data, customizable metadata, and a globally unique key) within logical containers called **buckets**.

Key use cases include:
- Hosting static web assets (HTML, CSS, JavaScript, media files).
- Secure backup and disaster recovery archives (with 99.999999999% [11 9's] durability).
- Storing staging build artifacts, container images, and software packages.
- Data lakes for analytics, machine learning, and security log aggregation (e.g., CloudTrail, VPC Flow Logs).

---

### Question 2: What is the difference between a public and a private bucket, and how is that controlled?
**Answer:**
- **Private Bucket (Default & Best Practice):** Only the bucket owner and explicitly authorized IAM identities or roles have permissions to list, read, or write objects. Unauthenticated internet users receive an `HTTP 403 Access Denied` response.
- **Public Bucket:** Anyone on the public internet, authenticated or unauthenticated, can access, download, or list the bucket's contents without credentials.

**How Access is Controlled:**
1. **S3 Block Public Access (BPA):** A centralized account-level and bucket-level kill-switch that overrides all ACLs and policies. Enabling all four BPA controls (`BlockPublicAcls`, `IgnorePublicAcls`, `BlockPublicPolicy`, `RestrictPublicBuckets`) guarantees the bucket cannot be made public by mistake.
2. **Bucket Policies:** JSON resource-based access policies attached directly to the bucket granting or denying specific actions (`s3:GetObject`) based on principals, IP conditions, or VPC endpoints.
3. **Access Control Lists (ACLs):** Legacy resource policies defining grant lists for individual objects or buckets (AWS now recommends disabling ACLs via *Bucket Owner Enforced* mode).
4. **IAM Identity Policies:** Permissions attached directly to AWS IAM users, groups, or roles dictating what S3 resources they can access.
5. **Pre-Signed URLs:** Time-bound URLs granting temporary access generated using valid AWS credentials without altering the bucket's private posture.

---

### Question 3: What is a bucket policy, and how does it differ from an IAM policy?
**Answer:**
Both Bucket Policies and IAM Policies are written in AWS JSON Access Policy syntax, but their attachment points and authorization contexts differ:

- **Bucket Policy (Resource-Based Policy):**
  - **Where it is attached:** Attached directly to the **Amazon S3 Bucket** resource itself.
  - **Who it controls:** Controls who (any AWS identity, specific external AWS accounts, anonymous users, or IP CIDRs) can access that specific bucket and its objects.
  - **Cross-Account Access:** Allows granting access to identities belonging to different AWS accounts without requiring cross-account IAM role assumption.
  - **Conditional Logic:** Can restrict access based on network properties (e.g., `aws:sourceVpce` to ensure requests only arrive from an internal VPC endpoint, or `aws:SourceIp`).

- **IAM Policy (Identity-Based Policy):**
  - **Where it is attached:** Attached to an **IAM User, IAM Group, or IAM Role**.
  - **Who it controls:** Defines the exact permissions of that specific identity across multiple AWS services (e.g., allowing a DevOps user to create EC2 instances AND access specific S3 buckets).
  - **Boundary:** Only applies to the specific identity it is attached to within that AWS account.

**Summary:** An IAM policy says *"What can this user do across AWS?"*, whereas a Bucket Policy says *"Who is allowed to access this specific S3 bucket and under what conditions?"*

---

### Question 4: Why is it risky to leave an S3 bucket publicly accessible by default?
**Answer:**
Leaving an S3 bucket publicly accessible is one of the most prevalent causes of enterprise security breaches and data exposure incidents. Key risks include:

1. **Mass Data Exfiltration & Intellectual Property Theft:** Attackers and automated scanners (e.g., `s3scanner`, `lazys3`) continuously probe predictable bucket names. Unauthenticated access exposes proprietary source code, internal staging files, sensitive customer databases, and personally identifiable information (PII).
2. **Credential & Secret Exposure:** Staging repositories frequently contain environment configuration files (`.env`), private SSL certificates, database connection strings, or cloud access keys that grant attackers lateral movement across the enterprise infrastructure.
3. **Regulatory & Compliance Penalties:** Unauthorized exposure of customer or financial data triggers severe non-compliance fines under GDPR, HIPAA, PCI-DSS, and DPDP regulations, accompanied by reputational and brand damage.
4. **Malicious Tampering & Ransomware (Public Write Access):** If write permissions (`s3:PutObject`) are open, attackers can overwrite legitimate static assets with malicious JavaScript (stored XSS or supply chain defacement), host phishing pages, or encrypt assets for ransom.
5. **Denial-of-Wallet (Financial Exhaustion):** Attackers can script millions of HTTP GET requests against public assets, generating catastrophic bandwidth and API invocation costs charged directly to the AWS account owner.
