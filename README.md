# AWS Cost Optimization 🚀

Managing AWS EBS snapshots manually can lead to **unnecessary storage costs** if old, unused snapshots accumulate. This project automates the cleanup process using **AWS Lambda, EC2, and SNS**, ensuring cost optimization while keeping you notified before deletion.

---
## 🚀 Features

✅ **Automatic EBS Snapshot Cleanup** – Deletes snapshots not linked to active EC2 instances.  
✅ **Pre-Deletion Notifications** – Sends an **SNS notification** before deleting snapshots.  
✅ **Cost Optimization** – Reduces AWS storage costs by removing unused snapshots.  
✅ **Serverless Architecture** – Uses **AWS Lambda** for automation, minimizing infrastructure costs.  
✅ **Scheduled Execution** – Uses **Amazon EventBridge** to trigger the function automatically.  
✅ **Customizable** – Modify retention policies and notification settings as needed.

---

## 🛠️ Tech Stack

- **AWS Lambda** (Python 3.9+)
- **Amazon EC2 & EBS**
- **Amazon SNS** (for notifications)
- **Amazon EventBridge** (for automation)
- **Boto3 SDK** (AWS SDK for Python)

---

## 🚀 Deployment Steps

### **1️⃣ Create an IAM Role**
1. Go to **IAM** in AWS Console.
2. Create a new role with **Lambda** as the trusted entity.
3. Attach the following policies:
   - `AmazonEC2FullAccess` (For managing snapshots)
   - `AmazonSNSFullAccess` (For sending notifications)
4. Attach this role to your Lambda function.

### **2️⃣ Create an SNS Topic for Notifications**
1. Open **Amazon SNS** in AWS Console.
2. Create a new **SNS Topic** (e.g., `EBS-Snapshot-Alerts`).
3. Add **email subscribers** to receive notifications.

### **3️⃣ Deploy Lambda Function**
1. Open **AWS Lambda** and create a function.
2. Select **Python 3.9+** as the runtime.
3. Assign the **IAM Role** created earlier.
4. Upload the `lambda_function.py` file.
5. Set the **timeout** to at least **1 minute**.

### **4️⃣ Schedule with EventBridge**
1. Open **Amazon EventBridge**.
2. Create a **Scheduled Rule** to trigger Lambda periodically.
3. Set an appropriate **cron expression** (e.g., `cron(0 12 * * ? *)` for daily cleanup).
4. Choose the Lambda function as the target.

---

## 🙌 Contributing
Want to improve this project? Feel free to **open an issue** or submit a **pull request**!
