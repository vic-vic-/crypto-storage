
***Project Structure***

CryptoStorage diagram and workflow(as of 10/30/15):

The diagram below shows an explanation of how our project works. We have been over analyzing our project (only programming) but we came to the conclusion of putting our project more clearly on paper to actually look at the big picture. We will continue to update this document  to add/remove requirements, if necessary, and we will continue programming. 

Application Requirements:

 - HTTPS session only.

 - User names will be emails. 
 - Password hashes computed on the client side will be pbkdf2. The password:
 - Must be at least 10 characters.
 - Must contain at least 1 special character (e.g. !@#$)
 - Must contain at least 1 capital character.
 - Must contain at least 1 numeric digit.
 - User attempts only 3. If user attempts is greater than or equal to 3, then the user account will be marked as locked. You must call customer service.
 - Pbkdf2 will be used to generate the key and prevent dictionary attack on the password.
 - The salt + the password will be the input for pbkdf2
Run pbkdf2 many times to create the key

[Diagram](https://github.com/vic-vic-/crypto-storage/blob/master/docs/content/diagram.JPG)

