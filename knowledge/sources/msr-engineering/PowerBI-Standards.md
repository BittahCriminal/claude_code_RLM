[[_TOC_]]

# Look and Feel
We are using a simple, color blind friendly theme, called Simply Modern Light for our reports. This theme is obtained from the PowerBI community theme gallery and freely available. The JSON file for the the theme is attached here, but it's worth checking [the gallery](https://community.fabric.microsoft.com/t5/Themes-Gallery/Simply-Modern-Light/td-p/2087814) occasionally for updates or corrections to the theme.

All of the colors, styling and element scaling included in the theme should be followed througout all of your report pages.

[Metricalist-Simply-Modern-Light.json](/.attachments/Metricalist-Simply-Modern-Light-4bdedfbf-f6c0-48df-98b2-1794bca8df20.json)

![theme.png](/.attachments/theme-6d59fb92-7d2e-4768-9330-db7236ec30c1.png =650x)

## General Aesthetic Guidelines and Design Rules
### Fonts
The above theme includes a couple of fonts in various weights. It's best to stick with the provided fonts and avoid adding more, as it becomes distracting and messy the more fonts you add. The design language of the report should tell the viewer to expect headings to be a certain font, weight and size and content or legends to be another. This helps the viewer quickly understand the contents of the report and how it's organized.

### Graphics
Charts and other standard elements included with PowerBI should respond to the theme and blend in nicely with your reports. There are a number of additional visuals available in the PowerBi AppSource marketplace that may or may not adapt to the theme. Use discretion when adding these elements, or your report may quickly become a disjointed eyesore. 

### Layout
Keep similar chart sections and their backgrounds the same size, except when necessary for larger or longer graphs. Don't try to crowd too many complex graphs together in one section, move large charts with many values to a dedicated line or section. Try to balance the placement of different grpahical elements on the page so that they look neat and are easy to pick out visually.

Our theme has a default spacing for chart elements and their boxes, try to maintain the same spacing throughout all of your report pages. Also pay attention to the padding within your boxes, keep even spacing between your content and your background elements. Visual consistency makes a report look professional and well made.

##Content
###Graphics
When deciding to add content, make sure that you are answering a question that has been identified as needing to be answered and that you are using the appropriate visual format for presenting the answer. As an example - a pie chart is not suitable for a large number of values, it will be difficult to read and takes up more and more space, the more values you add.

![badpie.png](/.attachments/badpie-deefcd79-3363-42a4-8c24-bc3201604a76.png =250x)

##Headings and Titles
Name your report elements in an obvious way, with enough detail that users don't have to spend time figuring out what they are. Use consistent font, size and color for titles and data labels.

# Security
- Use service accounts for refreshing report data to PowerBI, not user credentials.
- Do not publish personal information, or Microsoft confidential information without going through reltrack.azurewebsites.net and getting approval from Compliance.
- Always review the contents of your reports with RTE leadership to ensure you are sharing data with the appropriate people, even within our own division. 

We use a simple text box matched to our theme to denote confidential data in way that is immediately visible. The box should be placed in the upper right corner as shown below to maintain a consistent look and feel to our reports.

![confidential.png](/.attachments/confidential-39c1d665-b08c-4603-a456-fd48b75ca110.png =650x)

