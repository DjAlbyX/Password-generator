import fs from 'node:fs';

try {
    const data = fs.readFileSync('./passwords.txt', 'utf8');
    console.log("Stored passwords:");
    console.log(data);
} catch (err) {
    console.error(err);
}
