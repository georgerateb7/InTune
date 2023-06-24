import httpClient from "./httpClient";
import {SERVER_URL} from "./constants";

export const getUserData = async () => {
  const {data} = await httpClient.get(`${SERVER_URL}/user_data`)
  return data;
}

export const generateSong = async (allMetas, sampleLength, levels) => {
  let metas = allMetas
    .filter(meta => {
      return (meta.artist !== "" || meta.genre !== "")
    })
    .map(meta => {
      const {
        artist,
        genre,
        track
      } = meta;

      return {
        ...meta,
        artist: (artist === "" ? "unknown" : artist),
        genre: (genre === "" ? "unknown" : genre),
        track: (track.name === "" ? null : track),
      }
    });

  console.log(metas)
  return await httpClient.post(
     `${SERVER_URL}/generate_song`,
     {
       metas,
       sampleLength,
       levels
     }
   );
}

export const getAllJobs = async () => {
  const {data} = await httpClient.get(`${SERVER_URL}/jobs`);
  return data.jobs;
}

export const generatePlaylist = async (sortAttribute, userHistory, sortStrength, playlistName) => {
  return await httpClient.post(
    `${SERVER_URL}/recommend_playlist`,
    {
      userHistory,
      sortAttribute: (sortAttribute === "" ? null : sortAttribute), 
      sortStrength,
      playlistName: (playlistName === "" ? "Untitled Plalist" : playlistName)
    });
}
