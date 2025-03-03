Name: Marcelo Barillas
Email: marcelo.barillas1@gmail.com
Description:
    The first half of the project began with python. I began simply by gathering the data and understanding what was needed. We had two files named people, different formats. 
    
    Looking into it deeper, I saw that they were two halfs, and I performed some python operations in order to join them together to make a full dataset. I then exported them as a full csv file (in data/people.csv). Then I cleaned up the other projects, using the missing data as well as the helper functions defined in the helpers/ folder in order to continue parsing and understanding the data. 

    I then moved onto the data visualization part of the project. This part required data visualization techniques that I learned in college. Because this was a inference project for data analytics rather than a predictive one, I leaned away from performing regressions that were needless for this project. 

    I began building images that I would be able to use in the presentation. I decided to make a presentation because, apart from hearing it in the explanation of the interview process, if I didn't complete the Express.js website I would at least still be able to provide some form of analysis on the data given. 
    The presentation link was made using presentations.ai here: https://app.presentations.ai/view/jc5xaI.

    Up until this moment, I have only used basic Python (pandas, numpy, seaborn, and matplotlib) as well as using LucidChart to create the diagram of the Entity Relationship Model in figures/.

    I wanted to go ahead and proceed now that I had that for the most part done with creating an admin dashboard for Venmito. Although they might already have one, I decided to at least provide one for live access to the database. I created a database using Supabase which is an open-source BaaS platform allowing me to interact with a Postgres database while providing authentication.  I added the cleaned files with a new recommendation that the files come that way when added to the database. This can be done by performing cleanup and then appending the new row to the database.

    After setting up the database, I performed a simple connection using Node.Js and incorporated the Express.JS framework to begin the dashboard building. In order to display the plots, I would query the data that I needed from Supabase, and then process them slightly in the app.js folder and then display then as a fetch route in the index.html folder. 
    I decided that in order to account for differences of OS's, I made a simple Dockerfile that can run the code. 

    How to run it:
        1. Install Docker[https://www.docker.com/get-started/]
        2. Open the repository locally
        3. Then run docker-compose build
        4. Finally, run docker-compose up to start the local web server.
           1. You can hit this endpoint[http://localhost:3000/]
        5. When youre done, you can exit out with Ctrl+c and run docker-compose down
   
   Again, the python portion was already performed, and is accounted for in the presentation. The Website part is the one that requires user interaction. 


1. Complete your project as described above in a branch within your fork.
2. Submit your project by creating a pull request to merge your branch to the main branch of your fork.

We look forward to seeing your solution!

Thank you,

Venmito

