# MYSITE / ProjectView App

this is mysite, holds my Django Apps in one place. The main app is called ProjectView.

## About ProjectView:

### Purpose of this app:

This app is intended for **project / team leaders** working for companies providing **development / engineering** services for the **automotive industry**. I myself come from this field and work as a project leader in such a company. As a project leader I was always missing a tool such as this app. I needed a kind of digital control panel, where I would have all the information from all projects in one place - including protocols from meeting, to-do lists, contacts etc. Accessable from any place, at any time. I believe that with some adjustments, this app would also do fine in just about **any industry**, not only in the automotive one.

### Technical details:

I built this app using **Python** and the **Django** framework on the backend. I chose **SQLite** for the data base, but I'm thinking of switching to something more suited for multiple users. The front end is pure **HTML, CSS and JavaScript** plus a little bit of **Bootstrap & Crispy Forms**. To create this app I used the following tools: **Visual Studio Code as IDE, GitHub for version control**. To set it up online I bought a **Raspberry Pi**, which I then set up as a ***Linux** server using **Apache2**. The domain has an SSL certificate, the firewall allows 443 traffic only. The Django deployment check list has been completed. Recomended browsers: Firefox and Chrome

Even though this is a **full stack project**, I like to think of myself more as a backend kind of guy.

### Functionality:

The ProjectView app provides the following functionality:

A folder like structure of **OEMs** (original elements manufacturers e.g. BMW, Tesla), **Projects, Modules, Parts, Topics**

**A part area** where all the information about a part is held, including a section for types and amounts of fixing elements (many to many). There is also a list of topics, which can be viewed as a compressed view, or a protocol view (so that one can easily print out all topics including all entries and pictures as a pdf file or on paper)

**A topic area** which is used during meetings. During a meeting the user can edit, or create a new topic, **set a chosen priority** for the topic, add information, pictures & entries. This way you can easily create **documentation on the fly** during a meeting. **Entries** concist of entry date, solution and deadline. Entries are **coupled with project participants**. From the project participants pool, at least one participant must be chosen as 'responsible', one as 'involved' and one as the one with whom the given entry was agreed with.

**A project participant area**, where all information about all the project participants is held e.g. for whom the participant works, his job title, contact details, list of projects this person is involved in.

**A to-do area** for the project leader to maintain their tasks. This area includes a field where the responsible design engineer is set. As soon as a to-do item is created, or modified, the person responsible receives an **email notification** that a new task is ready (or an exitsting task has been modified). The responsible design engineer then clicks a link in the email to see the task, upon doing so the project leader is informed that the person has seen the task. To-do items also have a statuses (currently **'priority'**, **'in process'** and **'settled'**), which can be **easily changed simply by clicking on the icon**.

**myParts area** which is basically a favourites area, where the project leader keeps a list of the parts they are currently taking care of.

Search box which will be intoduced soon.

### Cool features:

**adding pictures simply by copy-paste** - very handy during a meeting. This feature is possible thanks to the **Javascript fetch method**, which allowes adding many pictures directly to the database without having to refresh the page. **CSRF prevention** is present.

switching between **compressed view** and **protocol view** without having to refresh the page (JavaScript)

adding, removing myParts without having to refresh the page (JavaScript)

adding/editing/removing entries whilst editing a topic without having to refresh the page

**Email notification** sent to the person involved as soon as a new task is created or edited

user can only modify / delete items he has created, this protects from accidentally modifying other users' data
