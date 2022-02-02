## Turbo Frames

Having an epiphany with turbo frames. 

Right now, I have an example at `main.profile_update_form()`. I was curious why, when I submit a frame to get a form, then I submit the form, why doesn't it show me the original link? Well, **it's because I wasn't sending the link code back!!** In `profile_update_form()`, you can see that when the form validates, it then return the original link tag, which is hte code that allowed me to get the form in the first place. 
I need to return that orignal code back on success so it updates the page in place. 

I will also want to update the fields within the profile page itself, which I think can be done with just turboframes, but I'm not sure how yet... 


## Notes from Video: https://www.youtube.com/watch?v=eKY-QES1XQQ&ab_channel=GettingReal
The form at 4:18: when you click the top edit button, to edit the room, that is just a turboframe, where it is switching back and forth. 

The bottom one, where you send a message, is reloading the entire page, lazily, when you submit, which is why the new messages show! (the target=_top for this one... which makes sense! I was really stuck on how the new messages were showing up)

#### Cool hack from video: the network tab of dev consoles
He is using the network tab of the browser dev consoles to look at the requests that are being made and the responses coming in,,, you can even see a preview of the html, which in the base of turboframes, are individual components... super cool!!!