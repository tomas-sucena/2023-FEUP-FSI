# WordPress CVE

## 1st flag

Upon accessing http://ctf-fsi.fe.up.pt:5001, which redirects to a website hosted by WordPress, we started investigating the several pages in search of potential clues.
Since the platform appeared to be a virtual store, we decided to check out the services for sale. 
That is when we stumbled across the following user-review:

![img.png](../images/review.png)

This led us to believe that we could exploit vulnerabilities in the plugins to hack the server.
By clicking on a tab beside the review, we discovered all the plugins and respective versions:

![img.png](../images/wordpress_plugins.png)

With the newly acquired information, we opened [CVEdetails.com](https://www.cvedetails.com/) to discover the CVEs associated with each plugin.
Considering our objective, we focused on vulnerabilities that allowed authentication bypassing.
After a thorough examination, we came across an entry for versions 5.4.3 and below of Booster whose description mentioned logging in as other users, including administrators: CVE-2021-34646.
Inputting `flag{CVE-2021-34646}`, we overcame the first challenge.

