I accordance with the user stories, our implementation of the backend lines up clearly to meet the needs of the users.
If a valid email, password and name are given, the user can create an account, with an assigned handle and can login/logout as they please. Once they register, they will automatically be logged in to join or create channels are they please.
If they logout, the implementation is safe enough to prevent other users from pretending to be the user and steal any information.
If the password is forgotten, an email will be sent to their registerd email and be given a code to reset their password. If this reset code is returned, then the user will be able to create a new password and be logged in again.
