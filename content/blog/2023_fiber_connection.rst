Unlocking Fiber Deployment in the town council: A Citizen's Journey of Using Data
==================================================================================

:date: 2023-02-4 21:00
:language: en
:author: eloycoto
:head: Unlocking Fiber Deployment in the town council: A Citizen's Journey of Using Data
:index_title: Unlocking Fiber Deployment in the town council: A Citizen's Journey of Using Data
:metatitle: Unlocking Fiber Deployment in the town council: A Citizen's Journey of Using Data
:tags: thoughts, work
:metatags: thoughts, work
:description: A journey how to get internet connection in our town council.
:keywords: telecoms, thoughts, government

European Union is pushing some money to all countries to develop infrastructure
for the regions. The kind of infrastructure does not matter, and the regions
ask for their needs. One of the biggest for many town councils in my area is
deploying FFTH to all homes, but as normal, some issues are in place.

I knew about these public funds! And I also knew that some telecoms operators
where I live got money to connect thousands of homes to FFTH. Sadly, time
passed, and I didn't see any development, so I started to get `suspicious
<https://acalustra.com/os-proxectos-de-fibra-optica-en-galicia.html>`_ that the
funds were not reaching the right place. So over the years, I shared this
information with all political parties to make them aware; some of them
supervised it others said I was lying. A few months ago, the new mayor called
me asking for help, so I decided to help to execute and supervise these public
funds.

After our first call with the Telecoms Operators, the information could have
been more transparent, so one of the first goals was to know if all the houses
they said have FFTH connections were correct or not, and validate their data
with mine.

To achieve this goal, I took advantage of two sources of truth:

**All houses' directions:** In Spain, there is a way to register the houses to the
govt(Catastro), so each plot has a reference number, and you know the direction
and coordinates of that house. I ended up mapping thousands of house directions
in simple GeoJson files.

**Real internet connection:** This is easy to do if you can ask the operator if you
have coverage. One of the landing pages out there has a way to know if you have
fiber connection, so it was easy to scrape all the council house directions
and, from there, map true/false.

Having this info allowed the mayor to have a lot of information; at the same
time, in April'22 we sent all the directions that were not with FFTH coverage
to the Spanish government to be able to receive funds to cover during the
following years.

During the following months, we learnt that each Wednesday, they updated the
coverage so that we could track the progress weekly. Because we have all this
information, we can chase them, follow the process and unlock the issues.

In the end, during 2022, **we ended with more than 1500 houses with FFTH**, and
more than 240 with deployment-ready, but with license issues with Spanish Govt
for the interconnection, a minor thing that should be finished in the coming
weeks.

Over this time, I learned a lot of things:

- **Social skills are needed:** I don't know how many times the deployment is
  blocked by someone who is not allowing to do certain things, like enter their
  plot to update the cables, even is good for him and all the neighbours.
- **All the people complained, and no one said thanks:** This has been an issue
  for so long in the town council, and it makes me sad that no one said thanks
  when the deployment was successful. Incredibly, a neighbour called me every
  week to complain; when he got his 1GB fiber connection, he didn't call me to
  say thanks!
- **Geojson is cool, but not performance enough:** A friend told me, but it's
  not going to work because of the performance, I can manage it, but I ended up
  with more than 10GB of Geojson information.
- **Ask for help:** It was cool that I made the small framework to get all the
  data, and  Adri took it to the next level; he updated all the maps weekly and
  helped me with some context information and added some cool features to our
  maps

Overall, I'm super happy to do this pro-bono project. Over the years, I had
this problem, and I needed to work with a crappy 4G connection. I learnt how
difficult it is to deal with the town council, government, and telecoms
operator, and not only having the data but also helping the telecoms unlock
their deployments. It makes me happy the public funds reach almost all people
and make a difference in how the town council tackle issues with data, so it
has been an excellent experience for me.
