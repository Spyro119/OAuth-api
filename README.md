<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Spyro119/OAuth-api">
    <img src="docs/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">OAuth-api</h3>

  <p align="center">
    Rest API for user management.
    <br />
    <a href="#"><strong>Explore documentation »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Spyro119/OAuth-api/issues">Report Bug</a>
    ·
    <a href="https://github.com/Spyro119/OAuth-api/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contribute">Contribute</a></li>
    <li><a href="#versions">Versions</a></li>
    <li><a href="#publis">Publis</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#ressources">Ressources</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About the project

[![Product Name Screen Shot][product-screenshot]](docs/screenshot_2.png)


<!-- API de gestion d'utilisateurs, groupes, permissions et tokens. -->
Simple Rest API to manage users account, authentification and authorizations.

<!-- There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template! -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- BUILT WITH -->
### Built with

* [![Python-shield]][Python-url]
* [![FastAPI-shield]][FastAPI-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting started

### Prerequisites

- python 3.11+
- pipenv
- postgreSQL
- docker
  

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Spyro119/OAuth-api/
   ```
2. Install dependencies with pipenv
    ```sh
    python -m pipenv install
    ```
3. rename ``.env.template`` file for ``.env`` and update values:
    ```sh
    POSTGRES_USER=<username>
    POSTGRES_PASSWORD=<password>
    POSTGRES_SERVER=<host>
    POSTGRES_PORT=<port>
    POSTGRES_DB=<db_name>
    JWT_SECRET_KEY=<secret_key>
    JWT_REFRESH_SECRET_KEY=<secret_key>

    # Docker vars
    PGDATA=<Docker Data path>
    PG_CONTAINER_NAME=<Docker db container name>
    ```
4. Run the app 
    ```sh
    python -m pipenv shell # Ouvre une nouvelle instance de terminal dans l'environnement du projet.
    uvicorn app.main:app --reload 
    ```

5. Log in as admin and create your new admin account.
    - Credentials are - username: ``admin`` password: ``password123!``.
    - IMPORTANT: It is recommended to delete this account after creating your own admin account.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Project initialisation.
- [x] Database initialised.
- [x] Endpoints defined.
- [ ] Unit testing integration. (Partially done).
- [ ] Document the project.

See the [open issues](https://github.com/Spyro119/OAuth-api/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTE -->
## Contribute

1. Clone the repo `git clone `
2. Create a new "Feature" branch (`git checkout -b feature/{FeatureName}`)
3. Commit changes (`git commit -m 'Problème x Résolu'`)
4. Push to your own branch (`git push origin feature/{FeatureName}`)
5. Create a Pull Request 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Versions -->
## Versions

* [1.0.0](https://github.com/Spyro119/OAuth-api/tags)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- PUBLISH -->
## Publish

To host the API, simply run it under docker: 
```sh
docker compose up -d --build 
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Samuel Jubinville-Baril - [github](https://github.com/Spyro119) - jubinvilles@outlook.com

<!-- Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com -->

Project Link: [https://github.com/Spyro119/OAuth-api](https://github.com/Spyro119/OAuth-api)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Ressources -->
## Ressources

* [README Template](https://github.com/othneildrew/Best-README-Template)
* [FastAPI](https://fastapi.tiangolo.com/)
* [FastAPI OAUTH2](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)
* [pipenv Documentation et installation](https://pipenv.pypa.io/en/latest/)
* [pipenv guide](https://realpython.com/pipenv-guide/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- GITHUB URLS -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/VIP.svg?style=for-the-badge
[contributors-url]: https://github.com/Spyro119/OAuth-api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/VIP.svg?style=for-the-badge
[forks-url]: https://github.com/Spyro119/OAuth-api/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/VIP.svg?style=for-the-badge
[stars-url]: https://github.com/Spyro119/OAuth-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/VIP.svg?style=for-the-badge
[issues-url]: https://github.com/Spyro119/OAuth-api/issues
[license-shield]: https://img.shields.io/github/license/Spyro119/OAuth-api.svg?style=for-the-badge
[license-url]: https://github.com/Spyro119/OAuth-api/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/samuel-jubinville-baril-bbb5601a4/
[product-name]: Oauth-api
[product-screenshot]: docs/screenshot_2.png
[Product-name-screenshot]: Oauth-api


<!-- FRAMEWORK AND LIBRARY URLS -->
[Python-shield]: https://img.shields.io/pypi/pyversions/FastAPI?logo=python
[Python-url]: (https://www.python.org/)
[FastAPI-shield]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[Vue-shield]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/