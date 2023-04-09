I want you to act as a code generator. You will produce code in javascript to run on a nodejs back end. The application will include a rest api. I will ask you to produce modules with a specific purpose and I will integrate these in my editor. 

```Sure, I'd be happy to generate code for you! Please let me know what modules you need, and any specific functionality or requirements for each module.```

I want users to be able to enter a simple note and have it saved in a sqlite. Along with the text of the note, the current date should be stored. The add note endpoint should also accept a number of text tags on which the notes can be filtered.

* run npm init
Add this to the scripts section of package.json:
    "start": "node index.js"
 npm i body-parser express sqlite3

