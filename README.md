# SULearn - E-Learning Platform

[<img align="left" height=150 width=250 src="https://i.ytimg.com/vi/iOHq7BWFQRc/maxresdefault.jpg">](www.algoexpert.io)
<br> _So, you wanna be a backend developer at SUTT...xD._

You have to design an e-learning platform. This one's a bit challenging but you'll eventually learn a lot from developing this. <br><br><br>

### Users

This platform will have two types of users -

1. **Creators**
2. **Viewers**

Creators upload **courses**, which are divided into **modules**. Any viewer can enroll in these courses. The viewer takes the course module by module, **marking them as complete**. The course taken is completed only when all its modules have been marked as completed. Once the course is complete, the viewer will have the option to **rate and review** it.

On the home page, the courses would be displayed to the user, preferably under individuals sections by their **tags**. The user will also have the option to **search** for a course using keywords or using tags as filters.

Each user will have a **profile** page that will show the user's personal details, the courses enrolled - completed and ongoing, or in case of creators - the courses uploaded by them.

Each course will have a dedicated page where one can see the various modules, their creator, course rating, and reviews.

### Model Attributes

Each user will have a `uid`, `name`, `email`, `dob`, `city`, `state` and `date of joining platform`.
Creators should have additional fields such as `educational qualifications`, `rating`.

Courses - `creator`, `rating`, `reviews`, `modules`

Tags - such as computer science, marketing, business, personal development, etc.

### Authentication

Each user should be able to register/login via Google OAuth. You are free to use a package called [django-allauth](https://wsvincent.com/django-allauth-tutorial/). Upon Google Oauth, the user should be able to choose the account type - creator or viewer and should be asked to fill in their details. Register the user in the database only when you have the required details.

### Bonus Tasks

1. **Follow + Following** - A viewer can follow a creator for updates on his new courses. You can implement this by sending **email notifications** to the user using `SMTP` or `Sendgrid API`. It would be desirable to also add a section on the home page that would show the courses uploaded by the user's following.
2. **Digital proof of completion** - each viewer can share a link that will act as proof of completion. It can be in the form of a mock certificate that would feature the user, the course, and the date of completion.

### Deployment

The project should be deployed on a desirable platform such as Heroku, Pythonanywhere, AWS, Digital Ocean, etc.

### My Take

Don't be overwhelmed by the magnitude of the task, focus on the subtasks instead and finish them one by one. Be creative and feel free to assume the minor details as you like. We don't expect you to build a proper frontend for this task. You are free to use any public template or use any CSS framework such as Bulma or Bootstrap.

In case you are stuck on any subtask, please feel free to contact us, we would be happy to discuss your approach to direct you in the right direction.
