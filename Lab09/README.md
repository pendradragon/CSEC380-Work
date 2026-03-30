# Lab Overview

When new security vulnerabilities appear, like the recent XZ vulnerability, it is often important for security researchers to be able to recreate the vulnerability and the associated attack as a part of the risk assessment process. Towards that end, in this lab, students will set up a web application that is not explicitly intended to be vulnerable and replicate some previously reported vulnerability.
The focus of this lab will be client-side vulnerabilities. Lab #10 will be similar and will focus on server-side vulnerabilities.


# File Explanation
- **docker-compose.yml**: Since qdPM 9.1 is a __depreciated software__ it relies on older versions of mySPL, PHP, and Apache to run. Older versions of this software is installed in container as a result. 
