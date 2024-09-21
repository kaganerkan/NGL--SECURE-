# NGL-(SECURE)

# Whats About "Secure"?
## What this defend you from:
This application directly connects NGL site's Back-End API.  Normally when doing this or Front-End API site grabs your ip and device id and sells this to questions publisher as a location etc. information. This is wrong for many reasons but mainly because its a "anonymous" way to ask questions.
## How does it defend you:
Application has built in proxy setting to turn on for to hide your ip, also location since that is how they got it in first place, meaning they will be selling nothing more then a fake location. It also has built in way to give site API fake device id so no reason to fear that to.

# How to use it properly
## Proxy settings:
Open app config and look for "letUserProxySelection". It should look like:

	"visibility":{

        "letUserSeeErrors":false,

        "letUserSelectMod":true,

        "letUserSeeVersion":true,

        "letUserProxySelection":true

    }

from here turn that "true".

## Device id
Device id is already secured and given randomly you cant disable fake device id method without modifying the code.
 
