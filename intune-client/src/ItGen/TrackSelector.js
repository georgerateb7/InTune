import React from 'react'

import { Select } from 'antd'
const { Option } = Select

export default function({track, tracks, setTrack}) {
  const handleChange = (trackName) => {
    setTrack(tracks.find(track => track.name === trackName));
  }

  return (
    <div>
      <Select
        showSearch
        placeholder="Select a track"
        optionFilterProp="children"
        onChange={handleChange}
        filterOption={(input, option) =>
          option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
        }
        style={{ width: '100%' }}
        value={track.name}
      >
        {tracks.map((track, ix) => {
          return (<Option
            value = {track.name}
            key = {track.preview_url ?? ix}
            disabled = {track.preview_url !== null}
          >
            {`${track.name} - ${track.artists[0].name}`}
          </Option>)
        })}
      </Select>
    </div>
  )
}
