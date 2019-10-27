# Assurances

In accordance with the user stories, our implementation of the backend lines up clearly to meet the needs of the users. The assurances have been split between the different epics.

## Epic 1 Assurances
If a valid email, password and name are given, the user can create an account, with an assigned handle and can login/logout as they please. Once they register, they will automatically be logged in to join or create channels are they please.
If they logout, the implementation is safe enough to prevent other users from pretending to be the user and steal any information.
If the password is forgotten, an email will be sent to their registered email and be given a code to reset their password. If this reset code is returned, then the user will be able to create a new password and be logged in again.

## Epic 2 Assurances

## Epic 3 Assurances

## Epic 4 Assurances 

These aspects were tested using both manual testing, trying all different aspects and trying to break the code ensuring for appropriate exceptions to be raised and by also considered branch coverage and linting.

Users can then create channels that they are either a owner, admin or member of (providing different permissions). If a channel is public people can both join and be invited to, while if a channel is private, people can only be invited into one, and cannot join without and invite.
