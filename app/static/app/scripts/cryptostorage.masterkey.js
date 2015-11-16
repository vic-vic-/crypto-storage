// This is the main function to generate the hash for your password

// generates the hash password on the client side using PBKDF2 SHA-256

function generatePWHash(password, salt)
{
    // we perform 5000 iterations of a 
    // key size of 256 bits. Note the keysize is 256 /32 since we need to account
    // for the hexadecimal representation which account for 2 hex values per character.
    // This function is per crypto.js
    var hashedPassword = CryptoJS.PBKDF2(password, salt, { keySize: 256 / 32, iterations: 5000 });
    // displays on page for testing purposes
    document.getElementById("displayhash").innerHTML = hashedPassword;

    return hashedPassword;
}

