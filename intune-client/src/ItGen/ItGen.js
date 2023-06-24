import React,
  {
    useState,
    useEffect
  } from "react";

import {
  Form,
  Button,
  Row,
  Col,
  Input,
  Collapse,
  Slider,
} from 'antd';


import { CloudUploadOutlined } from '@ant-design/icons';

import SearchableSelect from "../common/SearchableSelect";

import 'antd/dist/antd.css';
import TrackSelector from "./TrackSelector";
import {JUKEBOX_ARTISTS, JUKEBOX_GENRES} from "../api/constants";
import {useUserTopTracks} from "../contexts/UserContext";
import {generateSong, getAllJobs} from "../api/spotify";
import JobsView from "./JobsView";
import MetaForm from "./MetaForm";

const {Panel} = Collapse;

const twoInputLayout = {
  xs: 24,
  md: 12
}

const BLANK_TRACK = {name: "", preview_url: null}
const BLANK_META = {
  track: {...BLANK_TRACK},
  genre: "",
  artist: "",
  lyrics: "",
  sampleLength: 60
}

const deepClone = (inp) => JSON.parse(JSON.stringify(inp))

function ItGen() {
  let [jobs, setJobs] = useState([]);
  let [sampleLength, setSampleLength] = useState(20);
  let [levels, setLevels] = useState(1);

  useEffect(() => {
    (async() => {
      const jobs = await getAllJobs();
      setJobs(jobs);
    })();
  }, []);

  let metas = [
    deepClone(BLANK_META),
    deepClone(BLANK_META),
    deepClone(BLANK_META),
    deepClone(BLANK_META)
  ];

  const onFinish = async () => {
    const resp = await generateSong(metas, sampleLength, levels);
    console.log(resp)
    const jobs = await getAllJobs();
    setJobs(jobs);
  }


  const setMetaByIndex = (ix, meta) => {
    metas[ix] = meta;
  }

  return (
    <div>
      <Collapse>
        {[1, 2, 3, 4].map((_, ix)=>{
          return <Panel key={ix} header={`Job ${ix + 1}`}>
            <MetaForm
              setMeta={((meta) => {setMetaByIndex(ix, meta)})}
            />
          </Panel>
        })}
      </Collapse>
      <Form
        layout="vertical"
        style={{padding: "30px", background: 'white', margin: "30px 0"}}
      >
        <Form.Item
          label="Sample Length (seconds)"
        >
          <Slider
            value={sampleLength}
            onChange={setSampleLength}
            step={1}
            min={20}
            max={60}
            marks={{20: '20s', 60: '60s'}}
          />
        </Form.Item>

        {/*<Form.Item*/}
        {/*  label="Number of Levels (3 takes multiple hours)"*/}
        {/*>*/}
        {/*  <Slider*/}
        {/*    value={levels}*/}
        {/*    onChange={setLevels}*/}
        {/*    step={1}*/}
        {/*    min={1}*/}
        {/*    max={3}*/}
        {/*    marks={{1: '1', 2: '2', 3: '3'}}*/}
        {/*  />*/}
        {/*</Form.Item>*/}
        <Button
          type="primary"
          htmlType="submit"
          size="large"
          icon={<CloudUploadOutlined/>}
          onClick={onFinish}
        >
          Generate
        </Button>
      </Form>
      <JobsView
        jobs={jobs}
        setJobs={setJobs}
      />
    </div>
  )
}

export default ItGen
