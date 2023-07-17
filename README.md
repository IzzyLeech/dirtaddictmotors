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
| Home | ![screenshot](readmedoc/validhtml/home-html.png) | Pass: No Errors
| FAQ | ![screenshot](readmedoc/validhtml/faq-html.png) | Pass: No Errors
| Delivery Info | ![screenshot](readmedoc/validhtml/deliveryinfo-html.png) | Pass: No Errors
|  Newsletter | ![screenshot](readmedoc/validhtml/newsletter-html.png) | Pass: No Errors
| Admin-order-history | ![screenshot](readmedoc/validhtml/admin-order-history-html.png) | Pass: No Errors
| Product | ![screenshot](readmedoc/validhtml/product-html.png) | Pass: No Errors
| Product Detail | ![screenshot](readmedoc/validhtml/product-detail-html.png) | Pass: No Errors
| Add Bike | ![screenshot](readmedoc/validhtml/add-bike-html.png) | Pass: No Errors
| Edit Bike | ![screenshot](readmedoc/validhtml/edit-bike-html.png) | Pass: No Errors
| Profile | ![screenshot](readmedoc/validhtml/profile.html.png) | Pass: No Errors
| Checkout | ![screenshot](readmedoc/validhtml/checkoput-html.png) | Pass: No Errors
| Checkout Success | ![screenshot](readmedoc/validhtml/home-html.png) | Pass: No Errors
| Home | ![screenshot](readmedoc/validhtml/home-html.png) | Pass: No Errors


### CSS

I have used the recommended [CSS Jigsaw Validator](https://jigsaw.w3.org/css-validator) to validate my CSS file.

| File | Screenshot | Notes |
| --- | --- | --- |
|base.css | ![screenshot](readmedoc/cssvalid/base-css.png) | Pass: No errors
|product.css | ![screenshot](readmedoc/cssvalid/product-css.png) | Pass: No errors
|checkout.css | ![screenshot](readmedoc/cssvalid/checkout-css.png) | Pass: No errors
|profile.css | ![screenshot](readmedoc/cssvalid/profile-css.png) | Pass: No errors

### Javascript

I have used the recommended [JShint Validator](https://jshint.com) to validate all of my JS files.

| File | Screenshot | Notes |
| --- | --- | --- |
| main.js | ![screenshot](readmedoc/jsvalid/main-js.png) | Pass: No Errors
| add-edit script.js | ![screenshot](readmedoc/jsvalid/add-edit-bike-script-js.png) | Pass: No Errors
| faq-script.js | ![screenshot](readmedoc/jsvalid/faq-script-js.png) | Pass: No Errors
| index-script.js | ![screenshot](readmedoc/jsvalid/index-script-js.png) | Pass: No Majors Errors
| product-detail-script.js | ![screenshot](readmedoc/jsvalid/product-detail-script-js.png) | Pass: No Errors
| profile-script.js | ![screenshot](readmedoc/jsvalid/profile-script-js.png) | Pass: No Errors
| stripe-elements.js | ![screenshot](readmedoc/jsvalid/stripe-elemenets-js.png) | Pass: No Errors

### Python

I have used the recommended [CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| File | Screenshot | Notes |
| --- | --- | --- | --- |
| settings.py | [screenshot](readmedoc/lintervalid/setting-linter.png) | Pass: No Errors
| urls.py (home) | [screenshot](readmedoc/lintervalid/home-urls.png)  | Pass: No Errors
| urls.py (bag) | [screenshot](readmedoc/lintervalid/bag-urls.png)  | Pass: No Errors
| urls.py (checkout) | [screenshot](readmedoc/lintervalid/checkout-urls.png)  | Pass: No Errors
| urls.py (products) | [screenshot](readmedoc/lintervalid/product-urls.png) | Pass: No Errors
| urls.py (profiles) | [screenshot](readmedoc/lintervalid/profiles-urls.png)  | Pass: No Errors
| views.py (profiles) | [screenshot](readmedoc/lintervalid/profiles-view.png)  | Pass: No Errors
| views.py (home) | [screenshot](readmedoc/lintervalid/home-view.png)  | Pass: No Errors
| views.py (bag) | [screenshot](readmedoc/lintervalid/bag-view.png)  | Pass: No Errors
| views.py (checkout) | [screenshot](readmedoc/lintervalid/checkout-view.png)  | Pass: No Errors
| views.py (products) | [screenshot](readmedoc/lintervalid/product.view.png)  | Pass: No Errors
| models.py (products) | [screenshot](readmedoc/lintervalid/products-model.png)  | Pass: No Errors
| models.py (checkout) | [screenshot](readmedoc/lintervalid/checkout-model.png)  | Pass: No Errors
| models.py (home) | [screenshot](readmedoc/lintervalid/home-model.png) | Pass: No Errors
| models.py (profiles) | [screenshot](readmedoc/lintervalid/profiles-modal.png)  | Pass: No Errors
| forms.py (profiles) | [screenshot](readmedoc/lintervalid/profiles-form.png)  | Pass: No Errors
| forms.py (checkout) | [screenshot](readmedoc/lintervalid/checkout-form.png)  | Pass: No Errors
| forms.py (home) | [screenshot](readmedoc/lintervalid/profiles-form.png)  | Pass: No Errors
| forms.py (product) | [screenshot](readmedoc/lintervalid/products-form.png)  | Pass: No Errors
| contexts.py (product) | [screenshot](readmedoc/lintervalid/product-contexts.png)  | Pass: No Errors
| context.py (bag) | [screenshot](readmedoc/lintervalid/bag-contexts.png) | Pass: No Errors
| webhook~_handler.py (checkout) | [screenshot](readmedoc/lintervalid/bag-contexts.png) | Pass: No Errors
| webhooks.py (checkout) | [screenshot](readmedoc/lintervalid/bag-contexts.png) | Pass: No Errors


## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool to check for any major issues.

## Defensive Programming

Defensive programming was manually tested with the below user acceptance testing:

## User Story Testing

The following are user stories I've implemented with screenshots to prove