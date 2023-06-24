import httpClient from "./httpClient";
import {SERVER_URL} from "./constants";

export const loginToSpotify = () => {
  window.location.href = `${SERVER_URL}/authorize`;
}

export const isTokenValid = async () => {
  const {data} = await httpClient.get(`${SERVER_URL}/token_status`);
  return data;
}
