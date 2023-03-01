//@author Liquad Li
//@description find all users that associated with given profiles, then re-assign them to another profile.
List<String> profileIdsToUnassign = new List<String>{ '<profile_current>',
          '<profile_current2>'};

List<User> usersToUpdate = [SELECT Id, ProfileId,Profile.Name FROM User WHERE Profile.Name IN :profileIdsToUnassign];

for (User u : usersToUpdate) {
    u.ProfileId = '00exxxxxxxxxx';//The profile want to change to.
}

update usersToUpdate;
