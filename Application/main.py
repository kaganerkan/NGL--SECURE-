#############
#NGL(SECURE)# => Version 0.1
#############

#Import modules that are required

## Framework module
import streamlit as st
## Utility modules
import requests,json,time,uuid
from datetime import date
## Error handling modules
from requests.exceptions import RequestException
from urllib3.exceptions import NameResolutionError

# Setups
nglAPI = "https://ngl.link/api/submit" # NGL BackEnd-API
codeVersion = 0.1 # Version of appication
# Functions
def getUtcOffset():# Get the time zone offset in seconds from UTC
    timezone_offset_seconds = time.timezone
    offset_hours = timezone_offset_seconds // 3600
    if offset_hours > 0:
        return f"UTC-{offset_hours}"
    else:
        return f"UTC+{abs(offset_hours)}"
    
def log(report,senderFunc,repType):#Logs details with information such as time, timezone,date,date format, where the logging made from, what type it is.
    print(f"""\n----\n[{senderFunc}]\n[{repType}]{report}\n[{date.today().strftime("%d/%m/%Y")}/(day/month/year)][{time.strftime("%H:%M:%S", time.localtime())}/{getUtcOffset()}]""")

def sendToNGL(target,message,gameslug="",proxyMod=False,proxyDetail="xxx.xxx.xx.xx"): # Function to send NGL site a request.
    url = nglAPI
    try:
        data = {
            "username": target,
            "question": message,
            "deviceId": uuid.uuid4(),
            "gameSlug": gameslug,
            "referrer": ""
        }
        
        if proxyMod:
            proxies = {
            "http": "http://"+proxyDetail,
            "https": "http://"+proxyDetail
            }

            response = requests.post(url, data=data, proxies=proxies)
        else:
            response = requests.post(url, data=data)
        status,additionalexplanation = "Succes",""
        log(f"Succes","Func sendToNGL-main.py","Succes")
        return status, additionalexplanation
    except NameResolutionError as e:
        log(f"Failed to resolve the host: {e}","Func sendToNGL-main.py","Error")
        status,additionalexplanation = "NameResolutionError","NameResolutionError: \n This occurs when a program can't find the network address (like IP) associated with a domain name. This typically happens due to issues with DNS (Domain Name System), such as misconfiguration, server problems, or connectivity issues."
        
        log(f"Network Connection Result:{response.status_code}","Func sendToNGL-main.py","Info")
        log(f"Network Connection Result:{response.text}","Func sendToNGL-main.py","Info")
        return status, additionalexplanation
    except RequestException as e:
        log(f"An error occurred during the request: {e}","Func SendToNgl-main.py","Error")
        status, additionalexplanation = "RequestException", "RequestException: \n This occurs when there is an ambiguous exception while handling an HTTP request. It can happen due to various issues like a timeout, invalid URL, or connection problem."
    
        log(f"Network Connection Result:{response.status_code}","Func sendToNGL-main.py","Info")
        log(f"Network Connection Result:{response.text}","Func sendToNGL-main.py","Info")
        return status, additionalexplanation
    except Exception as e:
        log(f"An unexpected error occurred: {e}","Func SendToNGL-main.py","Error")
        status, additionalexplanation = "UnexpectedError", "UnexpectedError: \n This occurs when something unexpected happens during the program's execution. It could result from bugs, unhandled exceptions, or unforeseen conditions in the code."
        
        log(f"Network Connection Result:{response.status_code}","Func sendToNGL-main.py","Info")
        log(f"Network Connection Result:{response.text}","Func sendToNGL-main.py","Info")
        return status, additionalexplanation

def loadConfig(configFile): # Used for loading config.json file inside 
    try:
        with open(configFile, 'r', encoding='utf-8')  as file:
            config = json.load(file)
            log("Config Is Loaded","Func loadConfig-main.py","Info")
        return config
    except FileNotFoundError:
        log(f"Error: The file {configFile} was not found.","Func loadConfig-main.py","Error")
    except json.JSONDecodeError:
        log(f"Error: Failed to parse {configFile}. Ensure it contains valid JSON.","Func loadConfig-main.py","Error")
    except Exception as e:
        log(f"An unexpected error occurred: {e}","Func loadConfig-main.py","Error")
    return False

#Lunch 
## Setup
config = loadConfig("config.json")

## Layout written
st.title(config["application"]["name"])
if config["visibility"]["letUserSeeVersion"]:st.caption("version"+str(codeVersion))

userToSend = st.text_input("Instagram Account's Name")
messageToSend= st.text_input("Message")

### Loading optional setting modifiers after checking config.
if config["visibility"]["letUserSelectMod"]:gameSlug = st.selectbox(label="Mode(optional)",options=["","confessions","wfriendship","3words","rizzme","tbh","shipme","yourcrush","cancelled","dealbreaker"])
if config["visibility"]["letUserProxySelection"]:
    proxySetting = st.checkbox("Use proxy servers.")
    if proxySetting:
        proxyDetail = st.text_input("Proxy ip and port:")
        st.warning("Helps hide ip but most proxy servers are blocked by NGL.")

### Sending message and button
infoBox = st.empty() #Create box to use after to show message so it dosent look bad.(Rather then under now its over the button)

if st.button("Send NGL Message"):
    try:        
        status,explanation = sendToNGL(userToSend,messageToSend,gameSlug,proxySetting,proxyDetail)
        if status in ["NameResolutionError","RequestException","UnexpectedError"]:
            if config["visibility"]["letUserSeeErrors"]:log(f"Showed user an error message with explanation","streamlit running application after sendToNGL-main.py","Info");infoBox.error(f"Result is {status}. {explanation}")
            else:log(f"Showed user an error message without explanation","streamlit running application after sendToNGL-main.py","Info");infoBox.error("Resulted with a error.")
        else:
            log(f"Showed user an info box explaining message is send.","streamlit running application after sendToNGL-main.py","Info")
            infoBox.info(f"Message Send To {userToSend}.")
           
    except:#Add here a devlog(WIP)
        status,explanation = sendToNGL(userToSend,messageToSend,gameSlug)
        if status in ["NameResolutionError","RequestException","UnexpectedError"]:
            if config["visibility"]["letUserSeeErrors"]:log(f"Showed user an error message with explanation","streamlit running application after sendToNGL-main.py","Info");infoBox.error(f"Result is {status}. {explanation}")
            else:log(f"Showed user an error message without explanation","streamlit running application after sendToNGL-main.py","Info");st.error("Resulted with a error.")
        else:
            log(f"Showed user an info box explaining message is send.","streamlit running application after sendToNGL-main.py","Info")
            infoBox.info(f"Message Send To @{userToSend}.")