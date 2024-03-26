# APP : FinalChecker (lab) 
Web App for checking for unwanted changes right before signing a contract. 

## Description 
User story : As a user, I want to make sure the contract I have been asked to sign is identical to the final version that I have agreed to.  

Experimental Web app that checks for unwanted changes to the contract. The web app accomplishes this by comparing (1) the version of a contract that had been agreed upon and (2) the version that had been sent out for signature (via e-signature). 

## how to use 
User uploads the (1) the versiono of the contract that had been agreed upon and (2) the version that had been sent out for signatures. Both in PDF format. 
App will compare the text in the contracts word by word (but will ignore text that had been added by docusign for the purposes of tracking esignature authenticity)  

## Installation 
```
pip install -r requirement.txt 
```

## Requirements

- PyPDF2==3.0.1
- streamlit==1.32.2

## Contributors 
- ChatGPT 4.0 : generated based code


