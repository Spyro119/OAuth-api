<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Spyro119/OAuth-api">
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

  <h3 align="center">OAuth-api</h3>

  <p align="center">
    API pour gérer l'authentification des utilisateurs.
    <br />
    <a href="https://prod-api-website.com/docs"><strong>Explorer la documentation »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Spyro119/OAuth-apiVIP/issues">Report Bug</a>
    ·
    <a href="https://github.com/Spyro119/OAuth-apiVIP/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE DES MATIÈRES -->
<details>
  <summary>Table des matières</summary>
  <ol>
    <li>
      <a href="#à-propos-du-projet">À propos du projet</a>
      <ul>
        <li><a href="#fabriqué-avec">Fabriqué avec</a></li>
      </ul>
    </li>
    <li>
      <a href="#Pour-commencer">Pour commencer</a>
      <ul>
        <li><a href="#Pré-requis">Pré-requis</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#utilisation">Utilisation</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contribuer">Contribuer</a></li>
    <li><a href="#versions">Versions</a></li>
    <li><a href="#publier">Publier</a></li>
    <!-- <li><a href="#contact">Contact</a></li> -->
    <li><a href="#ressources">Ressources</a></li>
  </ol>
</details>



<!-- À PROPOS DU PROJET -->
## À propos du projet

[![Product Name Screen Shot][product-screenshot]](https://example.com) <!-- TODO -->

<!-- API de gestion d'utilisateurs, groupes, permissions et tokens. -->
API pour gérer l'authentification ainsi que les authorisations des utilisateurs.

<!-- There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should implement DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have contributed to expanding this template! -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- FABRIQUÉ AVEC -->
### Fabriqué avec

* [![Python-shield]][Python-url]
* [![FastAPI-shield]][FastAPI-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- POUR COMMENCER -->
## Pour commencer

### Pré-requis

- python 3.11+
- pipenv
    <!-- ```sh 
    pip install pipenv 
    ``` -->
- postgreSQL
- docker
  

### Installation

1. Clone le repo
   ```sh
   git clone https://github.com/Spyro119/OAuth-apiSegidocOAuthAPI/
   ```
2. Installer les dépendances de l'environnement avec pipenv
    ```sh
    python -m pipenv install
    ```
3. Renommer le fichier ``.env.template`` pour ``.env`` et changer les valeurs :
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
<!-- 4. alembic init alembic -->
4. Exécuter l'application
    ```sh
    python -m pipenv shell # Ouvre une nouvelle instance de terminal dans l'environnement du projet.
    uvicorn app.main:app --reload 
    ```

5. Créer un nouvel admin et supprimé l'admin généré par alembic.
    - pour se connecter, le nom d'utilisateur est ``admin`` et le mot de passe est ``password123!``.
    - IMPORTANT: veuillez supprimer ce compte après avoir créer un premier compte admin.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- UTILISATION -->
## Utilisation

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Initialiser le projet.
- [x] Créer la DB `SegidocAuth`.
- [x] Définir les endpoints.
- [x] Intégrer un mail service.
- [ ] Intégrer l'unit testing pour assurer le bon fonctionnement de l'API. (Partiellement fait).
- [ ] Documenter le projet.

See the [open issues](https://github.com/Spyro119/OAuth-apiSegidocOAuthAPI/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUER -->
## Contribuer

1. Cloner le repo `git clone `
2. Créer une nouvelle branche "Feature" (`git checkout -b feature/{FeatureName}`)
3. Commit les Changement (`git commit -m 'Problème x Résolu'`)
4. Push à la branche (`git push origin feature/{FeatureName}`)
5. Ouvrir une Pull Request 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Versions -->
## Versions

* [1.0.0](https://github.com/Spyro119/OAuth-apiSegidocOAuthAPI/tags)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- PUBLIER -->
## Publier

build le projet: 
```sh
docker compose up -d --build 
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
<!-- ## Contact -->

<!-- Samuel Jubinville-Baril - [github](https://github.com/jubinvilles) - samuel.jubinville@tactgroup.com -->

<!-- Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/Spyro119/OAuth-apirepo_name](https://github.com/Spyro119/OAuth-apirepo_name) -->

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



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
[contributors-url]: https://github.com/Spyro119/OAuth-apiSegidocOAuthAPI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/VIP.svg?style=for-the-badge
[forks-url]: https://github.com/Spyro119/OAuth-apiSegidocOAuthAPI/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/VIP.svg?style=for-the-badge
[stars-url]: https://github.com/Spyro119/OAuth-apiSegidocOAuthAPI/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/VIP.svg?style=for-the-badge
[issues-url]: https://github.com/Spyro119/OAuth-apiSegidocOAuthAPI/issues

<!-- FRAMEWORK AND LIBRARY URLS -->
[Python-shield]: https://img.shields.io/pypi/pyversions/FastAPI?logo=python
[Python-url]: (https://www.python.org/)
[FastAPI-shield]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[Vue-shield]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/