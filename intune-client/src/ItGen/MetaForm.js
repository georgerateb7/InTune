import {Button, Form, Slider, Input} from "antd";
import SearchableSelect from "../common/SearchableSelect";
import {JUKEBOX_ARTISTS, JUKEBOX_GENRES} from "../api/constants";
import TrackSelector from "./TrackSelector";
import React, {useState, useEffect} from "react";
import {useUserTopTracks} from "../contexts/UserContext";
const {TextArea} = Input;

export default function MetaForm({setMeta}) {
  const userTopTracks = useUserTopTracks();
  const [track, setTrack] = useState({name: "", preview_url: null})
  const [genre, setGenre]  = useState("")
  const [artist, setArtist]  = useState("")
  const [lyrics, setLyrics]  = useState("")

  useEffect(() => {
    setMeta({
      track, genre, artist, lyrics
    });
  }, [track, genre, artist, lyrics]);

  return(
    <Form
      layout="vertical"
      style={{maxWidth: "600px", margin: "0 auto"}}
    >
      <Form.Item
        label="Artist"
      >
        <SearchableSelect
          value={artist}
          onChange={setArtist}
          options={JUKEBOX_ARTISTS}
          placeholder={"Target Artist"}
        />
      </Form.Item>
      <Form.Item
        label="Genre"
      >
        <SearchableSelect
          value={genre}
          onChange={setGenre}
          options={JUKEBOX_GENRES}
          placeholder={"Target Genre"}
        />
      </Form.Item>
      <Form.Item
        label="Track"
      >
        <TrackSelector
          track={track}
          setTrack={setTrack}
          tracks={userTopTracks}
        />
      </Form.Item>
      <Form.Item
        label="Lyrics"
      >
        <TextArea
          placeholder="Lyrics"
          value={lyrics}
          onChange={(event) => setLyrics(event.target.value)}
          allowClear={true}
          autoSize={true}
        />
      </Form.Item>
    </Form>
  )
}
