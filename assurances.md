# Assurances

In accordance with the user stories, our implementation of the backend lines up clearly to meet the needs of the users. The assurances have been split between the different epics.

## Epic 1 Assurances
The following were tested by creating two different users. This was done by using the tests from the previous iteration and adding code to run on the Postman API. The first user logged out, and the second tried to login as the first user using their details. However, the second was not able to, as the token ensured that the first user's login details were protected. The password reset also functioned correctly.
* As a new user to Slackr, I would like to be able to register with my email and set my own password, so that I can log in at any time and
anywhere with the account that I have created.
* As a user of the Slackr, I would like to be able to log out of my account, so that if I have logged in a public device, I could sign out and protect my personal information.
* As a user of the Slackr, I would like to be able to reset my password through the email I registered with, so that if I accidentally forget my
old password, I can still get my access for the same account back using my email.

## Epic 2 Assurances
The following were tested by creating channels and two users with different permissions. Through testing on the Postman API, the user with the correct permissions was able to see and access the private channel, but the user without those permissions was not. Both members were able to see public channels.
* As a user of the Slackr, I would like to create public channels, so that I can get people interested in the same topic to join and I can see
other people’s opinions and make more friends at the same time.
* As a user of the Slackr, I would like to be able to create private channels, so that I can share things with only the people I know.
* As a user of the Slackr, I would love to have the ability to search for all the existing channels, so that I can always check if there are new channels I am interested in and join it.
* As a user of the Slackr, I would like to be able to see all the channels I have already joined, so that I can get a clear image of how many channels I have joined or if I want to get rid of some.

Following from the previous testing, the user with permission changed the permission of the other user and added them to the private channel. Thus, these user stories were also able to be fulfilled.
* As a user of the Slackr, I would love to be able to invite people to my channels, so that I can create special discussion groups at any time I want.
* As a user of the Slackr, I would like to have the ability to leave channels, so that if I do not like the channel or I do not belong to the
group of people in that specific channel anymore.
* As an owner of a channel in Slackr, I would like to be able to modify a member's privilege, so that I can manage and organize my channel more
efficiently.
* As an admin of Slackr, I would like to be able to make another person an admin as well, so that I can ask other people to help me manage
and organize Slackr application better.

## Epic 3 Assurances
* As a member of a channel in Slackr, I would like to be able to send messages, so that people in the channel can communicate with each other by sending messages.
* As a member of a channel in Slackr, I would like to be able to pin and unpin a message, so that I can mark the messages that I’m interested or I think it’s important, and also that I can unpin it when I don’t need the message anymore.
* As a member of a channel of Slackr, I would like to be able to react and unreact to messages, so that I can express my emotion and opinion on a certain message faster and more straight forward, and if I don’t want my emotions and opinions to be seen, I can unreact the message I reacted to.

## Epic 4 Assurances

These aspects were tested using both manual testing, trying all different aspects and trying to break the code ensuring for appropriate exceptions to be raised and by also considered branch coverage and linting.

Users can then create channels that they are either a owner, admin or member of (providing different permissions). If a channel is public people can both join and be invited to, while if a channel is private, people can only be invited into one, and cannot join without and invite.
