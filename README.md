# MOOFIS - Movies and TV Shows Tracker
#### Video Demo: https://youtu.be/UiVTSp28hr0
#### Description: This application allows users to keep track of their favorite movies and tv shows. It works as a wish list where you can add the movie you want to watch and the information will come directly from IMDB database via the OMDB API and categorize them as either watched or to-watch. With a clean dark mode interface styled with Bootstrap, confortable to access in the evening before your movie time, it´s intuitive and responsive. Developed with HTML, CSS, Bootstrap, JavaScript, Flask (Python) and Sqlite.

#### Project Overview: The main motivation behind this project was to create a personal media tracker. My husband and I always watch some movies and shows every night, and we had a simple notepad file to track our wish list. Automate it makes our life simpler and it's a usefull gadget for the CS50 final project. The application is lightweight, customizable, and centered on usability. It wants to maintain a minimalist list of what the user have watched or plan to watch.

#### The app allows:
- Add a movie or show by entering the title (autocomplete powered by OMDB).
- Optional manual input of IMDB ID.
- Classify the entry as a Movie or TV Show.
- Display media in separate sections: movies, shows and watched.
- Display a poster image, and information about the movie or show (powered by OMDB).
- Mark entries as watched or delete them.
- View external link to IMDB if avalable.

#### Application Structure:
- app.py: The main Flask app file, resposible for routing and logic. It uses Flask, render_template, request, redirect, and sqlite3 to manage the app's behavior.
- Main Routes:
    - /: Home route. Displays the form for adding new movies or shows and the list of unwatched entries. Handles both GET and POST requests. The POST request captures form inputs and inserts them into the SQLite database.
    - /movies: Lists all movies by querying the database for entries marked as type 'movie'.
    - /shows: Lists all TV shows, similar logic as above.
    - /movies/watched: Lists all watched movies by querying the database for entries marked as watched and of type 'movie'.
    - /shows/watched: Lists all watched TV shows, similar logic as above.
    - /movies/<id>/watched: A POST route that updates the watched status of a given movie or show by its ID.
    - /movies/<id>/delete: A POST route that deletes a movie or show from the database by ID.
    - templates/: Contains Jinja2-based HTML templates:
        - layout.html: The base HTML template. Includes Bootstrap, custom fonts, dark theme setup, and common layout elements like navbar and footer.
        - index.html: Home page template containing the add form and the list of current unwatched entries.
        - movies.html: Displays all entries marked as type 'movie'.
        - shows.html: Displays all entries marked as type 'show'.
        - watched_movies.html: Displays all entries marked as watched and type 'movie'.
        - watched_shows.html: Displays all entries marked as watched and type 'show'.
    - static/: Directory for custom CSS.
    - requirements.txt: Lists Python dependencies, including Flask and requests

#### Database Schema: The application uses a simple SQLite database with one table to store media entries. Each entry includes fields such as id, title, imdb_id, type (movie or show), watched (boolean), and other metadata fetched from the OMDB API like year, genre, director, actors, and IMDb rating. The schema was kept minimal to ensure fast read/write operations and make future migrations easier.

#### Form Validation and UX: Form inputs are validated both client-side (HTML required attributes) and server-side (checking for duplicates or invalid entries). JavaScript was used to enhance user experience through real-time search suggestions, improving speed and convenience when adding new titles.

#### How to Run Locally
1. Clone the repository:
    ```
    git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Set environment variable and run the app:
    ```
    export FLASK_APP=app.py  # on Windows use: set FLASK_APP=app.py
    flask run
    ```

5. Open your browser and go to http://127.0.0.1:5000

#### Future Improvements:
- User Authentication: Allow users to log in and save their watchlists to a personal and editable profile account.
- Rating System: Let users assign personal ratings or comments to movies/shows.
- Sorting & Filtering: Enable filtering by genre, year, and IMDb score.
- Better Placeholder Images: Improve visuals for entries with missing or invalid posters.
- Pagination: Add pagination for large lists to enhance performance and UX.
- Shows=>Seasons=>Episodes: Display seasons and episodes and track exactly what was watched.

### Conclusion: This project provided an opportunity to develop a full-stack application using HTML, CSS, JavaScript, Flask, Python, SQLite, and Bootstrap. From setting up the database schema to refining the UI and handling API integrations, each part was implemented with user experience in mind. Special attention was given to route structure and database interactions to ensure the app remains extensible and easy to maintain. The project is simple in concept but demonstrates how thoughtful design and lightweight tools can produce a functional, usefull, visually pleasing, and responsive app.
