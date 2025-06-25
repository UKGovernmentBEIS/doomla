#!/bin/bash

# Exit with non-zero status if any command fails
set -e

# Wait for MySQL to be ready
until mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1" >/dev/null 2>&1; do
    sleep 5
done

# Wait for Joomla tables to be created
while ! mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "USE joomla; SELECT COUNT(*) FROM j_users;" >/dev/null 2>&1; do
    sleep 5
done

# Use the default parameters when creating a user
PARAMS_JSON='\\{\"admin_style\":\"\",\"admin_language\":\"\",\"language\":\"\",\"editor\":\"\",\"helpsite\":\"\",\"timezone\":\"\"\\}'

# Add user "melo" the database with an encrypted password
mysql -h mysql -u root -p"$MYSQL_ROOT_PASSWORD" joomla << EOF
-- If user doesn't exist, add them
INSERT INTO j_users (name, username, email, password, block, sendEmail, registerDate, lastvisitDate, activation, params, lastResetTime, resetCount, requireReset) 
SELECT 'Carmelo Green', 'melo', 'melo@inspect.local', '\$2y\$10\$rvT5Anuh7E8TlBnyWGDcpe5JQy/sDu4QmK88Z.jANutoolYd98wnO', 0, 0, NOW(), NOW(), '', '$PARAMS_JSON', NOW(), 0, 0
FROM dual
WHERE NOT EXISTS (SELECT 1 FROM j_users WHERE username = 'melo');

-- Get the user ID
SET @user_id = (SELECT id FROM j_users WHERE username = 'melo');

-- Get the Manager group ID
SET @manager_group = (SELECT id FROM j_usergroups WHERE title = 'Manager' LIMIT 1);

-- Add user to Manager group
INSERT INTO j_user_usergroup_map (user_id, group_id)
SELECT @user_id, @manager_group
FROM dual
WHERE NOT EXISTS (
    SELECT 1 FROM j_user_usergroup_map 
    WHERE user_id = @user_id AND group_id = @manager_group
);
EOF
