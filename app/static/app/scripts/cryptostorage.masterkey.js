// This is the main function to generate the hash for your password
// generates the hash password on the client side using PBKDF2 SHA-256
// with the server's 128 random salt

// implementation of crypto.js library for hashing user password
function generatePWHash(password, salt,elementId)
{
    // we perform 5000 iterations of a 
    // key size of 256 bits. Note the keysize is 256 /32 since we need to account
    // for the hexadecimal representation which account for 2 hex values per character.
    // This function is per crypto.js
    var hashedPassword = CryptoJS.PBKDF2(password, salt, { keySize: 256 / 32, iterations: 5000 });
    // store password in local storage
    localStorage.setItem(elementId, hashedPassword);
    
    return hashedPassword;
}


// implementation of ASM Crypto library for hashing user password
// https://github.com/vibornoff/asmcrypto.js/
function generatePWHash_ASM(password, salt, elementId)
{
    // this creates a password hash using PBKDF2 SHA256 with 20,000 iterations
    // with the 128 bit salt that server sends per the user
    var iterations = 20000;
    var dklen = 32;
    var hashedPassword = asmCrypto.PBKDF2_HMAC_SHA256.base64(password, salt, iterations, dklen);
    // passes to page if required
    if (elementId != null) {
        document.getElementById(elementId).value = hashedPassword;
    }
        
    return hashedPassword
}

// generate file hashes for keying the file
// https://github.com/vibornoff/asmcrypto.js/
function generateFileHashes(password) {
    // this creates a password hash using PBKDF2 SHA256 with 20,000 iterations
    // with the 128 bit salt that server sends per the user
    var iterations = 20000;
    var dklen = 32;
    // lets generate a secured 128 bit salt
    // using sjcl pseudo random number generator
    // randomWords generates 4 bytes(32bits) of random words x 4 = 128 bits
    var salt = sjcl.codec.base64.fromBits(sjcl.random.randomWords(4));
    // remove the last two characters (bas64 endings)
    // and 6 chars to be the base64 representation of 16 characters
    salt = salt.substring(0, salt.length - 8)
    // generate pbkdf2 key for file
    var hash = asmCrypto.PBKDF2_HMAC_SHA256.base64(password, salt, iterations, dklen);
    // pbkdf2 key for encrypting the file
    // type$iterations$salt$hash
    var file_security_properties = "pbkdf2_sha256$" + iterations + "$" + salt + "$" + hash
    // store master key details in local storage
    localStorage.setItem("file_security_properties", file_security_properties);

}


// extracts element from hasher string
function hasherExtract(hasher_object, element) {

    // hasher structure
    // type$iterations$salt$hash
    var hasher_array= hasher_object.split("$")
    if (element == "type")
        return hasher_array[0];
    else if (element == "iterations")
        return hasher_array[1];
    else if (element == "salt")
        return hasher_array[2];
    else if (element == "hash")
        return hasher_array[3];
}

// composes a string $ separated of variables needed for
// hmac and encryption of file based on JSON object
// ommit the ct(encrypted data). Stored in database
function encryptForServer(properties) {

    properties = JSON.parse(properties)
    properties = properties.iv + "$" +
                 properties.iter + "$" +
                 properties.ks + "$" +
                 properties.ts + "$" +
                 properties.mode + "$" +
                 properties.adata + "$" +
                 properties.cipher + "$" +
                 properties.salt;

    return properties;
}

// converts a server seperated $ encryption string
// to the required decryption json object for sjcl.decrypt()
function encryptForDecrypt(encrypt_for_server_object, file_encrypt) {

    var efso_parsed = encrypt_for_server_object.split("$");

    return JSON.stringify({
        "iv":     efso_parsed[0],
        "iter":   parseInt(efso_parsed[1]),
        "ks":     parseInt(efso_parsed[2]),
        "ts":     parseInt(efso_parsed[3]),
        "mode":   efso_parsed[4],
        "adata":  efso_parsed[5],
        "cipher": efso_parsed[6],
        "salt":   efso_parsed[7],
        "ct":     file_encrypt})
    
}




