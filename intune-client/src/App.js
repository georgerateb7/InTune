import './App.css';

import InTune from "./InTune";
import {useEffect, useState} from "react";
import {isTokenValid, loginToSpotify} from "./api/auth";

function App() {
  let [tokenIsValid, setTokenIsValid] = useState(false);

  useEffect(() => {
    const loginIfTokenIsInvalid = async () => {
      if (await isTokenValid()) {
        setTokenIsValid(true);
      } else {
        loginToSpotify()
      }
    }

    loginIfTokenIsInvalid();
  }, []);

  return (
      <div className="App">
        {tokenIsValid &&
          <header className="App-header">
            <InTune/>
          </header>
        }
      </div>
  );
}

export default App;
