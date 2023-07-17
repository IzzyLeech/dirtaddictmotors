# Dirt Addict Motors

# Goal for this Project

# UX

## User Stories

### Epic | Website Function

### Epic
### Epic
### Epic
### Epic

## User Requirements and Expectations

### Requirements

### Expectations

## Wireframes

### [Mobile Wireframe]

### [Tablet Wireframe]

### [Desktop Wireframe]

## Design Choices
### Fonts

### Colours

### Images

## Structure

### Modal Diagram

### Models Info

## App Flow

### Non Register-User

### Authenticated-User

### Admin

# Features

## Existing Features

## Features to be Implemented

# Tools and Technologies used

# Testing

## Code Validation

### HTML

I have used the [HTML W3C Validator](https://validator.w3.org) to validate all of my HTML files.

As my project uses Jinja syntax, such as `{% for loops %}`, `{% url 'home' %}`, and `{{ variable|filter }}`
it will not validate properly if I copy and paste into the HTML validator straight from my source files.

In order to properly validate my HTML pages with Jinja syntax for authenticated pages, I followed these steps:

- Navigate to the deployed pages which require authentication
- Right-click anywhere on the page, and select **View Page Source**.
- This will display the entire "compiled" code, without any Jinja syntax.
- Copy everything, and use the [validate by input](https://validator.w3.org/#validate_by_input) method.
- Repeat this process for every page that requires a user to be logged-in/authenticated.

| Page | Screenshot | Notes |
| --- | --- | --- |
| Home | 


### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate my CSS file.

### Javascript

I have used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files.

### Python

I have used the recommended [CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool to check for any major issues.

## Defensive Programming

Defensive programming was manually tested with the below user acceptance testing:

## User Story Testing

The following are user stories I've implemented with screenshots to prove