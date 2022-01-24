- turbo-frame redirects are a bit confusing, but I found this resource that was helpful: https://turbo.hotwired.dev/handbook/frames#targeting-navigation-into-or-out-of-a-frame. When I want to redirect from my register-form or login-form, I need to set the target="_top" on the turbo-frame, but then it only allows me to redirect on success, but not show the errors... 
    - for now, the solution is to show error messages with turbo streams, and use _top to redirect. This means that for right now, when there are errors, I return a 400 with a string message and the page doesn't change. This is working, but I see 
```javascript
turbo.js:17 Error: Form responses must redirect to another location
    at A.requestSucceededWithResponse (turbo.js:3:6617)
``` 
in the dev console of the browser, which seems bad... oh well for now. 