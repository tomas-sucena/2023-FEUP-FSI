# XSS + CSRF

In this CTF, we are required to perform a XSS attack on a website where only an administrator should be capable of providing us with the flag.

## Exploration

Upon accessing http://ctf-fsi.fe.up.pt:5004, we started investigating the website. Considering the title of this challenge, we were particularly interested in understanding the requests it could make.
The pages we found are listed below:

### Input Page

![img](images/website_input.png)

This page allows us to input a message for the admins to review. When the "Submit" button is pressed, that message is displayed in the following page.

### Request Page

![img](images/website_show_test.png)

This new page displays our request message. If we look closely, by inspecting the page, we may notice our request is written within the HTML code.

![img](images/website_source_test.png)

By pressing the hyperlinked label in this page, we are redirected to the page where the admin reviews requests.

### Admin Page

![img](images/website_admin.png)

In this page, we may notice there is a button "Give the Flag" with which the admin will supposedly approve one's request.
This button's contents within the HTML page may be very valuable to capturing the flag.

To look for vulnerabilities, we chose to start by checking if the input in the request is validated before being inserted in the following HTML page.

![img](images/website_alert_input.png)

![img](images/website_alert.png)

![img](images/website_alert_source.png)

It turns out that actually was the answer! The request's content is not validated! Given the admin will review our request, we are likely to be able to inject some code that forces them to give us the flag.

## Execution

We need to get the admin to click the "Give the Flag" button from the Request Page. With the found vulnerability it is clear we can add any HTML elements, including JavsScript code.
Here's our idea:

1. Make a HTML form similar to that present in the admin's page
2. Make it so that whenever the admin's page is loaded, we force them or their client to post the form

For step 1, we copy the code used on the admin's page and add an id to the form.

```html
<form id="exploit" method="POST" action="http://ctf-fsi.fe.up.pt:5005/request/1b735e8c7a1c8a6aae9315e8f9f18d259aaff761/approve" role="form">
    <div class="submit">
        
        <input type="submit" id="giveflag" value="Give the flag" enabled>
        
    </div>
</form>
```

For step 2, we can make use the script tag to execute JavaScript code which will submit the form above.

```html
<script>
    document.getElementById("exploit").submit();
</script>
```

Now if we put all of this together and submit it in the Input Page, we can see that the Request Page now redirects us to a forbidden page, likely the one that approves requests!

![img](images/website_exploit_input.png)

![img](images/website_forbidden.png)

This is a good sign, since it means we are trying to make the same request as the "Give the Flag" button, but we do not have permission to do it. Now we need to wait for the admin to enter the Request Page.

There was one problem with this approach, however. Since we are always redirected, we are unable to view the request page and thus we are unable to actually check the flag!
To solve this, all we had to do was disable JavaScript in our browser. After doing so and waiting for the admin to visit the page, we successfully found the flag!

![img](images/website_flag.png)