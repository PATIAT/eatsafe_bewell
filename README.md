<h2 align="center"><img src=""></h2>

# Eat Safe - Be Well, a website designed to record and document food safety and quality incidents experienced by consumers.

## Milestone Project 3 - Backend Development

<h2 align="center"><img src=""></h2>

* Eat Safe - Be well is a website which allows consumers of everyday food items to report, record and document food safety and quality incidents. Incidents may relate to the safety or quality of food including food borne illnesses, the discovery of foreign object or allergic reactions. The website is designed to be fully responsive so that it can be used on any device.

* This is my Milestone Project 3 submission for Code Institute's Diploma in Web Application Development course. My website uses non-relational databases, features full CRUD functionality and is built using technologies that I have learnt including HTML, CSS, JavaScript, Python, Flask and MongoDB.

## Live Project

[View the live project here.](https://eatsafe-bewell.herokuapp.com/get_reports)

## Repository

[Find the project repository here.](https://github.com/PATIAT/eatsafe_bewell)

# Table of Contents

## Contents
- [User experience](#user-experience)
  * [User Stories](#user-stories)
    + [First-time Users](#first-time-users)
    + [Returning Users](#returning-users)
    + [Business Owner](#business-owner)
- [Design](#design)
  + [Overview](#overview)
  + [Colour Scheme](#colour-scheme)
  + [Typography](#typography)
  + [Imagery and Aesthetics](#imagery-and-aesthetics)
  + [Icons](#icons)
  + [Cards](#cards)
- [Wireframes](#wireframes)
- [Features](#features)
  + [Site Wide Page Features](#site-wide-page-features)
  + [Landing Page (Index) Features](#landing-page-index-features)
  + [Register and Log In Page Features](#-register-log-in-page-features)
  + [Find Report Page Features](#find-report-page-features)
  + [View Report Page Features](#view-report-page-features)
  + [My Reports (Dashboard) Page Features](#my-reports-dashboard-page-features)
  + [Submit and Edit Reports Page Features](#submit-edit-report-page-features)
  + [Favourite Reports Page Features](#favourite-reports-page-features)
  + [Manage Categories Page Features](#manage-categories-page-features)
  + [Add and Edit Categories Pages Features](#add-edit-categories-pages-features)
  + [Delete Report and Categories Pages Features](#delete-report-categories-pages-features)
  + [Error Handling](#error-handling)
- [Future Features](#future-features)
  + [User Experience Features](#user-experience-features)
  + [Development Features](#development-features)
- [Data Model](#data-model)
- [Technologies used](#technologies-used)
  + [Languages Used](#languages-used)
  + [Frameworks Libraries and Programs](#frameworks-libraries-and-programs)
- [Testing](#testing)
- [Deployment](#deployment)
  + [Creating a Gitpod Workspace](#creating-a-gitpod-workspace)
  + [GitHub Pages](#github-pages)
  + [Forking the GitHub Repository](#forking-the-github-repository)
  + [Making a Local Clone](#making-a-local-clone)
  + [Creating an application with Heroku](#creating-an-application-with-heroku)
- [Credits](#credits)
  + [Code](#code)
  + [Media](#media)
  + [Content](#content)
  + [Acknowledgements](#acknowledgements)

# User Experience

## User stoires

### First-time Users

*The website users that fall into this category are considering reporting a food safety incident online for the first time.* 

* As a first-time user, I want the landing page of the website to clearly explain the purpose of the website .

* As a first-time user, I want to be able to easily register for an account.

* As a first-time user, I want the website to work on any device.

### Returning Users

*The website users that fall into this category are have previously reported a food safety incident online.* 

* As a returning user, I want to be able to log in to my account.

* As a returning user, I want to be able to create / view / edit / delete my own food safety incident reports.

* As a returning user, I want to be able to view other user’s food safety incident reports.

* As a returning user, I want there to be valid corrective actions that I am able to take based upon my food safety incident report. This may include links to reporting mechanisms which alert potentially unsafe foods to the relevant authorities.

* As a returning user, I want to be able to search for food safety incident reports, to make it quicker to find incidents with a certain word in their name or description.

* As a returning user, I want to be able to access and use the website on any device.

### Buisness Owner

* As the website owner, I want users to be able to create, edit and delete their own reports, but not those of any other users.

* As the website owner, I want the adding, editing and deletion of any of the food safety incident categories to be restricted to users with admin privileges.

* As the business owner, I want it to be as easy as possible for users to submit food safety incident reports. E.g. a simple and quick process while gathering enough meaningful information to be useful to other users.

* As the business owner, I want the website to be effective and look consistently good on any device.

## Design

### Overview

- The website design is professional, yet attractive. The name Eat Safe - Be Well refers to the importance of food safety and food quality. These two food attributes should be a prerequisite for all food that is on sale to consumers. Where this is not found to be the case, a mechanism must exist where consumers can report any such issues, thereby alerting fellow consumers and relevant authorities to potentially unsafe food.

### Colour
<h2 align="left"><img src="static/readme/images/colour-scheme.jpeg" width="600"></h2>

- Eat Safe – Be Well uses a simple colour scheme of pale greens, browns, beiges and whites. The background is white with the nav and footer background being green which contrast well and keep these elements distinguishable from other elements on the page. 

### Typography

- Brand Logos and Headings are in Alegreya with a serif fallback font. This was used as sparingly as possible to maintain maximum impact. The body is in Roboto which is one of the most popular google fonts with sans-serif as a fallback font. Using Roboto means that the text will be easy to read on all device sizes.

### Images

- Images have been used sparingly on the website as the concept of the website does not necessarily lend itself to images. There is a banner image on the home page which is used to give the user an idea of what the website is about.

Photo by Viktoria Slowikowska: https://www.pexels.com/photo/fresh-vegetables-on-the-table-5677717/

### Icons

- Icons from Fontawesome have been used on the website's forms and on some of the buttons to emphasise the purpose of these elements.

### Materialize CSS Cards

- I decided to use cards as a way to display the user reports as it offers a clean and concise way to display the data submitted by the user. The cards are reveal cards which allow the user to click to reveal more information, this offers a good solution to prevent the cards from becomming cluttered.

# Wireframes

- [View my wireframes in PDF form here](https://github.com/PATIAT/eatsafe_bewell/blob/main/static/readme/wireframes/eat-safe-be-well-wireframes.png).
