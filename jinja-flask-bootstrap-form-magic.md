I'm proud of myself today. 

I knew there had to be a better way to get forms to render, and today I thought back to the wtf.quick_form function I saw awhile back, that is part of the flask-bootstrap package... 
I don't want the whole package (although I am using it for now), but I went to their github to see how they do this, and what I found was perfect (but hard to break down at first). 

First, [the code](https://github.com/mbr/flask-bootstrap/blob/3e2695bb36f29bf72befce86c9e63609c3016203/flask_bootstrap/__init__.py). There is a lot, and it's terribly formatted, but it's not that bad. 

There are macros, which are just functions in the template

Macros:
1. quick_form
    this is the top level. this is what we call from other templates that want to render a form
2. form_field
    might be a little recursive... which i don't like 
    either way, in quick form, we use {{for field in form}}, which gives the fields of the form, and they are each passed to `form_field` which has the logic to render each form field (and it's erors using form_errors) based on the type of field it is. 
    not that crazy, just looks intimidating at first. 
    I should use this for all the forms. They will have uniform formatting and I won't have to mess with all the bs

    getting the turbo-frames to work will be fine, but I will need to have the naming schema down really well between backend and templates
