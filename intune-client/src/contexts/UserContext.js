import React, {createContext, useEffect, useMemo, useState} from "react";
import {getUserData} from "../api/spotify";

const UserContext = createContext();

const USER_DATA_INITIAL_STATE = {
  current_user: {
    display_name: ""
  },
  top_tracks: [],
  top_artists: [],
}

export function UserContextProvider({ children }) {
  let [userData, setUserData] = useState(USER_DATA_INITIAL_STATE);

  const userDataValue = useMemo(() => ({
    userData, setUserData
  }), [userData]);

  useEffect(() => {
    (async () => {
      setUserData(await getUserData());
    })();
  }, []);

  return (
    <UserContext.Provider value={userDataValue}>
      {children}
    </UserContext.Provider>
  )
}

export function useUserData() {
  const context = React.useContext(UserContext);
  return context;
}

export function useUserTopTracks() {
  const context = React.useContext(UserContext);
  return context.userData.top_tracks;
}
