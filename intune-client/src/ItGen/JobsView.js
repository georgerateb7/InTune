import React, {useEffect, useState} from 'react';

import {Table} from 'antd';
import {getAllJobs} from "../api/spotify";

import ReactAudioPlayer from 'react-audio-player';
import {SERVER_URL} from "../api/constants";
const JobsView = ({jobs, setJobs}) => {

  const columns = [
    {
      title: 'Slurm Job ID',
      dataIndex: 'slurm_job_id',
      key: 'slurm_job_id',
    },
    {
      title: 'Created By',
      dataIndex: 'spotify_username',
      key: 'spotify_username',
    },
    {
      title: 'Mode',
      dataIndex: 'mode',
      key: 'mode',
    },
    {
      title: 'Artist',
      dataIndex: 'artist',
      key: 'artist',
    },
    {
      title: 'Genre',
      dataIndex: 'genre',
      key: 'genre',
    },
    {
      title: 'Lyrics',
      dataIndex: 'lyrics',
      key: 'lyrics',
    },
    {
      title: 'Sample Length',
      dataIndex: 'sample_length_in_seconds',
      key: 'sample_length_in_seconds',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: 'Levels',
      key: 'wav_path',
      render: ({wavs}) => {
        return wavs.length !== 0
          ?
          wavs.map(wav => {
            return <ReactAudioPlayer
              src={`${SERVER_URL}/songs/${wav}`}
              autoPlay={false}
              controls
            />
          }) : <></>
      }
    }
  ]

  return (
    <div>
      <Table
        dataSource={jobs}
        columns={columns}
      />
    </div>
  )
}

export default JobsView