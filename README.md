# crypto-storage

## ***Secures your files in the cloud***

**Project Members:**
  *Victor Veliz and Phuc Pham*

## Problem Statement

Freedom is one of the most basic needs for human society in which includes the freedom of the Internet. As Snowden revealed before, the U.S. government censored our Internet. Protecting our privacy on the Internet is the motivation for this project. In today’s Internet world, the cloud is becoming the digital storage of our personal digital belongings, which range from storing sensitive documents, pictures, and other digital media. But housing all of this personal information in the cloud comes at a great risk: security threats from hackers and the actual cloud itself. So what are you going to do?

## Proposed Solution/Approach

Our first implementation is to support only encrypting files. The current file size(TBD) is limited to a small file size to prevent data processing errors during upload/download. Encrypting a folder and sharing a file between users will be supported later when we have time. Cipher only attack is the attacking model this project is built to against. In order to protect information stored in the cloud, we will encrypt your information before it is transferred to the cloud. The cloud will keep your information encrypted; therefore, the cloud company who provides the cloud storage as well as hackers will not see the content of your file(s). Instead, they will see nonsense words. We are planning on using a private server as a small private cloud. Our critical mission is protecting the user’s files stored on that server. The communication channel between the server and the client is secured by using OpenSSL. On the client side, user has to register their username and password with the server. A user has to login to the web application in order to encrypt/decrypt a file. It helps against unauthorized users to get access to the database. Additionally, it also helps each user get access to the right files to determine to whom it belongs. Using a password will help to maintain message integrity over the communication. When a user signs up for an account, strong encryption keys for the user’s account will be automatically generated and encrypted with user’s password. The plain user’s password will never be sent to the server but the hash(SHA-2) of the password will be sent to the server. So the user’s password is the secret formula to allow the user decrypt their data alone, thus the password MUST not be forgotten. To protect data integrity, we will take a SHA-2 hash of that file before it is encrypted and SHA-2 hash of the encrypted file. Those SHA-2 hashes will be encrypted and will be stored in the server. In addition, those SHA-2 hash will also be used to verify when the user downloads their file locally to their PC.

## Detailed Implementation

**Platform:**

- Windows - For development of our source code. Microsoft Azure free
- Dreamspark account - Web app
- django framework. https://www.youtube.com/watch?v=M_WHS_CfHlo

**Programming Languages:**

- HTML5.
- Javascript.
- Python.

**Tools for development:**

- Visual Studio Community 2013 for our IDE.
- git - For our source control.

**Other Considerations:**

**Mysql Tables for:**

- User Info: Table to store user info (login name, e.g.)
- Message integrity (hash) : Keep the hashes in a table on the server
   side (FileTable).
- Encrypted file Hash

- Original File Hash

- OpenSSL

- django cryptography(django.core.signing)? - For secure key passing
https://docs.djangoproject.com/en/1.8/topics/signing/#protecting-the-secret-key

- HTML website for the client side. Possibly have javascript to compose
   (encrypt the file to be sent to the server).

- Use Javascript CryptoJS library on the client side to encrypt file,
   and file hash info.
http://tutorialzine.com/2013/11/javascript-file-encrypter/

- Python scripts - On the server side to do all the processing:

- Check data integrity(do the file hash comparison, etc)

> Password: Minimum requirements for password(e.g. password length 12-32
> characters) Password attempts ( Only 3 attempts. After 3 attempts,
> account is locked. Account must be unlocked by rigorous user
> verification process).

## **Getting Started**

I'm using macOS, so if you are a Windows user, commands may differ.

System requirements:

- python v3.X+ (at writing using v3.7)
- Django v3+

For development purposes:
Assuming you have cloned the project,

1.Create an env.json file outside of this project folder.

```json
{
        "DJANGO_SKEY": "<secret_key>"
}
```

Replace <secret_key> with a random alphanumeric value.

2.Create a virtual environment.
If you don't have virtualenv installed on your system, execute:

```shell
python3 -m pip install --user virtualenv
```

Now create the virtualenv

```shell
python3 -m venv env
```

Change into the virtualenv folder (env)

```shell
source env/bin/activate
```

And install the python requirements
```shell
python3 -m pip install -r requirements_local.txt
```
Note: Note requirements_local.txt includes all of the requirements.txt packages
in addition to the Django's debug tool.

3.Perform database migrations. Note that for development purposes,
We are using sqlite. For production use, you should use a relational database.

```shell
python3 manage.py migrate
```

4.Create a super user for administration.

```shell
python3 manage.py createsuperuser
```

5.Run the local test server.

```shell
python3 manage.py runserver localhost:8095 --settings=CryptoStorage.settings.local
```

Note: For production, use settings.production

6.On your browser, navigate to http://localhost:8095
You should now be running a local test server.

## **Basic Usage**

Now that you have configured the local test server, for testing purposes,
use the same credentials that were used by the super user above to login. Note: You
may create other users by clicking the link "New Registration User".

Once logged in, you will upload the encrypted file to the server, then you can download the file and decrypt it using your login password.

That's it. Project is simple to show how we can encrypt data at rest by uploading it to the server from the client.

## **Timeline and workload distribution among teammates:**

Team Member Assigned: Phuc & Victor
Project: HTML Application with Javascript
Due Date: 10/10/2015

Team Member Assigned: Victor
Project: Python module for MySQL creation
Due Date: 10/20/2015

Team Member Assigned: Phuc
Project: Secure Session (HTTPS) client and server.
Due Date: 10/25/2015

Team Member Assigned: Victor
Project: Encryption Implemantation & Generation of "MasterKey"
         based on user password.
Due Date: 10/29/2015

Team Member Assigned: Phuc
Project: Python module for MySql database interfacing.
		 User profiles.
Due Date: 11/01/2015

Team Member Assigned: Victor
Project: File Upload <ENCk(file)> - Test & Verify.
Due Date: 11/05/2015

Team Member Assigned: Phuc
Project: File Download <DECk(file)> - Test & Verify.
Due Date: 11/09/2015

Team Member Assigned: Phuc & Victor
Project: Check for Vulnerabilities on code & server(Azure).
Due Date: 11/15/2015

Team Member Assigned: Phuc & Victor
Project: Final Evaluation & Testing.
Due Date: 11/22/2015

Team Member Assigned: Phuc & Victor
Project: Ready for completion and submission
Due Date: 12/01/2015

> Written with [StackEdit](https://stackedit.io/).