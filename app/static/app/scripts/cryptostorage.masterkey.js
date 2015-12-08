// This is the main function to generate the hash for your password
// generates the hash password on the client side using PBKDF2 SHA-256
// with the server's 128 random salt

// implementation of crypto.js library for hashing user password
function generatePWHash(password, salt)
{
    // we perform 5000 iterations of a 
    // key size of 256 bits. Note the keysize is 256 /32 since we need to account
    // for the hexadecimal representation which account for 2 hex values per character.
    // This function is per crypto.js
    var hashedPassword = CryptoJS.PBKDF2(password, salt, { keySize: 256 / 32, iterations: 5000 });
    // passes to page
    document.getElementById("hash").value = hashedPassword;
    
    return hashedPassword;
}


// implementation of ASM Crypto library for hashing user password
// https://github.com/vibornoff/asmcrypto.js/
function generatePWHash_ASM(password, salt)
{
    // this creates a password hash using PBKDF2 SHA256 with 20,000 iterations
    // with the 128 bit salt that server sends per the user
    var iterations = 20000;
    var dklen = 32;
    var hashedPassword = asmCrypto.PBKDF2_HMAC_SHA256.base64(password, salt, iterations, dklen);
    // passes to page
    document.getElementById("hash").value = hashedPassword;
}

