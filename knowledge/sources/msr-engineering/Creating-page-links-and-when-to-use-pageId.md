#What is pageId?
`pageId` is an element of the URI for an Azure DevOps wiki page. You can see examples of how it's intended to be used by looking at the [REST API documentation](https://docs.microsoft.com/en-us/rest/api/azure/devops/wiki/pages/get%20page%20by%20id?view=azure-devops-rest-5.1) for ADO, but for our purposes, it's largely something to be avoided, as it effectively makes links to wiki pages more fragile. Azure DevOps internally seems to handle changes to the ID without difficulty, but some operations (deleting and reverting the delete, for example) can result in a new Id for the same content.

#Why avoid it or why keep it?
In December 2019, we had a problem where someone deleted a page accidentally. Since ADO wikis are just Git repositories mostly populated by Markdown files, we reverted the deletion, but upon doing so, the `pageId` of deleted page was not what it was prior to deletion. If we want to avoid that scenario, we can create links without `pageId` values by following the process outlined below.

However! We shouldn't. pageId doesn't change when a page is renamed, but the path to a page changes when that page or any of its parent pages are renamed or moved. So our options are two optimize for one of two scenarios:
- People renaming pages, which happens often. Using pageId in the link means that a link to this page with a `pagePath` of `/foo/bar/baz` will still work, as the path is ignored in favor of the Id.
- People accidentally deleting pages, which has happened once as far as we know. If this happens, a new `pageId` is generated and the ADO team has confirmed that there's basically nothing we can do about it to fix existing external incoming links that include `pageId`. We can protect ourselves from this scenario by stripping pageId out and instead using `pagePath`.

So if we use pageId, we're out of luck if someone deletes a page on accident, but if we don't use it, we have to decide not to rename or move pages or face corrupting external incoming links. Since the renaming is vastly more likely than the accidental deletion, the most effective approach is to continue using normal links, which include `pageId`. They're easier to make (just copy the URI) and will be more robust in the majority of scenarios.

----

#Creating an Id-less link
If you have a good reason to do so, this will help you avoid `pageId`.
Instead of simply copying the page's URI out of the browser's address bar (which will include a `pageId`), you can create a link that uses the `pagePath` query string parameter to avoid any ephemeral identifiers except the title. 

This is an example of a link with the `pageId` (copied from my address bar when viewing this page) which we want to avoid in our publications. `pageId` is the underlined and bolded portion in the example:
<span style="display: block;unicode-bidi: embed;font-family: monospace;white-space: pre; background-color: #EFEFEF">http<span>s://dev.azure</span>.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki/<u><b>2322</b></u>/Creating-pageId-less-links</span>

The giant mess below is an example of a link to the same page from edit mode:
`https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki?wikiVersion=GBwikiMaster&pagePath=%2FProcess%20and%20Reference%2FGeneral%2FCreating%20pageId%252Dless%20links&pageId=2322&_a=edit`

Note that it still contains `pageId` value, so we'll want to clean it up by stripping some of the query string parameters. If you remove, `pageId=2322`, `_a=edit`, and `wikiVersion=GBwikiMaster`, you'll end up with a shorter link that won't break if the pageId changes:
`https://dev.azure.com/msresearch/MSR%20Engineering/_wiki/wikis/MSR-Engineering.wiki?pagePath=%2FProcess%20and%20Reference%2FGeneral%2FCreating%20pageId%252Dless%20links`

#Gotchas
It should be noted that a deeper link has more points of failure in that renames to any of the parent pages will break any links to itself _and all of its children_. This is true with both link types.

#History
As mentioned previously, this page exists because we had some links get broken because their `pageId` changed. We initially thought that created links without `pageId` would be a solution, but didn't realize that the page's Id functions as a permalink even when the name changes. This page is left primarily as a reminder for next time.