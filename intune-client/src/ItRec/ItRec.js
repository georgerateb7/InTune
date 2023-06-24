import React, { useState } from "react";
import { Form, Button, Slider, Input, notification, Spin, Alert } from 'antd';

import 'antd/dist/antd.css';
import { CloudDownloadOutlined } from '@ant-design/icons';
import SearchableSelect from "../common/SearchableSelect";

import {USERS_WITH_DATA, SORTABLE_SONG_ATTRIBUTES} from "../api/constants";
import {generatePlaylist} from "../api/spotify";

const {TextArea} = Input;

function ItRec() {
  const [userHistory, setUserHistory]  = useState("");
  const [sortAttribute, setSortAttribute]  = useState("");
  const [sortStrength, setSortStrength] = useState(5);
  const [playlistName, setPlaylistName] = useState("");
  const [loading, setLoading] = useState(false);

  const onFinish = async () => {
    const resp = await generatePlaylist(sortAttribute, userHistory, sortStrength, playlistName);
    console.log(resp);
  }

  const openNotification = () => {
    setLoading(true);
    notification.open({
      message: 'Recommended Playlist is Being Generated',
      description:
        'Site backend is processing your selected data to determine the top 100 song recommendations for you! Expect to see a new playlist with your custom name in Spotify within the next 5 minutes.',
      onClick: () => {
        console.log('Notification Clicked!');
      },
    });
  };

  return (
    <div>
      <Spin spinning={loading}>
        <Form
        layout="vertical"
        style={{maxWidth: "600px", margin: "0 auto"}}
        onFinish={onFinish}
      >
        <h1>Custom Recommender</h1>
        <h3>Create a custom playlist in your Spotify account based on a user's listening history and associated preferences!</h3>
        <hr></hr>
        <Form.Item
          label="Whose Listening History Should Be Used?"
        >
          <SearchableSelect
            value={userHistory}
            onChange={setUserHistory}
            options={USERS_WITH_DATA}
            placeholder={"Target User"}
          />
        </Form.Item>
        <Form.Item
          label="Choose a Song Attribute to Filter By"
        >
          <SearchableSelect
            value={sortAttribute}
            onChange={setSortAttribute}
            options={SORTABLE_SONG_ATTRIBUTES}
            placeholder={"Sortable Song Attribute"}
          />
        </Form.Item>
        <Form.Item
          label="Choose What Percentile of Filtered Results Your Playlist Should be Sampled From"
        >
          <Slider
            value={sortStrength}
            onChange={setSortStrength}
            step={1}
            min={0}
            max={9}
            marks={{0: '10th Percentile', 9: '90th Percentile'}}
          />
        </Form.Item>
        <Form.Item
          label="Custom Playlist Name"
        >
          <TextArea
            placeholder="Playlist Name"
            value={playlistName}
            onChange={(event) => setPlaylistName(event.target.value)}
            allowClear={false}
            autoSize={true}
          />
        </Form.Item>
        <Form.Item>
          <Button
            type="primary"
            onClick={openNotification}
            htmlType="submit"
            size="large"
            icon={<CloudDownloadOutlined/>}
          >
            Generate Recommended Playlist
          </Button>
        </Form.Item>
      </Form>
      </Spin>
    </div>
  )
}

export default ItRec