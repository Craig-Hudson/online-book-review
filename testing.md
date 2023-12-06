# Readers Realm Testing

## Table of contents

- [Readers Realm Testing](#readers-realm-testing)
  - [Table of contents](#table-of-contents)
  - [Overview](#overview)
  - [Automated Testing](#automated-testing)
    - [Lighthouse](#lighthouse)
    - [HTML validator](#html-validator)
    - [CSS validator](#css-validator)
    - [JavaScript Validator](#javascript-validator)
  - [wave reports](#wave-reports)
  - [Manual Testing](#manual-testing)
    - [Testing user Stories](#testing-user-stories)
    - [Full Testing](#full-testing)

## Overview

I used test driven development throughout the entire build for this project.
This includes using chrome developer tools to test for responsiveness and for general positioning of elements, I also used the dev tools and the terminal with the use of print statements in my python to help identify if there was any errors in the console and where the issues may of been arising from.


## Automated Testing

### Lighthouse

- Desktop Lighthouse report perfect scores all round!

![Desktop Lighthouse report](assets/images/testing-images/desktop-lighthouse.webp)

- Mobile lighthouse report 

![Mobile lighthouse report](assets/images/testing-images/mobile-lighthouse.webp)

### HTML validator

I have used the html validator [W3C HTML Validator](https://validator.w3.org/)
Initially many of my html files had either info's or warnings, which have all been corrected,
A couple of my html files had errors which have now also been fixed and are all clear of errors.
![HTML Validation](documentation/validation/html-validation.png)

### CSS validator

- My css has come back with no errors and no warnings.

![CSS Validation](documentation/validation/css-validation.png)

### JavaScript Validator

- Home page JavaScript validation on JShint

![JavaScript validation](documentation/validation/javascript-validation.png)

- As you can see if the above image it's coming back with two info's

- First one is about emailJS not being defined, I followed along the code institute tutorial for
  setting up emailJS and emailJS is initialized in my base.html file starting on line 11.
  
- Second is the function sendMail being unused, but this is called on line 7 in my contact.html page

## wave reports

- Home Page

![Home page](documentation/wave-reports/home-page-wave.png)

- Browse Books Page

![Browse Books Page](documentation/wave-reports/browse-books-wave.png)

- Contact page

![Contact Page](documentation/wave-reports/contact-page-wave.png)

- Login page

![Login Page](documentation/wave-reports/login-wave.png)

- Register page

![Register page](documentation/wave-reports/register-page-wave.png)

- Review Page
  
![Review page](documentation/wave-reports/review-page-wave.png)

- The pages above wave reports have zero errors and zero contrast errors, a few of them have alerts for possible headings and redundant link.

- The following pages below I was unable to get to use the wave report due to them being restricted pages
only for users who are logged in, but I have made sure anything that may be a contrast error has been
resolved, and making sure all the headings are there, and none are skipped.

- Add Book Page

- Edit Book page

- Add Review page

- Edit Review page

- Profile page

## Manual Testing

### Testing user Stories

- **First time Visitors**

|  Goals | How are they achieved?  |
| ------------ | ------------ |
|  |  |


- **Returning Visitor Goals**

| Goals  |  How are they achieved? |
| ------------ | ------------ |
|  |  |
​

- **Frequent visitor goals**

|  Goals | How are they achieved  |
| ------------ | ------------ |
|  |  |

### Full Testing

Testing was done on the following devices and browsers

- Devices
  - Lenovo Laptop 14inch screen
  - oppo xp lite (android)

- Browsers
  - Google chrome
  - Firefox

-**Index Page**

| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Browse Book Page**

| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Contact Page**

| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Login Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Register Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|

- **Error Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Add Book Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Edit Book Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Add Review Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Edit Review Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Review Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |

- **Profile Page**
  
| Feature  | Expected outcome  | Testing performed  | Result  | Pass/Fail  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
|  |  |  |  |  |