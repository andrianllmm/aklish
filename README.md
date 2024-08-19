# Aklish

**A Django x React.js web application for crowdsourcing Aklanon-English translations.**


<div align="center">
   <img src="demo/mockups/demo.png" alt="demo" width="500"/>
   <br>
   <a href="https://aklish.up.railway.app" >
      <strong>↗ Demo</strong>
   </a>
</div>


## About

[Aklish](https://aklish.up.railway.app) is a web application designed to facilitate the crowdsourcing of Aklanon-English translations. It offers a collaborative platform where users can contribute and manage translations between Aklanon and English. The app focuses on community engagement and high-quality results by employing several key strategies.

Key [features](#features) of Aklish include a community voting system for evaluation, an Aklanon-English dictionary for reference, proofreaders to ensure entry quality, and a points system similar to [StackOverflow’s](https://stackoverflow.com/help/whats-reputation) to enhance accountability. To boost user participation, Aklish includes leaderboards and interactive games, such as a [Wordle](https://www.nytimes.com/games/wordle/index.html) clone and synonym-antonym matching.

By supporting the Aklanon language’s preservation and enrichment, Aklish provides valuable resources for both linguistic enthusiasts and everyday users.



## Features

1. Bidirectional Input of Entries
2. Multiple Translations for a Single Entry
3. Browse Entries
4. Search Entries
5. Authentication
6. Quality Control Strategies
   - Voting System
   - Aklanon-English Dictionary
   - Aklanon and English Proofreader
   - Points System
7. Engagement Strategies
   - Leaderboard System
   - Games


## Installation

To set up Aklish locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/andrianllmm/aklish.git
   cd aklish
   ```

2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # or `env\Scripts\activate` for Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```


## Configuration

Before running the application, ensure that you have configured the following settings in your .env file:

- `DATABASE_URL`: URL for the database connection.
- `SECRET_KEY`: A secret key for Django security purposes.
- `DEBUG`: Set to True for development, False for production.


## Usage

1. **Register an account**: Since some features can only be accessed by authenticated users, sign up to create a new account or sign in if you already have one.
3. **Earn reputation**: Some features can only be accessed by earning enough reputation points.
2. **Participate**: To earn reputation, submit entries or translations, bookmark, vote, etc.
4. **Learn more**: View the help center at `/help` for more information.


## Contributing

Contributions are welcomed! To get started:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Make your changes.
4. Submit a pull request with a clear description of your changes.


## Issues

If you encounter any issues or bugs, please report them on the [GitHub issues page](https://github.com/andrianllmm/aklish/issues).


## License

This project is licensed under the [GPL-3.0 License](LICENSE).

---

For more information contact [maagmaandrian@gmail.com](mailto:maagmaandrian@gmail.com) with any additional questions or comments.