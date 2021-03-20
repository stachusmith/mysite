# MYSITE / ProjectView App

this is mysite, holds my Django Apps in one place. The main app is called ProjectView. Next one up - SpotifyRandomizer

## About ProjectView:

### Purpose of app:

This app is intended for **project/team leaders** working for companies providing **development/engineering** services for the **automotive industry**. I myself come from this field and work as a project leader in such a company. As such I've always been missing a tool such as this app. I needed a kind of digital control panel, where I would have all the information from all projects in one place - including protocols from meeting, to-do lists, contacts etc. - accessable from any place, at any time. I believe that with appropiate adjustments, this app would be invaluable in just about **any industry**, not only in automotive concerns.

### Technical details:

I built the app using **Python** and the **Django** framework on the backend. I chose **SQLite** for the data base, but I'm thinking of switching to something more suited to multiple users. The front end is pure **HTML, CSS and JavaScript** plus a bit of **Bootstrap & Crispy Forms**. To create the app I used the following tools: **Visual Studio Code as IDE, GitHub for version control**. To set it up online I bought a **Raspberry Pi**, which I then set up as a **Linux** server using **Apache2**. The domain has an SSL certificate; the firewall allows 443 traffic only. The settings have been verified in accordance with the Django deployment checklist. Recommended browsers: Firefox and Chrome

### Functionality:

The ProjectView app provides the following functionality:

A folder-like structure of **OEMs** (original elements manufacturers, e.g. BMW, Tesla), **Projects, Modules, Parts, Topics**

**A part area** where all the information about a particular part is held, including a section for types and amounts of fixing elements. There is also a list of topics, which can be viewed in compressed view, or protocol view (so that one can easily generate all topics, including all entries and pictures, as a pdf file or printout).

**A topic area** for use in meetings. During a meeting the user can edit a topic, create a new topic, **set a chosen priority** for the topic, add information, pictures & entries. This way you can easily create **documentation on the fly** during a meeting. **Entries** consist of entry date, solution and deadline. Entries are **coupled with project participants**. From the project participants' pool, at least one participant must be chosen as the person 'responsible', one as 'involved', and one as the person the entry was agreed with.

**A project participant area**, where all information about all the project participants is held, e.g. who the participant works for, theit job title, contact details, list of projects they're involved in.

**A to-do area** for the project leader to maintain their tasks. This area includes a field where the responsible design engineer is designated. As soon as a to-do item is created, or modified, they receive an **email notification** that a new task is ready (or an existing task has been modified). They then click on a link in the email to see the task, and the project leader is informed that the engineer in question has seen it. To-do items also have statuses (currently **'priority'**, **'in process'** and **'settled'**), which are **easily changed by simply clicking on the icon**.

**A myParts area**, which is basically a 'favourites' area, where the project leader keeps a list of the parts they are currently dealing with.

**A search box** (to be introduced shortly).

### Cool features:

**adding pictures simply by copy-paste** - very handy during a meeting. This feature is possible thanks to the **JavaScript fetch method**, which allows many pictures to be added directly to the database without having to refresh the page. **CSRF prevention** is present. The same function also **resizes** the clipboard image to a reasonable magnitude, so as to avoid saving unnecessarily large images in the database.

switching between **compressed view** and **protocol view** without having to refresh the page (JavaScript)

adding or removing myParts without having to refresh the page (JavaScript)

adding/editing/removing entries whilst editing a topic without having to refresh the page

**Email notification** sent to the person involved as soon as a new task is created or edited

user can only modify or delete items they have created, thus preventing accidental modification of other users' data
