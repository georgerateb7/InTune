# inTune

## Developer Notes
**DO NOT DEVELOP DIRECTLY ON MASTER. WORK ON YOUR OWN BRANCH AND MAKE A PR WHEN READY FOR REVIEW.**

The Spotify auth flow is handled from the client side. Upon login, an auth token is accessible via the TokenContext provider in `App.js`. All RESTful requests to the Spotify API should invoke the `getData` utility function in `src/api/spotify.js`, which will logout the user if the token is expired.

The UI library is Ant Design: https://ant.design/. Rather than writing your own CSS, please try to use as much of the built-in components for Layout (Row, Col) and form components to minimize code and ensure a consistent user experience. 

All code for music recommendation should go in the `src/ItRec` directory. There is a component `ItGen.js` to help you get started.
All code for music generation should go in the `src/ItGen` directory.

## Startup

First, install all node modules. Make sure you have Node.js installed.

`cd intune-client`
`npm install`

Then in the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

