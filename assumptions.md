# Assumptions

## General assumptions:
* Assume that in every test, the state of the slackr server is reset. This means that new users, new channels, etc have to be created in every test function.
* All functions called in testing are implemented correctly.
* All details of users are stored correctly.
* A valid email is of the form [personal_data]@[domain], so, for example, goodemail@gmail.com would be valid, whereas a bad email such as bademail_gmail.com would be invalid.
* Owner permission_id = 1, admin permission_id = 2, member permission_id = 3. Any other permission_id is invalid.
* Assume owners and admins have the same special permissions, however, admins have special permissions over every channel, whereas owners just have permissions over specific channels.
* Messages must have less than 1000 characters inclusive. So a message with 1000 characters is permitted, but 1001 and above is not.

## Assumptions about variables:
* When a user logs in or creates an account, a unique token and u_id is created for them that no other user shares.
* For functions that require a token, the token is assumed to be valid.
* Assume that for ValueErrors where data does not refer to valid data, the invalid data is of the same type as the valid data. So for example, an invalid u_id would also be of type integer, and a string in place of u_id would never happen.
* Assume that any variable with time_ is only stored up to the second. So it stores year, month, day, hour, minute, second, but anything smaller than a second, such as milliseconds, microseconds etc are not stored.

## Function-specific assumptions:
channel_create, channel_addowner
* When a channel is created, the user that created that channel is automatically made the owner of the channel.
* A member must be part of a channel to be made the owner of the channel.

admin_userpermission_change, channel_addowner
* admin_userpermission_change and channel_addowner can theoretically achieve the same thing - changing a user’s permissions to be an owner of a channel. However, channel_addowner only makes the user an owner of a specific channel, whereas admin_userpermission_change makes the user an owner of all currently existing channels.
* The difference in permissions between someone made owner through the admin_userpermission_change method and being made admin is that an admin is automatically given special permissions over any new channel that is created, however, a user with owner permissions has to be added as an owner any time a new channel is created.

user_profiles_uploadphoto
* In this current iteration, the HTTP value returned is not tested. This is because there is no function currently available to do so.
* Likewise, testing whether the crop bounds are outside the maximum image dimensions is also not tested, for similar reasons.
* The current ValueErrors for crop bounds are assumed to be a mistake in the specifications. Currently, they make no sense - x_start, y_start, x_end, and y_end are all within the dimensions of the image is not at all a cause for an error. Instead, tests for alternative ValueErrors have been implemented:
* If any of the bounds are negative, this should produce a ValueError.
* If x_start > x_end or y_start > y_end, this should also produce a ValueError.

standup_start, standup_send, message_send, message_sendlater
* Assume that standup_send can only be called after standup_start.
* Assume message_send cannot be called while a standup is occurring. The only standup_send can be called. message_sendlater can be called only if the time specified is after the standup has finished.
* Whilst calling standup_send after the standup has finished is an AccessError, currently there is no way to test that (without waiting for 15 mins), as there is currently no way to change the length of a standup or access the time_created of messages sent in a standup. Thus, it will be implemented later.

message_remove, message_edit
* Assume in terms of AccessError in message_remove and message_edit, “message with message_id edited by authorised user is not the poster of the message” is the same as “Message with message_id was not sent by the authorised user making this request”.
* Assume that there is a limited amount of reactions you can give to a message, i.e. in message_react and message_unreact, assume there are only 4 reactions you can make(thumb up, thumb down, happy and angry) and other than these 4 reactions are invalid reaction_ids.

channels_list, channels_listall
* To differentiate between channels_list and channels_listall, channels_list will **only** list channels the user is part of, whereas channels_listall will list functions the user is part of **in addition** to all public channels available (regardless of membership).
